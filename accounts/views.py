from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from django.http.response import JsonResponse
from django.http import HttpResponse

from .models import Profile

from .forms import CustomUserChangeForm, CustomUserCreationForm, ProfileForm


@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('community:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('movies:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)

@login_required
def member_del(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    context = {
        'person': person,
    }
    if request.method=='POST':
        pw_del = request.POST["pw_del"]
        user = request.user
        if check_password(pw_del, user.password):
            user.delete()
            return redirect('movies:index')
    return render(request, 'accounts/member_del.html',context)
        # if not check_password(pw_del,user.password):


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('movies:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'movies:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@require_POST
def logout(request):
    auth_logout(request)
    return redirect('movies:index')


@login_required
def profile(request, username):

    person = get_object_or_404(get_user_model(), username=username)
    context = {
        'person': person,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def profupdate(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    context = {
        'person': person,
    }
    if request.method=='POST':
        user_change_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST,request.FILES, instance=request.user.profile)
        if user_change_form.is_valid() and profile_form.is_valid():
            user = user_change_form.save()
            profile_form.save()
            return redirect('accounts:profile', user.username)
        return redirect('accounts:profupdate')
    else:
        user_change_form = CustomUserChangeForm(instance=request.user)
        # 새롭게 추가하는 것이 아니라 수정하는 것이기 때문에
        # 기존의 정보를 가져오기 위해 instance를 지정해야 한다.
        profile, create = Profile.objects.get_or_create(user=request.user)
        # Profile 모델은 User 모델과 1:1 매칭이 되어있지만
        # User 모델에 새로운 인스턴스가 생성된다고 해서 그에 매칭되는 Profile 인스턴스가 생성되는 것은 아니기 때문에
        # 매칭되는 Profile 인스턴스가 있다면 그것을 가져오고, 아니면 새로 생성하도록 한다.
        profile_form = ProfileForm(instance=profile)
        return render(request, 'accounts/profilemod.html', {
            'user_change_form': user_change_form,
            'profile_form': profile_form
        })


    

@require_POST
def follow(request, user_pk):
    if request.user.is_authenticated:
        person = get_object_or_404(get_user_model(), pk=user_pk)
        user = request.user
        if person != user:
            if person.followers.filter(pk=user.pk).exists():
                person.followers.remove(user)
                is_follow = False
            else:
                person.followers.add(user)
                is_follow = True
            data = {
                'is_follow': is_follow,
                'cnt_following': person.followings.count(),
                'cnt_follower': person.followers.count(),
            }
            return JsonResponse(data)
    return redirect('accounts:profile', person.username)


@login_required
def chg_pw(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('movies:index')
    else:
        form = PasswordChangeForm(request.user)
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/chg_pw.html', context)