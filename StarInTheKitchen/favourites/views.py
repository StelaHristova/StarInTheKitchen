from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from StarInTheKitchen.favourites.models import Favourite
from StarInTheKitchen.recipes.models import Recipe


@login_required
def toggle_favourite(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    fav, created = Favourite.objects.get_or_create(user=request.user, recipe=recipe)

    if not created:
        fav.delete()
    return redirect('recipe-detail', pk=pk)


@login_required
def my_favourites(request):
    favourites = Favourite.objects.filter(user=request.user).select_related('recipe')
    return render(request, 'favourites/favourite_list.html', {'favourites': favourites})