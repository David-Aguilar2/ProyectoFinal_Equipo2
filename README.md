# ProyectoFinal_Equipo2
Repositorio oficial del proyecto final del equipo 2, curso Desarrollo de Software Empresarial.

David Alexander Aguilar Barrientos:	David-Aguilar2
Gabriela de los Angeles Chacón Guevara:	GabrielaChacon
María Guadalupe Canjura Díaz:	guadalupe-a11y
Mallerli Yamileth Ventura Escobar:	yamileth30-escobar
Milagro Stefany Tejada Jiménez:	MilagroTejada
Noe Steve Mejia Hernandez:	Steve11xx
Jose Angel Gutierrez Cortez:	JAGC60

Cambios realizados:
Se crearon las respectivas carpetas templates para la web, una en la carpeta sistema con los CRUD de
citas, especialidad, medicos y pacientes, y otra en la carpeta core para el template que tendrá el diseño base
para la web. También se modificaron los archivos views.py   urls.py   y   forms.py para elfuncionamiento de los CRUD

Las respectivas carpetas citas, especialidad, medicos y pacientes tienen ya en funcionamiento sus respectivos CRUD
que modifican correctamente los datos en la base de datos.

Copie y pegue el siguiente enlace en el navegador:
http://127.0.0.1:8000/sistema/pacientes/

Actualización de cambios.

Implementación del sistema de autenticación y Control de acceso y permisos.

Se implementó un sistema de autenticación, no se podrá acceder al sistema si no se tiene una cuenta
cuenta creada, se agregó un login para iniciar sesión y un registrarse para crearse una cuenta,
en lugar de usar @login_required se optó por otra alternativa ya que el sistema de autenticación
que se usa es diferente.

Se agregó un menú para navegar mejor por el sistema y se modificó el navbar anterior al igual
que se agregó diseños a la web usando bootstrap y otros archivos css.

Se agregó la opción de que los usuarios puedan editar y actualizar su cuenta, además se modificó el
apartado visual de formularios y tablas.

Se modificó las citas para que los usuarios pacientes y medicos solo puedan ver las citas que los
referencien por sus ids.

Se modificó el código para limitar el acceso a los diferentes tipos de usuarios a ciertas partes
del sistema, siendo el usuario administrador el único que tiene acceso al sistema completo.

Se actualizó la sección de pedir citas para que al seleccionar una especialidad ahora puedan 
filtrarse los médicos que pertenecen a dica especialidad.

El código js para las citas se pasó a la carpeta static y se enlazó correctamente desde el 
archivo base.html.