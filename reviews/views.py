from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Review
from .forms import ReviewForm
from django.contrib.auth import get_user_model


# Create your views here.
def index(request):
    return render(request, 'reviews/index.html')

@login_required
def create(request):
    if request.method == 'POST':
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, '글 작성이 완료되었습니다.')
            return redirect('reviews:community')
    else: 
        review_form = ReviewForm()
    context = {
        'review_form': review_form
    }
    return render(request, 'reviews/create.html', context=context)

def community(request):
    reviews = Review.objects.order_by('-pk')
    context = {
        'reviews': reviews
    }
    return render(request, 'reviews/community.html', context)


def detail(request, pk):
  review = Review.objects.get(pk=pk)
  context = {
    'review': review
    }
  return render(request, 'reviews/detail.html', context)
