from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Review
from .forms import ReviewForm

def reviews_page(request):
    reviews = Review.objects.all().order_by('-created_at')  # Mostrar reseñas más recientes

    # Manejo del formulario de reseñas
    if request.user.is_authenticated and request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user 
            review.save()
            return redirect('reviews_page')
    else:
        form = ReviewForm() if request.user.is_authenticated else None  

    context = {
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'reviews/reviews_page.html', context)
