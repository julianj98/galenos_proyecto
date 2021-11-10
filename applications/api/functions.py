
import string as s

def generar_codigo(paciente):
    dni=str(paciente.dni)
    
    abecedario=s.ascii_lowercase
    
    digitos=dni[:4]
    
    codigo=''
    for n in digitos:
        letra=abecedario[int(n)]
        codigo = codigo + letra
        
    n=paciente.nombre
    a=paciente.apellido
    
    return codigo + digitos + n[0] + a[0]