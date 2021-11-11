from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
import datetime as dt
from .models import *
# Create your views here.
from .functions import *
from django.db.models import Max
import random as r
from IA.xray import *   
from django.db.models.signals import pre_save , post_save
from django.dispatch import receiver
from rest_framework import status as s

class Paises(generics.ListAPIView):
    queryset = Pais.objects.all()

    def list(self, request):
        
        queryset = self.get_queryset()
        serializer = PaisesSerializer(queryset, many=True)
        return Response(serializer.data)
    
    
    
class Provincias(generics.ListAPIView):
    queryset = Provincia.objects.all()
    
    def list(self, request):
        
        queryset = self.get_queryset()
        serializer = ProvinciasSerializer(queryset, many=True)
        return Response(serializer.data)
    
    
class ABMPacientes(APIView):
    queryset = Paciente.objects.all()
    
    
    
    def get(self,request):
        
        numero_afiliado=self.request.query_params.get('paciente',None)
    
        pacientes=Paciente.objects.all()
        
        if numero_afiliado is None:
            serializer = PacienteSerializer(pacientes, many=True)
            
            response={'status':200 , 'message':serializer.data}
            
            
        else:
            
            pac=pacientes.filter(numero_afiliado=numero_afiliado)
            
            
            
            if pac.count() > 0:
            
                serializer=PacienteSerializer(pac[0])
                
                response={'status':200 , 'paciente':serializer.data}
                
            else:
                response={'status':404,'message':'No se encontro el paciente'}

        
        return Response(response)
    
    
    def post(self,request):
        
            
        try:   
            serializer=ABMPacienteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            datos=serializer.validated_data
            
            nombre=datos.get('nombre')
            dni=datos.get('dni')
            email=datos.get('email')
            apellido=datos.get('apellido')
        
            telefono=datos.get('telefono')
            #numero_afiliado=datos.get('numero_matricula')
            
            fecha_alta=dt.date.today()
            
            # f=datos.get('fecha_nacimiento')
            # fecha_nac=dt.datetime.strptime(f , '%Y-%m-%d')
            fecha_nac=datos.get('fecha_nacimiento')
            
            # pais=datos.get('pais')
            # prov=datos.get('provincia')
        
            loc=datos.get('localidad').upper()
            
            #codigo_postal=datos.get('codigo_postal')
            direccion=datos.get('direccion')
            entre_calle_sup=datos.get('entre_calle_sup')
            entre_calle_inf=datos.get('entre_calle_inf')
            fecha_desde=datos.get('fecha_desde')
            
            aux=r.randint(1,int(dni))
            num=str(aux)
            num_afiliado='{}{}{}{}{}{}'.format(dni[:4] , fecha_nac.year , fecha_nac.month , fecha_nac.day , num[0] , num[-1])
            #crear domicilio
            domicilio=Domicilio(
                entre_calle_sup=entre_calle_sup,
                entre_calle_inf=entre_calle_inf,
                direccion=direccion,
                fecha_desde=fecha_desde,
                localidad=Localidad.objects.get(nombre=loc),

            )
            domicilio.save()
            
            dom=Domicilio.objects.get(pk=domicilio.pk)
            #crear medico
            paciente=Paciente(
                nombre=nombre,
                dni=dni,
                email=email,
                apellido=apellido,
                fecha_nacimiento=fecha_nac,
                telefono=telefono,
                numero_afiliado=num_afiliado,
                fecha_alta=fecha_alta,
            
            )
            paciente.save()
            paciente.domicilio.add(dom)
            paciente.save()
            
            response={'status':'200','message':'Se creo un paciente'}
                
            
        except Exception as e:
            
            response={'status':'500','message':str(e)}
            
        return Response(response)
 
 
    def delete(self,request):
        numero_afiliado=self.request.query_params.get('numero_afiliado')
        paciente=Paciente.objects.get(numero_afiliado=numero_afiliado).delete()
        
        return Response({'status':200,'message':'Paciente con numero_afiliado {} eliminado'.format(numero_afiliado)})
    
    
    
class Localidades(generics.ListAPIView):
    queryset = Localidad.objects.all()
    
    def list(self, request):
        
        queryset = self.get_queryset()
        serializer = LocalidadesSerializer(queryset, many=True)
        return Response(serializer.data)
       

