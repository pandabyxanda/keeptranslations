from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *


# from django.contrib.auth.models import User
# from captcha.fields import CaptchaField


class WordTranslationForm(forms.Form):
    word = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'English text'}), label='', required=False)
    translation = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': "Russian translation"}), label='', required=False)


class Choose_collection_form(forms.Form):
    pass
    # collection = forms.ModelChoiceField(queryset=Collection.objects.all(), empty_label="(Nothing)")


class ChooseAmountOfWordsToLearnForm(forms.Form):
    amount_of_words_to_learn = forms.IntegerField(widget=forms.NumberInput(
        attrs={}), min_value=1, max_value=100, step_size=1, label='')


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        label='Login',
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': "login"})
    )
    email = forms.EmailField(
        label='Email', required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': "email (not necessary)"})
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'password'})
    )
    password2 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'password'})
    )

    # captcha = CaptchaField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label='Login',
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': "login"})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': "password"})
    )
