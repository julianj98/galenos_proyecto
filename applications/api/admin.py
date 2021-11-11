from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Domicilio)
admin.site.register(Localidad)
admin.site.register(Pais)
admin.site.register(Provincia)
admin.site.register(Medico)
admin.site.register(Paciente)
admin.site.register(Radiologo)
admin.site.register(Radiografia)
admin.site.register(Diagnostico)
admin.site.register(Secretario)