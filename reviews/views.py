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

@login_required
def update(request, pk):
    review = Review.objects.get(pk=pk)
    if request.user == review.user:

        if request.method == 'POST':
            # POST : input 값 가져와서, 검증하고, DB에 저장
            review_form = ReviewForm(request.POST, request.FILES, instance=review)
            if review_form.is_valid():
                # 유효성 검사 통과하면 저장하고, 상세보기 페이지로
                review_form.save()
                messages.success(request, '글이 수정되었습니다.')
                return redirect('reviews:detail', review.pk)
            # 유효성 검사 통과하지 않으면 => context 부터해서 오류메시지 담긴 article_form을 랜더링
        else:
            # GET : Form을 제공
            review_form = ReviewForm(instance=review)
        context = {
            'review_form': review_form
        }
        return render(request, 'reviews/create.html', context)
    else:
        # 403 에러메세지를 던진다
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden()