class SubirRadiografia(APIView):

    def post(self,request):
        
        serializer=SubirRadiografiaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        datos=serializer.validated_data
        
        num_af=datos.get('numero_afiliado')
        paciente=Paciente.objects.get(numero_afiliado=num_af)
        
        
        
        
        ultimo_estudio=Radiografia.objects.all().aggregate(Max('id'))
        codigo_estudio=generar_codigo(paciente) + str(ultimo_estudio['id__max'])
        
        f=datos.get('fecha')
        fecha=dt.datetime.strptime(f , '%Y-%m-%d')
        
        nueva_radiografia=Radiografia(
            estudio=datos.get('estudio'),
            codigo_estudio=codigo_estudio,
            fecha = fecha,
            radiologo = Radiologo.objects.get(numero_matricula=datos.get('matricula_radiologo')),
            placa=datos.get('radiografia'),
            descripcion = datos.get('descripcion'),
            paciente = paciente,
            medico = Medico.objects.get(numero_matricula=datos.get('matricula_medico')),
            
        )
        nueva_radiografia.save()

        return Response({'status':'recursada'})
    
    
    def delete(self,request):
        
        id=request.query_params.get('id')
        radiografia=Radiografia.objects.filter(pk=int(id)).first()
        
        if radiografia:
            radiografia.delete()
            response={'status':200,'message':'radiografia eliminada'}
        else:
            response={'status':400,'message':'No existe una radiografia con el id {}'.format(id)}
            
        return Response(response)
            
        
        

class RadiografiasPorMedico(generics.ListAPIView):
    queryset = Radiografia.objects.all()

    def get(self, request,**kwargs):
        
        
        paciente=self.request.query_params.get('numero_afiliado')
        medico=self.request.query_params.get('matricula_medico')
        
        
        radiografias = self.get_queryset()
        filtradas=radiografias.filter(medico__numero_matricula=int(medico) , paciente__numero_afiliado=paciente)
        
        serializer = RadiografiasSerializer(filtradas, many=True)
        return Response(serializer.data)       

class ResultadoRadiografia(APIView):
    
    def get(self,request):
        
        
        resultado=diagnostico()
        
        return Response({'recursada':resultado})

class ABMRadiologos(APIView):
    
    
    def post(self, request):
        
        try:
        
            serializer=ABMRadiologoSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            datos=serializer.validated_data
            
            nombre=datos.get('nombre')
            dni=datos.get('dni')
            email=datos.get('email')
            apellido=datos.get('apellido')
            fecha_nac=datos.get('fecha_nacimiento')
            telefono=datos.get('telefono')
            numero_matricula=datos.get('numero_matricula')
            legajo=datos.get('legajo')
            fecha_alta=dt.date.today()
            
            
            # pais=datos.get('pais')
            # prov=datos.get('provincia')
        
            loc=datos.get('localidad').upper()
            
            #codigo_postal=datos.get('codigo_postal')
            direccion=datos.get('direccion')
            entre_calle_sup=datos.get('entre_calle_sup')
            entre_calle_inf=datos.get('entre_calle_inf')
            fecha_desde=datos.get('fecha_desde')
            
            
            
            #crear domicilio
            domicilio=Domicilio(
                entre_calle_sup=entre_calle_sup,
                entre_calle_inf=entre_calle_inf,
                direccion=direccion,
                fecha_desde=fecha_desde,
                localidad=Localidad.objects.get(nombre=loc),

            )
            domicilio.save()
            
            dom=Domicilio.objects.get(pk=domicilio.pk)
            #crear medico
            radiologo=Radiologo(
                nombre=nombre,
                dni=dni,
                email=email,
                apellido=apellido,
                fecha_nacimiento=fecha_nac,
                telefono=telefono,
                numero_matricula=numero_matricula,
                legajo=legajo,
                fecha_alta=fecha_alta,
            
            )
            radiologo.save()
            radiologo.domicilio.add(dom)
            radiologo.save()
            
            response={'status':'200','message':'Se creo un radiologo'}
            
            
        except Exception as e:
            
            response={'status':'500','message':str(e)}
            
        return Response(response)
        
    
    def delete(self,request):
        matricula=self.request.query_params.get('matricula')
        
    
        radiologo=Radiologo.objects.filter(numero_matricula=matricula).first()
        
        if radiologo:
            radiologo.delete()
            response={'status':200,'message':'Radiologo con matricula {} eliminado'.format(matricula)}
        else:
            response={'status':400,'message':'No se encontro radiologo con matricula {}'.format(matricula)}
        
        return Response(response)
    
    def get(self,request):
        
        matricula=request.query_params.get('numero_matricula',None)
        
        radiologos=Radiologo.objects.all()
        
        if matricula is None:

            serializer=RadiologosSerializer(radiologos,many=True)
            response=serializer.data
        
        else:
            radiologo=radiologos.filter(numero_matricula=int(matricula))
            
            
            if radiologo.count() > 0:
            
                serializer=RadiologosSerializer(radiologo[0])
                response=serializer.data
            else:
                response={'message':'No se encontro un radiologo con ese numero de matricula'}

        return Response(response)


