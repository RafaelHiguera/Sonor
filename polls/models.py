from __future__ import unicode_literals

from django.db import models

class Entreprise(models.Model):
    entrepriseName = models.CharField(max_length=100, primary_key=True)
    entreprisePassword = models.CharField(max_length=200)

class Person(models.Model):
    SIN_Number = models.CharField(max_length=9, primary_key=True)
    Person_Name = models.CharField(max_length=100)
    Person_Password = models.CharField(max_length=500)
    isInEntrepriseName = models.ForeignKey(Entreprise, null=False, default="None",on_delete=models.SET_DEFAULT)

class Requests(models.Model):
    personSINRequests = models.ForeignKey(Person, null=False ,on_delete=models.CASCADE)
    entrepriseNameRequests = models.ForeignKey(Entreprise, null=False ,on_delete=models.CASCADE)
    jobName = models.CharField(max_length=200, null=False)

class Record(models.Model):
    recordFlag = models.BooleanField(default=False, editable=True)
    sinNumberPersonne = models.ForeignKey(Person, on_delete=models.CASCADE)

class PersonalInformations(models.Model):
    adress = models.CharField(max_length=80)
    postalCode = models.CharField(max_length=7)
    sexe = models.CharField(max_length=1)
    personEmail = models.CharField(max_length=50)
    phone = models.CharField(max_length=14)
    sinNumberPersonne = models.ForeignKey(Person , on_delete=models.CASCADE)
