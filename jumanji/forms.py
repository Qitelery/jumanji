from django import forms
from django.forms import ModelForm

from jumanji.models import Company, Resume, Vacancy


class SendForm(forms.Form):
    name = forms.CharField()
    telephone = forms.IntegerField()
    cover_letter = forms.CharField()


class Registration(forms.Form):
    login = forms.CharField()
    name = forms.CharField()
    surname = forms.CharField()
    password = forms.CharField(
        label="password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )


class LogInForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(
        label="password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )


class SearchForm(forms.Form):
    search_string = forms.CharField()


class EditOwnCompany(ModelForm):

    class Meta:
        model = Company
        fields = ['title', 'logo', 'employee_count', 'location', 'description']


class ResumeForm(ModelForm):

    class Meta:
        model = Resume
        fields = ['name', 'surname', 'status', 'salary', 'specialty', 'qualification', 'education', 'experience', 'portfolio']


class VacancyForm(ModelForm):

    class Meta:
        model = Vacancy
        fields = ['title', 'specialty', 'salary_min', 'salary_max', 'skills', 'description']