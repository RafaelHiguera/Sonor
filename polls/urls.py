from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^PersonHomepage/$', views.PersonHomepage, name='PersonHomepage'),
    url(r'^PersonHomepage/PersonSignup/$', views.PersonSignup, name='PersonSignup'),
    url(r'^PersonHomepage/PersonLogin/$', views.PersonLogin, name='PersonLogin'),
    url(r'^PersonHomepage/Personal_Informations/$', views.Personal_Informations, name='Personal_Informations'),
    url(r'^PersonHomepage/Cv/$', views.Cv, name='Cv'),
    url(r'^PersonHomepage/HomeP/$', views.HomeP, name='HomeP'),
    url(r'^PersonHomepage/Logout/$', views.Logout, name='Logout'),
    url(r'^PersonHomepage/RequestForEntreprise/$', views.RequestForEntreprise, name='RequestForEntreprise'),
    url(r'^PersonHomepage/requests/$', views.RequestsDispachter, name='RequestsDispachter'),
    url(r'^EntrepriseHomepage/$', views.EntrepriseHomepage, name='EntrepriseHomepage'),
    url(r'^EntrepriseHomepage/EntrepriseSignup/$', views.EntrepriseSignup, name='EntrepriseSignup'),
    url(r'^EntrepriseHomepage/HomeE/$', views.HomeE, name='HomeE'),
    url(r'^EntrepriseHomepage/EntrepriseLogin/$', views.EntrepriseLogin, name='EntrepriseLogin'),
    url(r'^EntrepriseHomepage/PersonRequest/$', views.PersonRequest, name='PersonRequest'),
]
