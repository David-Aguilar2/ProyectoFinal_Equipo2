#Importamos el modulo 'models' de Django que nos permite definir estructuras de DB.
from django.db import models

#Modelo Usuario
class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True) #llave Primaria para identificar el usuario.
    correo = models.CharField(max_length=100) #Alcamenar el correo del usuario.
    contrasenia = models.CharField(max_length=50)#Almacena la contraseña.

    def __str__(self): #Devuelve una representacion en cadena del objeto Usuario.
        return self.correo

#Modelo Administrador
class Administrador(models.Model):
    id_administrador = models.AutoField(primary_key=True) #Llave Primaria 
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE) #Llave foranea 
    nombres = models.CharField(max_length=50) #Campos para almacenar los datos personales.
    apellidos = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15)

    def __str__(self): #Retorna el nombre completo del administrador.
        return f"{self.nombres} {self.apellidos}"

#Modelo Paciente
class Paciente(models.Model):
    id_paciente = models.AutoField(primary_key=True) #Llave Primaria.
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE) #Llave Foranea.
    nombres = models.CharField(max_length=50) #Campos para alamacenar los datos.
    apellidos = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15)

    def __str__(self): #Retorna el nombre completo del paciente.
        return f"{self.nombres} {self.apellidos}"

#Modelo Especialidad
class Especialidad(models.Model):
    id_especialidad = models.AutoField(primary_key=True) #Llave Primaria.
    nombre_especialidad = models.CharField(max_length=100) #Nombre de la especialidad.
    descripcion = models.CharField(max_length=600)#Descripcion breve de la especialidad.

    def __str__(self): #Devuelve el nombre de la especialidad.
        return self.nombre_especialidad

#Modelo Medico
class Medico(models.Model):
    id_medico = models.AutoField(primary_key=True) #llave Primaria.
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE) #Llave foranea.
    nombres = models.CharField(max_length=50) #Campos personales del medico.
    apellidos = models.CharField(max_length=50)
    id_especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15)

    def __str__(self): #Retorna el nombre completo del medico 'Dr. Nombre Apellido'.
        return f"Dr. {self.nombres} {self.apellidos}"

#Modelo Cita
class Cita(models.Model):
    id_cita = models.AutoField(primary_key=True) #Llave Primaria.
    id_paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE) #Llave Foranea.
    id_medico = models.ForeignKey(Medico, on_delete=models.CASCADE)#Medico asignado a la cita.
    motivo_consulta = models.CharField(max_length=500) #Motivo de la consulta.
    fecha_cita = models.DateTimeField() #Fecha y hora de la cita

    def __str__(self): #Retorna una representacion en cadena de la cita.
        return f"Cita {self.id_cita} - {self.id_paciente.nombres}"
