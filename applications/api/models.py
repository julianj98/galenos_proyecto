from django.db import models

#from IA.xray import *   
from django.db.models.signals import pre_save , post_save
from django.dispatch import receiver


class Pais(models.Model):
    nombre=models.CharField(max_length=30)
    
    
    def __str__(self):
        
        return self.nombre

class Provincia(models.Model):
    nombre=models.CharField(max_length=30)
    pais=models.ForeignKey(Pais , on_delete=models.CASCADE)
    
    def __str__(self):
        
        return self.nombre


class Localidad(models.Model):
    nombre=models.CharField(max_length=30)
    codigo_postal=models.CharField(max_length=5)
    provincia=models.ForeignKey(Provincia , on_delete=models.CASCADE)
    
    def __str__(self):
        
        return self.nombre


class Domicilio(models.Model):
    direccion=models.CharField(max_length=30)
    entre_calle_sup=models.CharField(max_length=30)
    entre_calle_inf=models.CharField(max_length=30)
    fecha_desde=models.DateField()
    fecha_hasta=models.DateField(blank=True,null=True)
    localidad=models.ForeignKey(Localidad , on_delete=models.CASCADE)
    
    def __str__(self):
        
        return self.direccion

    
class Persona(models.Model):
    dni=models.CharField(max_length=13,unique=True)
    email=models.EmailField(max_length=254)
    nombre=models.CharField(max_length=20)
    apellido=models.CharField(max_length=20)
    #domicilio=models.CharField(max_length=30) 
    telefono=models.IntegerField()
    fecha_nacimiento=models.DateField(blank=True,null=True)
    fecha_alta = models.DateField(blank=True,null=True)
    foto=models.ImageField(blank=True,null=True)
    domicilio=models.ManyToManyField(Domicilio)
    
    
    class Meta:
        abstract = True
        
        
class Medico(Persona):
    numero_matricula=models.IntegerField(unique=True) 
    legajo = models.IntegerField(unique=True)
    
    
    def __str__(self):
        return self.nombre
    
    
class Paciente(Persona):
    numero_afiliado=models.CharField(unique=True,max_length=20) 
    
    def __str__(self):
        return self.nombre    
    
   
class Radiologo(Persona):
    legajo=models.IntegerField(unique=True) 
    numero_matricula=models.IntegerField(blank=True,null=True,unique=True) 
    
    
    def __str__(self):
        return self.nombre
    
   
class Secretario(Persona):
    legajo=models.IntegerField(unique=True) 
    
    def __str__(self):
        return self.nombre
    
 

class Radiografia(models.Model):
    estudio=models.CharField(max_length=100,default='Radiografia de torax')
    codigo_estudio=models.CharField(max_length=15 , blank=True,null=True ,unique=True)
    fecha = models.DateField()
    radiologo = models.ForeignKey(Radiologo, on_delete=models.CASCADE)
    placa=models.ImageField()
    descripcion = models.CharField(max_length=100)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, blank=True,null=True)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, blank=True,null=True)
    
    
    def __str__(self):
    
        return self.radiologo.nombre + '-' + self.paciente.nombre + str(self.id)
    
    class Meta:
        
        ordering=['-fecha',]
  
resultados = [
    ('COVID', 'COVID'),
    ('NORMAL', 'NORMAL'),
    ('NEUMONIA', 'NEUMONIA'),

]
  
class Diagnostico(models.Model):
    fecha = models.DateTimeField()
    resultado=models.CharField(max_length=15 , default='NORMAL',choices=resultados)
    radiografia=models.ForeignKey(Radiografia, on_delete=models.CASCADE, blank=True,null=True)

    def __str__(self):
        return self.resultado   
    
    class Meta:
        verbose_name = 'Resultado'

   


