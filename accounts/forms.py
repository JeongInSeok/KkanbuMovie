from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model

from django.db import models
from .models import Profile
from django import forms

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields

class CustomUserChangeForm(UserChangeForm):
    # 유저 체인지 폼에서는 password 수정 불가
    password = None
    class Meta:
        model = User
        fields = ['email','username']

class ProfileForm(forms.ModelForm):
    nickname = forms.CharField(label="별명", required=False)
    description = forms.CharField(label="자기소개", required=False, widget=forms.Textarea())
    image = forms.ImageField(label="이미지", required=False)
   	# 위의 내용을 정의하지 않아도 상관없지만, 화면에 출력될 때 label이 영문으로 출력되는 것이 싫어서 수정한 것이다..
    class Meta:
        model = Profile
        fields = ['nickname', 'description', 'image',]