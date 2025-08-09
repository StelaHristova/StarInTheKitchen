from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy


from .models import Recipe
from .forms import RecipeForm
from ..reviews.forms import ReviewForm
from ..reviews.models import Review


class MyRecipesView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/my_recipes.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        return Recipe.objects.filter(created_by=self.request.user)


class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            queryset = Recipe.objects.filter(
                Q(is_approved=True) | Q(created_by=user)
            ).distinct()
        else:
            queryset = Recipe.objects.filter(is_approved=True)

        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(title__icontains=query)

        search_query = self.request.GET.get('search', '').strip()
        meal_type = self.request.GET.get('meal_type')
        season = self.request.GET.get('season')
        diet = self.request.GET.get('diet')
        cooking_method = self.request.GET.get('cooking_method')
        occasion = self.request.GET.get('occasion')

        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        if meal_type:
            queryset = queryset.filter(meal_types__id__in=meal_type)
        if season:
            queryset = queryset.filter(seasons__id__in=season)
        if diet:
            queryset = queryset.filter(diets__id__in=diet)
        if cooking_method:
            queryset = queryset.filter(cooking_methods__id__in=cooking_method)
        if occasion:
            queryset = queryset.filter(occasions__id__in=occasion)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not context['recipes']:
            context['no_results'] = True

        return context


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if not obj.is_approved and obj.created_by != self.request.user:
            raise Http404("This recipe is not available.")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.object

        if self.request.user.is_authenticated:
            context['is_favourited'] = recipe.favourited_by.filter(user=self.request.user).exists()
            context['can_review'] = recipe.created_by != self.request.user

            if Review.objects.filter(user=self.request.user, recipe=recipe).exists():
                context['review_form'] = None
            else:
                context['review_form'] = ReviewForm()

        else:
            context['is_favourited'] = False
            context['can_review'] = False

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated:
            return redirect('login-page')

        try:
            review = Review.objects.get(user=request.user, recipe=self.object)
            form = ReviewForm(request.POST, instance=review)
        except Review.DoesNotExist:
            form = ReviewForm(request.POST)

        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.user = request.user
            new_review.recipe = self.object
            new_review.save()
            return redirect('recipe-detail', pk=self.object.pk)

        context = self.get_context_data()
        context['review_form'] = form
        return self.render_to_response(context)


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'
    success_url = reverse_lazy('recipe-list')

    def get_success_url(self):
        return reverse_lazy('recipe-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        form.instance.created_by = self.request.user
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'

    def get_queryset(self):
        return Recipe.objects.filter(created_by=self.request.user)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        recipe = self.get_object()

        if recipe.is_approved:
            raise PermissionDenied("You cannot edit an approved recipe.")

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('recipe-detail', kwargs={'pk': self.object.pk})


class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    template_name = 'recipes/recipe_confirm_delete.html'
    success_url = reverse_lazy('my-recipes')

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.created_by