class MedicoABM(APIView):
    
    
    serializer_class=ABMMedicoSerializer
    
    def get(self,request):
        
        matricula=self.request.query_params.get('matricula',None)
        
        
        medicos=Medico.objects.all()
        
        
        if matricula is None:
            serializer = MedicoSerializer(medicos, many=True)
            
            response={'status':200 , 'medicos':serializer.data}
            
            
        else:
            
            medico=medicos.filter(numero_matricula=matricula)
            
            
            
            if medico.count() > 0:
            
                serializer=MedicoSerializer(medico[0])
                
                response={'status':200 , 'medico':serializer.data}
                
            else:
                response={'status':404,'message':'No se encontro el medico'}

        
        return Response(response)
        
   
    def delete(self,request):
        matricula=self.request.query_params.get('matricula')
        medico=Medico.objects.filter(numero_matricula=matricula).first()
        
        if medico:
            medico.delete()
            response={'status':200,'message':'Medico con matricula {} eliminado'.format(matricula)}
        else:
            response={'status':400,'message':'No existe un medico con matricula {}'.format(matricula)}
        
        return Response(response)
        
    def post(self, request):
        
        try:
        
            serializer=ABMMedicoSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            datos=serializer.validated_data
            
            nombre=datos.get('nombre')
            dni=datos.get('dni')
            email=datos.get('email')
            apellido=datos.get('apellido')
            fecha_nac=datos.get('fecha_nacimiento')
            telefono=datos.get('telefono')
            numero_matricula=datos.get('numero_matricula')
            legajo=datos.get('legajo')
            fecha_alta=dt.date.today()
            
            
            # pais=datos.get('pais')
            # prov=datos.get('provincia')
        
            loc=datos.get('localidad').upper()
            
            #codigo_postal=datos.get('codigo_postal')
            direccion=datos.get('direccion')
            entre_calle_sup=datos.get('entre_calle_sup')
            entre_calle_inf=datos.get('entre_calle_inf')
            fecha_desde=datos.get('fecha_desde')
            
            
            
            #crear domicilio
            domicilio=Domicilio(
                entre_calle_sup=entre_calle_sup,
                entre_calle_inf=entre_calle_inf,
                direccion=direccion,
                fecha_desde=fecha_desde,
                localidad=Localidad.objects.get(nombre=loc),

            )
            domicilio.save()
            
            dom=Domicilio.objects.get(pk=domicilio.pk)
            #crear medico
            medico=Medico(
                nombre=nombre,
                dni=dni,
                email=email,
                apellido=apellido,
                fecha_nacimiento=fecha_nac,
                telefono=telefono,
                numero_matricula=numero_matricula,
                legajo=legajo,
                fecha_alta=fecha_alta,
            
            )
            medico.save()
            medico.domicilio.add(dom)
            medico.save()
            
            response={'status':'200','message':'Se creo un medico'}
            
            
        except Exception as e:
            
            response={'status':'500','message':str(e)}
            
        return Response(response)
    
    
class MedicoUpdate(generics.UpdateAPIView):
    serializer_class=MedicoSerializer
    
    def get_queryset(self,pk):
        return self.get_serializer().Meta.model.objects.all().filter(id=pk).first()
    

    def put(self,request,pk=None):
        queryset=self.get_queryset(pk)
        if queryset:
            medico_serializer=self.serializer_class(queryset,data=request.data)
            
            if medico_serializer.is_valid():
                medico_serializer.save()
                response=medico_serializer.data
                st=s.HTTP_200_OK
                
            else:
                response=medico_serializer.errors
                st=s.HTTP_500_INTERNAL_SERVER_ERROR
                
            return Response(response,st)
        
class PacienteUpdate(generics.UpdateAPIView):
    serializer_class=PacienteSerializer
    
    def get_queryset(self,pk):
        return self.get_serializer().Meta.model.objects.all().filter(id=pk).first()
    

    def put(self,request,pk=None):
        queryset=self.get_queryset(pk)
        if queryset:
            medico_serializer=self.serializer_class(queryset,data=request.data)
            
            if medico_serializer.is_valid():
                medico_serializer.save()
                response=medico_serializer.data
                st=s.HTTP_200_OK
                
            else:
                response=medico_serializer.errors
                st=s.HTTP_500_INTERNAL_SERVER_ERROR
                
            return Response(response,st)


class RadiologoUpdate(generics.UpdateAPIView):
    serializer_class=RadiologosSerializer
    
    def get_queryset(self,pk):
        return self.get_serializer().Meta.model.objects.all().filter(id=pk).first()
    

    def put(self,request,pk=None):
        queryset=self.get_queryset(pk)
        if queryset:
            medico_serializer=self.serializer_class(queryset,data=request.data)
            
            if medico_serializer.is_valid():
                medico_serializer.save()
                response=medico_serializer.data
                st=s.HTTP_200_OK
                
            else:
                response=medico_serializer.errors
                st=s.HTTP_500_INTERNAL_SERVER_ERROR
                
            return Response(response,st)     


