
from django.forms import inlineformset_factory
from django.db.models import Q
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


from .models import Recipe
from .forms import RecipeForm


class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Recipe.objects.filter(
                Q(is_approved=True) | Q(created_by=user)
            ).distinct()
        return Recipe.objects.filter(is_approved=True)


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if not obj.is_approved and obj.created_by != self.request.user:
            raise Http404("This recipe is not available.")
        return obj


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