import logging
from django.db import models
from django.core.validators import RegexValidator
from django import forms

from .models import Person, PersonalInformations, Entreprise

class EntrepriseForm(forms.ModelForm):
    entrepriseName = forms.CharField(label="Entreprise Name")
    entreprisePassword = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirmPassword = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    class Meta:
        model = Entreprise
        fields = ('entrepriseName' ,'entreprisePassword',)

    def clean(self):
        cleaned_data = super(EntrepriseForm, self).clean()
        entreprisePassword = cleaned_data.get("entreprisePassword")
        confirmPassword = cleaned_data.get("confirmPassword")

        if entreprisePassword != confirmPassword:
            raise forms.ValidationError(
                "Both passwords do not match"
            )

alphanumeric = RegexValidator(r'^[0-9]*$', 'Only numeric characters are allowed for the Sin number.')
class PersonForm(forms.ModelForm):
    Person_Password = forms.CharField(widget=forms.PasswordInput)
    Confirm_Password = forms.CharField(widget=forms.PasswordInput)
    SIN_Number = forms.CharField(min_length=9, max_length=9, validators=[alphanumeric],label="Sin number")
    class Meta:
        model = Person
        fields = ('SIN_Number', 'Person_Name', 'Person_Password', )

    def clean(self):
        cleaned_data = super(PersonForm, self).clean()
        Person_Password = cleaned_data.get("Person_Password")
        Confirm_Password = cleaned_data.get("Confirm_Password")

        if Person_Password != Confirm_Password:
            raise forms.ValidationError("Both passwords do not match")


SEXE_CHOICES = (
('m','Men'),('w','Women'))
phone = RegexValidator(r'^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$', 'Phone number is not valid.')
postalCode = RegexValidator(r'^[ABCEGHJKLMNPRSTVXY][0-9][ABCEGHJKLMNPRSTVWXYZ] ?[0-9][ABCEGHJKLMNPRSTVWXYZ][0-9]$', 'Postal code is not valid')

class PersonalInformationsForm(forms.ModelForm):
    adress = forms.CharField(max_length=80)
    postalCode = forms.CharField(max_length=7, min_length=6, label="Postal code", validators=[postalCode])
    sexe = forms.CharField(widget=forms.Select(choices=SEXE_CHOICES))
    personEmail = forms.EmailField(label="Email")
    phone = forms.CharField(max_length=14, validators=[phone])
    sinNumberPersonne = forms.ModelChoiceField(queryset=Person.objects.all(),required=False, widget=forms.HiddenInput(), label="")

    class Meta:
        model = PersonalInformations
        fields = ('adress', 'postalCode', 'sexe', 'personEmail','phone', 'sinNumberPersonne')
