from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from .models import Review, Comment
from .forms import ReviewForm, CommentForm
from django.core.paginator import Paginator


@require_GET
def index(request):
    reviews = Review.objects.order_by('-pk')
    paginator = Paginator(reviews, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'community/index.html', context)

@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        review_form = ReviewForm(request.POST) 
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('community:detail', review.pk)
    else:
        review_form = ReviewForm()
    context = {
        'review_form': review_form,
        'site_name': '게시글 작성'
    }
    return render(request, 'community/form.html', context)


@require_GET
def detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comments = review.comment_set.all()
    comment_form = CommentForm()
    context = {
        'review': review,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'community/detail.html', context)

@login_required
@require_http_methods(['GET', 'POST'])
def update(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user != review.user:
        return redirect('community:index')
    if request.method == 'POST':
        review_form = ReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            review_form.save()
            return redirect('community:detail', review.pk)
    else:
        review_form = ReviewForm(instance=review)
    context = {
        'review': review,
        'review_form': review_form,
        'site_name': '글 수정',
    }
    return render(request, 'community/form.html', context)

@login_required
@require_POST
def delete(request, review_pk):
    review =get_object_or_404(Review, pk=review_pk)
    review.delete()
    return redirect('community:index')

@login_required
@require_POST
def create_comment(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
        return redirect('community:detail', review.pk)
    context = {
        'comment_form': comment_form,
        'review': review,
        'comments': review.comment_set.all(),
    }
    return render(request, 'community/detail.html', context)


@require_POST
def like(request, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        user = request.user

        if review.like_users.filter(pk=user.pk).exists():
            review.like_users.remove(user)
            is_like = False
        else:
            review.like_users.add(user)
            is_like = True
        data = {
            'is_like': is_like,
            'cnt_like': review.like_users.count(),
        }
        return JsonResponse(data)
    return redirect('accounts:login')

def kakaomap(request):
    return render(request, 'community/kakaomap.html')