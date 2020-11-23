from django import forms


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
        widget=forms.PasswordInput(attrs = {'autocomplete': 'new-password'}),
    )


class SearchForm(forms.Form):
    search_string = forms.CharField()


class EditOwnCompany(forms.Form):
    name_company = forms.CharField()
    logo = forms.ImageField()
    workers_amount = forms.IntegerField()
    city = forms.CharField()
    description = forms.CharField()