class SecretarioUpdate(generics.UpdateAPIView):
    serializer_class=SecretarioSerializer
    
    def get_queryset(self,pk):
        return self.get_serializer().Meta.model.objects.all().filter(id=pk).first()
    

    def put(self,request,pk=None):
        queryset=self.get_queryset(pk)
        if queryset:
            secretario_serializer=self.serializer_class(queryset,data=request.data)
            
            if secretario_serializer.is_valid():
                secretario_serializer.save()
                response=secretario_serializer.data
                st=s.HTTP_200_OK
                
            else:
                response=secretario_serializer.errors
                st=s.HTTP_500_INTERNAL_SERVER_ERROR
                
            return Response(response,st)        
        
        
class DiagnosticoPaciente(APIView):
    
    
    def get(self,request):
        
        
        num_afiliado=request.query_params.get('numero_afiliado')
        id_rad=request.query_params.get('id_diagnostico')
        
    
        diagnostico=Diagnostico.objects.get(radiografia__id=int(id_rad),radiografia__paciente__numero_afiliado=num_afiliado)
        
        serializer=DiagnosticoSerializer(diagnostico)
        
        return Response(serializer.data)   
    
    
    
class ABMSecretarios(APIView):
    serializer_class=ABMSecretarioSerializer
    
    def get(self,request):
        
        legajo=self.request.query_params.get('legajo',None)
        
        
        secretarios=Secretario.objects.all()
        
        
        if legajo is None:
            serializer = SecretarioSerializer(secretarios, many=True)
            
            response={'status':200 , 'secretarios':serializer.data}
            
            
        else:
            
            secretario=secretarios.filter(legajo=legajo)
            
            
            
            if secretario.count() > 0:
            
                serializer=SecretarioSerializer(secretario.first())
                
                response={'status':200 , 'secretario':serializer.data}
                
            else:
                response={'status':404,'message':'No se encontro el secretario'}

        
        return Response(response)
        
   
    def delete(self,request):
        legajo=self.request.query_params.get('legajo')

        secret=Secretario.objects.filter(legajo=legajo).first()
        
        if secret:
            secret.delete()
            response={'status':200,'message':'Secretario con legajo {} eliminado'.format(legajo)}
        else:
            response={'status':400,'message':'No existe el secretario con legajo {}'.format(legajo)}
        return Response(response)
    
    
    def post(self, request):
        
        try:
        
            serializer=ABMSecretarioSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            datos=serializer.validated_data
            
            nombre=datos.get('nombre')
            dni=datos.get('dni')
            email=datos.get('email')
            apellido=datos.get('apellido')
            fecha_nac=datos.get('fecha_nacimiento')
            telefono=datos.get('telefono')
            
            legajo=datos.get('legajo')
            fecha_alta=dt.date.today()
            
            
            # pais=datos.get('pais')
            # prov=datos.get('provincia')
        
            loc=datos.get('localidad').upper()
            
            #codigo_postal=datos.get('codigo_postal')
            direccion=datos.get('direccion')
            entre_calle_sup=datos.get('entre_calle_sup')
            entre_calle_inf=datos.get('entre_calle_inf')
            fecha_desde=datos.get('fecha_desde')
            
            
            
            #crear domicilio
            domicilio=Domicilio(
                entre_calle_sup=entre_calle_sup,
                entre_calle_inf=entre_calle_inf,
                direccion=direccion,
                fecha_desde=fecha_desde,
                localidad=Localidad.objects.get(nombre=loc),

            )
            domicilio.save()
            
            dom=Domicilio.objects.get(pk=domicilio.pk)
            #crear medico
            sec=Secretario(
                nombre=nombre,
                dni=dni,
                email=email,
                apellido=apellido,
                fecha_nacimiento=fecha_nac,
                telefono=telefono,
                legajo=legajo,
                fecha_alta=fecha_alta,
            
            )
            sec.save()
            sec.domicilio.add(dom)
            sec.save()
            
            response={'status':'200','message':'Se creo un secretario'}
            
            
        except Exception as e:
            
            response={'status':'500','message':str(e)}
            
        return Response(response)
    
    
@receiver(post_save, sender=Radiografia)


def procesar_radiografia(sender, **kwargs):
    
    instancia=kwargs['instance']
    path=instancia.placa.url
    resultado=diagnostico(path) 
    
    
    diag=Diagnostico.objects.create(
        resultado=resultado,
        fecha=dt.date.today(),
        radiografia=instancia,
    )
    