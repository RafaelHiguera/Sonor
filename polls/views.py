import logging
import os
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from pathlib import Path
from django.contrib.auth.hashers import make_password,check_password
from django.http import HttpResponse
from django.utils.encoding import smart_str


from .forms import PersonForm, PersonalInformationsForm, EntrepriseForm
from .models import Entreprise, Person, Record, PersonalInformations, Requests


def index(request):
    Logout(request)
    return render(request, 'index.html')

def EntrepriseHomepage(request):
    return render(request, 'polls/EntrepriseHomepage.html')

def PersonHomepage(request):
    return render(request, 'polls/PersonHomepage.html')

def HomeP(request):
    if  not sessionValidePersonne(request):
        return redirect('PersonSignup')
    name = Person.objects.get(SIN_Number=request.session['SIN_Number']).isInEntrepriseName_id
    return render(request, 'polls/HomeP.html', {'entrepriseName': name})

def RequestForEntreprise(request):
    if  not sessionValidePersonne(request):
        return redirect('PersonSignup')
    entreprises = Entreprise.objects.all()
    return render(request, 'polls/EntrepriseRequest.html', {'entreprises': entreprises})

def PersonRequest(request):
    if  not sessionValideEntreprise(request):
        return redirect('EntrepriseSignup')
    errorMessage = ""
    if request.method == 'POST':
        cvExiste = ""
        cvExistantDoc = Path('Cvs/'+request.POST['SIN_Number']+".docx")
        cvExistantPdf = Path('Cvs/'+request.POST['SIN_Number']+".pdf")
        if cvExistantPdf.exists():
            cvExiste = cvExistantPdf
        elif cvExistantDoc.exists():
            cvExiste = cvExistantDoc
        if os.path.exists(cvExiste):
            with open(cvExiste, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(cvExiste)
                return response
        else:
            errorMessage = "Cv no existant!"
    if request.method == 'GET' and 'Sin' in request.GET:
        person = Person.objects.get(SIN_Number=request.GET['Sin'])
        person.isInEntrepriseName = Entreprise.objects.get(entrepriseName=request.session['entrepriseName'])
        person.save()
        requests = Requests.objects.get(id=request.GET['id'])
        requests.delete()
        return redirect('PersonRequest')
    requests = Requests.objects.filter(entrepriseNameRequests=request.session['entrepriseName'])
    return render(request, 'polls/PersonRequest.html', {'requests': requests, 'errorMessage':errorMessage})

def RequestsDispachter(request):
    if  not sessionValidePersonne(request):
        return redirect('PersonSignup')
    entrepriseName = ""
    if request.method == 'GET':
        entrepriseName = request.GET['entrepriseName']
    if request.method == 'POST':
        requests = Requests()
        requests.personSINRequests = Person.objects.get(SIN_Number=request.session["SIN_Number"])
        requests.entrepriseNameRequests = Entreprise.objects.get(entrepriseName=request.GET['entrepriseName'])
        requests.jobName = request.POST["jobName"]
        requests.save()
        return redirect('HomeP')
    return render(request, 'polls/RequestDispatcher.html', {'entrepriseName': entrepriseName})


def HomeE(request):
    if  not sessionValideEntreprise(request):
        return redirect('EntrepriseSignup')
    entreprise = Entreprise.objects.get(entrepriseName=request.session['entrepriseName'])
    return render(request, 'polls/HomeE.html')

def PersonSignup(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            formFinal = form.save(commit=False)
            formFinal.Person_Password = make_password(formFinal.Person_Password)
            request.session['SIN_Number'] = formFinal.SIN_Number
            formFinal.save()
            return redirect('Personal_Informations')
    else:
        form = PersonForm()
    return render(request, 'polls/PersonSignup.html', {'form': form})

def EntrepriseSignup(request):
    if request.method == 'POST':
        form = EntrepriseForm(request.POST)
        if form.is_valid():
            formFinal = form.save(commit=False)
            formFinal.entreprisePassword = make_password(formFinal.entreprisePassword)
            request.session['entrepriseName'] = formFinal.entrepriseName
            formFinal.save()
            return redirect('HomeE')
    else:
        form = EntrepriseForm()
    return render(request, 'polls/PersonSignup.html', {'form': form})

def Personal_Informations(request):
    if not sessionValidePersonne(request):
        return redirect('PersonSignup')
    if request.method == 'POST':
        try:
            informationsPerson = PersonalInformations.objects.get(sinNumberPersonne=request.session['SIN_Number'])
            informationsPerson.adress = request.POST['adress']
            informationsPerson.postalCode = request.POST['postalCode']
            informationsPerson.sexe = request.POST['sexe']
            informationsPerson.personEmail = request.POST['personEmail']
            informationsPerson.phone = request.POST['phone']
            informationsPerson.save()
            return redirect('HomeP')
        except PersonalInformations.DoesNotExist:
            data = {
                'adress': request.POST['adress'],
                'postalCode': request.POST['postalCode'],
                'sexe': request.POST['sexe'],
                'personEmail': request.POST['personEmail'],
                'phone': request.POST['phone'],
                'sinNumberPersonne': request.session['SIN_Number'],
            }

            form = PersonalInformationsForm(data)
            if form.is_valid():
                form.save()
                return redirect('Cv')
    else:
        form = PersonalInformationsForm()
        try:
            personLogger = PersonalInformations.objects.get(sinNumberPersonne=request.session['SIN_Number'])
            form.fields['adress'].initial = personLogger.adress
            form.fields['postalCode'].initial = personLogger.postalCode
            form.fields['personEmail'].initial = personLogger.personEmail
            form.fields['phone'].initial = personLogger.phone
        except PersonalInformations.DoesNotExist:
            personLogger = None
    return render(request, 'polls/Personal_Informations.html', {'form': form})

def Cv(request):
    if not sessionValidePersonne(request):
        return redirect('PersonSignup')
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        deleteCvExistant(fs, request)
        if myfile.name.endswith('.docx'):
            filename = fs.save('Cvs/'+request.session['SIN_Number']+".docx", myfile)
        elif myfile.name.endswith('.pdf'):
            filename = fs.save('Cvs/'+request.session['SIN_Number']+".pdf", myfile)
        else:
            errorMessage = 'The document is not compatible'
            return render(request, 'polls/Cv.html', {'errorMessage': errorMessage})
        return render(request, 'polls/HomeP.html')
    return render(request, 'polls/Cv.html')

def PersonLogin(request):
    if request.method == 'POST':
        try:
            personLogin = Person.objects.get(SIN_Number=request.POST['SIN_Number'])
        except Person.DoesNotExist:
            return redirect('PersonLogin')
        if check_password(request.POST['Person_Password'], personLogin.Person_Password):
            request.session['SIN_Number'] = personLogin.SIN_Number
            return redirect('HomeP')
    return render(request, 'polls/PersonLogin.html')

def EntrepriseLogin(request):
    if request.method == 'POST':
        try:
            entreprise = Entreprise.objects.get(entrepriseName=request.POST['entrepriseName'])
        except Entreprise.DoesNotExist:
            return redirect('EntrepriseLogin')
        if check_password(request.POST['entreprisePassword'], entreprise.entreprisePassword):
            request.session['entrepriseName'] = entreprise.entrepriseName
            return redirect('HomeE')
    return render(request, 'polls/EntrepriseLogin.html')

def sessionValidePersonne(request):
    if 'SIN_Number' not in request.session:
        return False
    return True

def sessionValideEntreprise(request):
    if 'entrepriseName' not in request.session:
        return False
    return True

def deleteCvExistant(fs, request):
    cvExistantDoc = Path('Cvs/'+request.session['SIN_Number']+".docx")
    cvExistantPdf = Path('Cvs/'+request.session['SIN_Number']+".pdf")
    if cvExistantPdf.exists():
        fs.delete(cvExistantPdf)
    elif cvExistantDoc.exists():
        fs.delete(cvExistantDoc)

def Logout(request):
    if 'entrepriseName' in request.session:
        del request.session['entrepriseName']
        return redirect('EntrepriseLogin')
    elif 'SIN_Number' in request.session:
        del request.session['SIN_Number']
        return redirect('PersonLogin')
