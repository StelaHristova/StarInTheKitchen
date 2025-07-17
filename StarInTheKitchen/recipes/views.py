
from django.forms import inlineformset_factory
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


from .models import Recipe
from .forms import RecipeForm
from StarInTheKitchen.ingredients.models import Ingredient
from StarInTheKitchen.ingredients.forms import IngredientForm


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

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        IngredientFormSet = inlineformset_factory(
            Recipe,
            Ingredient,
            form=IngredientForm,
            extra=1,
            can_delete=True
        )
        if self.request.POST:
            data['ingredients'] = IngredientFormSet(self.request.POST)
        else:
            data['ingredients'] = IngredientFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        ingredients = context['ingredients']
        form.instance.created_by = self.request.user
        self.object = form.save()

        if ingredients.is_valid():
            ingredients.instance = self.object
            ingredients.save()
        else:
            return self.form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

