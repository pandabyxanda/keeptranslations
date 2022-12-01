from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from .models import *

# class AddWordsForm(forms.Form):
#     word = forms.CharField(widget=forms.Textarea(attrs={'cols':60, 'rows':10}), label='', initial='type here')

class AddWordsForm(forms.Form):
    word = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Type english text here'}), label='', )

class AddTranslationForm(forms.Form):
    translation = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': "Translation"}), label='')

# class AddWordsForm1(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['word'].label = ''
#         self.fields['translation'].label = ''
#
#     class Meta:
#         model = Words
#         fields = ['word', 'translation']
#         widgets = {
#             'word': forms.Textarea(attrs={'cols':60, 'rows':10, 'placeholder': 'Type english text here'}),
#             'translation': forms.Textarea(attrs={'cols':60, 'rows':10,
#                                                  'placeholder': "Translation of your text appears here"}),
#         }



class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Login',
                               widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': "Your name/login"}))
    email = forms.EmailField(label='Email', required=False,
                             widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': "not necessary"}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    captcha = CaptchaField()
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        # widgets = {
        #     'username': forms.TextInput(attrs={'class': 'form-input'}),
        #     'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
        #     'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
        #           }


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    # captcha = CaptchaField(label='Captcha_y0')

