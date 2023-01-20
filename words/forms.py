from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from .models import *


# class AddWordsForm(forms.Form):
#     word = forms.CharField(widget=forms.Textarea(attrs={'cols':60, 'rows':10}), label='', initial='type here')

# class AddWordsForm(forms.Form):
#     word = forms.CharField(widget=forms.Textarea(
#         attrs={'placeholder': 'English text'}), label='', )
#
#
# class AddTranslationForm(forms.Form):
#     translation = forms.CharField(widget=forms.Textarea(
#         attrs={'placeholder': "Russian translation"}), label='')

class WordTranslationForm(forms.Form):
    word = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'English text'}), label='', required=False)
    translation = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': "Russian translation"}), label='', required=False)





class ChooseAmountOfWordsToLearnForm(forms.Form):
    amount_of_words_to_learn = forms.IntegerField(widget=forms.NumberInput(
        attrs={}), min_value=1, max_value=100, step_size=1, label='')

# class ChooseAmountOfWordsToLearnForm(forms.Form):
#     amount_of_words_to_learn = forms.IntegerField(widget=forms.NumberInput(
#         attrs={'value': 5}), min_value=1, max_value=100, step_size=1, label='')

class ButtonStartTestForm(forms.Form):
    pass

class ButtonChooseAnswerForm(forms.Form):
    pass
    # c = forms.ChoiceField()

class ButtonRenewAnswersCounterForm(forms.Form):
    pass

class AddButtonDeletionForm(forms.Form):
    pass

class SwitchLanguageForTest(forms.Form):
    pass

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
