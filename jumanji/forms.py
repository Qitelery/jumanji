from django import forms


class SendForm(forms.Form):
    name = forms.CharField()
    telephone = forms.IntegerField()
    cover_letter = forms.CharField()
