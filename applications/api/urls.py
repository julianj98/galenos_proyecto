from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import *









urlpatterns=[
    path('altamedico' ,MedicoABM.as_view() , name='alta_medico'),
    path('modificarmedico/<pk>' ,MedicoUpdate.as_view() , name='modificar_medico'),
    path('modificarsecretario/<pk>' ,SecretarioUpdate.as_view() , name='modificar_secretario'),
    path('modificarpaciente/<pk>' ,PacienteUpdate.as_view() , name='modificar_paciente'),
    path('modificaradiologo/<pk>' ,RadiologoUpdate.as_view() , name='modificar_radiologo'),
    path('paises' ,Paises.as_view() , name='paises'),
    path('altapaciente' ,ABMPacientes.as_view() , name='pacientes'),
    path('altasecretario' ,ABMSecretarios.as_view() , name='secretarios'),
    path('subiradiografia' ,SubirRadiografia.as_view() , name='subir-radiografia'),
    path('radiologos' ,ABMRadiologos.as_view() , name='radiologos'),
    path('resultado' ,ResultadoRadiografia.as_view() , name='resultado'),
    path('radiografias' ,RadiografiasPorMedico.as_view() , name='radiografias'),
    path('diagnostico' ,DiagnosticoPaciente.as_view() , name='diagnostico'),
  

]