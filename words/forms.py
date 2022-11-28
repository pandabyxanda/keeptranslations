from django import forms
from .models import *

class AddWordsForm(forms.Form):
    word = forms.CharField(widget=forms.Textarea(attrs={'cols':60, 'rows':10}), label='', initial='type here')

class AddTranslationForm(forms.Form):
    translation = forms.CharField(widget=forms.Textarea(attrs={'cols':60, 'rows':10}), label='')

class AddWordsForm1(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['word'].label = ''
        self.fields['translation'].label = ''

    class Meta:
        model = Words
        fields = ['word', 'translation']
        widgets = {
            'word': forms.Textarea(attrs={'cols':60, 'rows':10}),
            'translation': forms.Textarea(attrs={'cols':60, 'rows':10}),
        }



