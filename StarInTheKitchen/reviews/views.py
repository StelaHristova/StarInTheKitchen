from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .forms import ReviewForm
from .models import Review
from StarInTheKitchen.recipes.models import Recipe


@login_required
def submit_review(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    try:
        existing = Review.objects.get(user=request.user, recipe=recipe)
        form = ReviewForm(request.POST, instance=existing)
    except Review.DoesNotExist:
        form = ReviewForm(request.POST)

    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.recipe = recipe
        review.save()

    return redirect('recipe-detail', pk=pk)
