
from django.forms import inlineformset_factory
from django.db.models import Q
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
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
        # queryset = Recipe.objects.all()

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
        method = self.request.GET.get('method')
        occasion = self.request.GET.get('occasion')

        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        if meal_type:
            queryset = queryset.filter(meal_types__id=meal_type)
        if season:
            queryset = queryset.filter(seasons__id=season)
        if diet:
            queryset = queryset.filter(diets__id=diet)
        if method:
            queryset = queryset.filter(methods__id=method)
        if occasion:
            queryset = queryset.filter(occasions__id=occasion)

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

            try:
                review = Review.objects.get(user=self.request.user, recipe=recipe)
                context['review_form'] = ReviewForm(instance=review)
            except Review.DoesNotExist:
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

        # if invalid, re-render with the form and context
        context = self.get_context_data()
        context['review_form'] = form
        return self.render_to_response(context)
    #     context = super().get_context_data(**kwargs)
    #     recipe = self.object
    #
    #     if self.request.user.is_authenticated:
    #         context['is_favourited'] = recipe.favourited_by.filter(user=self.request.user).exists()
    #     else:
    #         context['is_favourited'] = False
    #
    #     return context


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'
    success_url = reverse_lazy('recipe-list')

    def get_success_url(self):
        return reverse_lazy('recipe-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'

    def dispatch(self, request, *args, **kwargs):
        recipe = self.get_object()

        if recipe.is_approved:
            return HttpResponseForbidden("You cannot edit an approved recipe.")

        if recipe.created_by != self.request.user:
            return HttpResponseForbidden("You can only edit your own recipes.")

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('recipe-detail', kwargs={'pk': self.object.pk})