from django import forms

from socialdict.models import Term

class TermForm(forms.ModelForm):
    meaning = forms.CharField(widget=forms.Textarea, max_length=140)

    class Meta:
        model = Term
        exclude = ('alphabet_letter', 'date_added')
