from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import *









urlpatterns=[
    path('altamedico' ,MedicoABM.as_view() , name='alta_medico'),
    path('paises' ,Paises.as_view() , name='paises'),
    path('altapaciente' ,ABMPacientes.as_view() , name='pacientes'),
    path('subiradiografia' ,SubirRadiografia.as_view() , name='subir-radiografia'),
    path('radiologos' ,Radiologos.as_view() , name='radiologos'),
    path('resultado' ,ResultadoRadiografia.as_view() , name='resultado'),
    path('radiografias' ,RadiografiasPorMedico.as_view() , name='radiografias'),
    path('diagnostico' ,DiagnosticoPaciente.as_view() , name='diagnostico'),
  

]