from rest_framework import serializers as s
from .models import *


class SubirRadiografiaSerializer(s.Serializer):
    estudio=s.CharField()
    #codigo_estudio=s.CharField()
    fecha = s.CharField()
    matricula_radiologo = s.IntegerField()
    radiografia=s.ImageField()
    descripcion = s.CharField()
    numero_afiliado = s.IntegerField()
    matricula_medico= s.IntegerField()

class RadiografiasSerializer(s.ModelSerializer):
    class Meta:
        model=Radiografia
        fields='__all__'   

class PacienteSerializer(s.ModelSerializer):
    class Meta:
        model=Paciente
        #fields='__all__'
        exclude=('domicilio',)

class ProvinciasSerializer(s.ModelSerializer):
    
    class Meta:
        model=Provincia
        fields='__all__'

class LocalidadesSerializer(s.ModelSerializer):
    
    class Meta:
        model=Localidad
        fields='__all__'

class PaisesSerializer(s.ModelSerializer):
    
    class Meta:
        model=Pais
        fields='__all__'

class SecretarioSerializer(s.ModelSerializer):
     class Meta:
        model=Secretario
        exclude=('domicilio',)

class MedicoSerializer(s.ModelSerializer):
    
    class Meta:
        model=Medico
        #fields='__all__'
        exclude=('domicilio',)
        
class RadiologosSerializer(s.ModelSerializer):
    
    class Meta:
        model=Radiologo
        #fields='__all__'
        exclude=('domicilio',)
        
class SecretarioSerializer(s.ModelSerializer):
    
    class Meta:
        model=Secretario
        #fields='__all__'
        exclude=('domicilio',)

class ABMSecretarioSerializer(s.Serializer):
    dni=s.CharField(required=True)
    email=s.EmailField(required=True)
    nombre=s.CharField(required=True)
    apellido=s.CharField(required=True)
    #domicilio=s.CharField(required=True) 
    telefono=s.IntegerField(required=True)
    fecha_alta = s.DateField(required=False)
    fecha_nacimiento=s.DateField(required=True)
    foto=s.ImageField(required=False)

    direccion=s.CharField(required=True)
    entre_calle_sup=s.CharField(required=True)
    entre_calle_inf=s.CharField(required=True)
    fecha_desde=s.DateField(required=True)
    
    fecha_hasta=s.DateField(required=False)
    
    localidad=s.CharField(required=True)
    legajo=s.IntegerField(required=True)

class ABMMedicoSerializer(s.Serializer):
    dni=s.CharField(required=True)
    email=s.EmailField(required=True)
    nombre=s.CharField(required=True)
    apellido=s.CharField(required=True)
    #domicilio=s.CharField(required=True) 
    telefono=s.IntegerField(required=True)
    fecha_alta = s.DateField(required=False)
    fecha_nacimiento=s.DateField(required=True)
    
    foto=s.ImageField(required=False)
    
    numero_matricula=s.IntegerField(required=True) 
    direccion=s.CharField(required=True)
    entre_calle_sup=s.CharField(required=True)
    entre_calle_inf=s.CharField(required=True)
    fecha_desde=s.DateField(required=True)
    
    fecha_hasta=s.DateField(required=False)
    
    localidad=s.CharField(required=True)
    # codigo_postal=s.CharField(required=True)
    # provincia=s.CharField(required=True)
    # pais=s.CharField(required=True)
    legajo=s.IntegerField(required=True)
    
    
class ABMPacienteSerializer(s.Serializer):
    dni=s.CharField(required=True)
    email=s.EmailField(required=True)
    nombre=s.CharField(required=True)
    apellido=s.CharField(required=True)
    #domicilio=s.CharField(required=True) 
    telefono=s.IntegerField(required=True)
    fecha_alta = s.DateField(required=False)
    fecha_nacimiento=s.DateField(required=True)

    
    foto=s.ImageField(required=False)
    
    
    direccion=s.CharField(required=True)
    entre_calle_sup=s.CharField(required=True)
    entre_calle_inf=s.CharField(required=True)
    fecha_desde=s.DateField(required=True)
    
    fecha_hasta=s.DateField(required=False)
    
    localidad=s.CharField(required=True)
    # codigo_postal=s.CharField(required=True)
    # provincia=s.CharField(required=True)
    # pais=s.CharField(required=True)
    
class ABMRadiologoSerializer(s.Serializer):
    dni=s.CharField(required=True)
    email=s.EmailField(required=True)
    nombre=s.CharField(required=True)
    apellido=s.CharField(required=True)
    #domicilio=s.CharField(required=True) 
    telefono=s.IntegerField(required=True)
    fecha_alta = s.DateField(required=False)
    fecha_nacimiento=s.DateField(required=True)
    
    foto=s.ImageField(required=False)
    
    numero_matricula=s.IntegerField(required=True) 
    direccion=s.CharField(required=True)
    entre_calle_sup=s.CharField(required=True)
    entre_calle_inf=s.CharField(required=True)
    fecha_desde=s.DateField(required=True)
    
    fecha_hasta=s.DateField(required=False)
    
    localidad=s.CharField(required=True)
    # codigo_postal=s.CharField(required=True)
    # provincia=s.CharField(required=True)
    # pais=s.CharField(required=True)
    legajo=s.IntegerField(required=True)
#class PersonaSerializer()

class RadiografiaDiagnosticoSerializer(s.ModelSerializer):
    medico=s.SerializerMethodField()
    paciente=s.SerializerMethodField()
    radiologo=s.SerializerMethodField()
    
    class Meta:
        model=Radiografia
        fields=('estudio','codigo_estudio','fecha','medico','paciente','descripcion','placa','radiologo','placa')
    
    def get_paciente(self,obj):
        
        paciente=Paciente.objects.get(dni=obj.paciente.dni)
        serializer=PacienteSerializer(paciente)
        
        return serializer.data
        
        
    def get_medico(self,obj):
        
        medico=Medico.objects.get(dni=obj.medico.dni)
        serializer=MedicoSerializer(medico)
        
        return serializer.data
    
    
    def get_radiologo(self,obj):
        
        radiologo=Radiologo.objects.get(dni=obj.radiologo.dni)
        serializer=RadiologosSerializer(radiologo)
        
        return serializer.data
    
class DiagnosticoSerializer(s.ModelSerializer):
    radiografia=RadiografiaDiagnosticoSerializer()
    
    
    class Meta:
        model=Diagnostico
        fields=('fecha','resultado','radiografia')
        
    def get_radiografia(self,obj):
        
        rad=Radiografia.objects.get(pk=obj.radiografia.id)
        serializer=RadiografiasSerializer(rad)
        
        return serializer.data
    
    