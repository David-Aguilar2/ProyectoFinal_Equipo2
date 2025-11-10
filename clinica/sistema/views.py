from django.shortcuts import render, redirect
#Importar las vistas genéricas
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
#Importar las clases
from .models import Especialidad, Paciente, Medico, Cita, Usuario, Administrador
from django.views import View
from django.contrib import messages
#Importar el método reverse_lazy
from django.urls import reverse_lazy
#Importar los formularios
from .forms import EspecialidadForm, PacienteForm, MedicoForm, CitaForm, CitaMedicoForm
from django.http import JsonResponse

# Create your views here.

#Crear una clase genérica para mostrar todas las especialidades
class EspecialidadListView(ListView):

    #Indicar el modelo
    model = Especialidad
    template_name = 'especialidad/especialidad-list.html'
    context_object_name = 'especialidad'

    def dispatch(self, request, *args, **kwargs):
        # Verifica si el usuario está autenticado.

        if not request.session.get('usuario_autenticado'):
            return redirect('core:login')
        return super().dispatch(request, *args, **kwargs)

#Crear una clase genérica para crear una nueva especialidad
class EspecialidadCreateView(CreateView):

    #Indicar el modelo
    model = Especialidad
    template_name = 'especialidad/especialidad-form.html'
    form_class = EspecialidadForm
    success_url = reverse_lazy('sistema:especialidad-list')

    def dispatch(self, request, *args, **kwargs):
        # Verifica si el usuario está autenticado.

        if not request.session.get('usuario_autenticado'):
            return redirect('core:login')
        return super().dispatch(request, *args, **kwargs)

#Crear una clase genérica para eliminar una especialidad
class EspecialidadDeleteView(DeleteView):

    #Indicar el modelo
    model = Especialidad
    template_name = 'especialidad/especialidad-delete.html'
    success_url = reverse_lazy('sistema:especialidad-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Especialidad'
        return context
    
    def dispatch(self, request, *args, **kwargs):
        # Verifica si el usuario está autenticado.

        if not request.session.get('usuario_autenticado'):
            return redirect('core:login')
        return super().dispatch(request, *args, **kwargs)

#Crear una clase genérica para actualizar una especialidad
class EspecialidadUpdateView(UpdateView):
    
    #Indicar el modelo
    model = Especialidad
    form_class = EspecialidadForm
    template_name = 'especialidad/especialidad-update.html'
    success_url = reverse_lazy('sistema:especialidad-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Actualizar Especialidad'
        return context
    
    def dispatch(self, request, *args, **kwargs):
        # Verifica si el usuario está autenticado.

        if not request.session.get('usuario_autenticado'):
            return redirect('core:login')
        return super().dispatch(request, *args, **kwargs)

#Crear una clase genérica para mostrar todos los pacientes
class PacienteListView(ListView):
    model = Paciente
    template_name = 'pacientes/pacientes-list.html'
    context_object_name = 'pacientes'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('usuario_autenticado'):
            return redirect('core:login')
        
        # Verificar si es administrador o médico
        usuario_email = request.session.get('usuario_email')
        if usuario_email:
            from .models import Usuario, Medico, Administrador
            try:
                usuario = Usuario.objects.get(correo=usuario_email)
                # Si no es administrador ni médico, redirigir
                if not (Medico.objects.filter(id_usuario=usuario).exists() or 
                       Administrador.objects.filter(id_usuario=usuario).exists()):
                    return redirect('core:menu')
            except Usuario.DoesNotExist:
                return redirect('core:menu')
        
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Determinar si es médico (solo lectura)
        usuario_email = self.request.session.get('usuario_email')
        if usuario_email:
            from .models import Usuario, Medico
            try:
                usuario = Usuario.objects.get(correo=usuario_email)
                context['es_medico'] = Medico.objects.filter(id_usuario=usuario).exists()
            except Usuario.DoesNotExist:
                pass
        return context

#Crear una clase genérica para crear un nuevo paciente
class PacienteCreateView(CreateView):

    #Indicar el modelo
    model = Paciente
    template_name = 'pacientes/pacientes-form.html'
    form_class = PacienteForm
    success_url = reverse_lazy('sistema:pacientes-list')

    def dispatch(self, request, *args, **kwargs):
        # Verifica si el usuario está autenticado.

        if not request.session.get('usuario_autenticado'):
            return redirect('core:login')
        return super().dispatch(request, *args, **kwargs)

#Crear una clase genérica para eliminar un paciente
class PacienteDeleteView(DeleteView):

    #Indicar el modelo
    model = Paciente
    template_name = 'pacientes/pacientes-delete.html'
    success_url = reverse_lazy('sistema:pacientes-list')
    
    def delete(self, request, *args, **kwargs):
        paciente = self.get_object()
        usuario = paciente.id_usuario
        
        # Primero eliminar el paciente
        response = super().delete(request, *args, **kwargs)
        
        # Luego eliminar el usuario
        usuario.delete()
        
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Paciente y Usuario'
        return context
    
    def dispatch(self, request, *args, **kwargs):
        # Verifica si el usuario está autenticado.

        if not request.session.get('usuario_autenticado'):
            return redirect('core:login')
        return super().dispatch(request, *args, **kwargs)

#Crear una clase genérica para actualizar un paciente
class PacienteUpdateView(UpdateView):
    
    #Indicar el modelo
    model = Paciente
    form_class = PacienteForm
    template_name = 'pacientes/pacientes-update.html'

    # success_url se manejará dinámicamente en get_success_url
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Pre-cargar el correo y contraseña del usuario en el formulario
        paciente = self.get_object()
        if paciente and paciente.id_usuario:
            form.fields['correo'].initial = paciente.id_usuario.correo
            form.fields['contrasenia'].initial = paciente.id_usuario.contrasenia
        return form
    
    def form_valid(self, form):
        # Primero actualizar el usuario
        usuario = self.object.id_usuario
        usuario.correo = form.cleaned_data['correo']
        
        # Solo actualizar contraseña si se proporcionó una nueva
        if form.cleaned_data.get('contrasenia'):
            usuario.contrasenia = form.cleaned_data['contrasenia']
        usuario.save()
        
        #Actualizar el paciente
        return super().form_valid(form)
    
    def get_success_url(self):
        # Redirigir a pacientes-list si es administrador, sino a cuenta
        if self.request.session.get('es_administrador'):
            return reverse_lazy('sistema:pacientes-list')
        else:
            return reverse_lazy('sistema:cuenta-view')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Actualizar Paciente'
        # Pasar si es administrador desde la sesión
        context['es_administrador'] = self.request.session.get('es_administrador', False)
        return context
    
    def dispatch(self, request, *args, **kwargs):
        # Verifica si el usuario está autenticado.
        if not request.session.get('usuario_autenticado'):
            return redirect('core:login')
        return super().dispatch(request, *args, **kwargs)

#Crear una clase genérica para mostrar todos los medicos
class MedicoListView(ListView):

    #Indicar el modelo
    model = Medico
    template_name = 'medicos/medicos-list.html'
    context_object_name = 'medicos'

    def dispatch(self, request, *args, **kwargs):
        # Verifica si el usuario está autenticado.

        if not request.session.get('usuario_autenticado'):
            return redirect('core:login')
        return super().dispatch(request, *args, **kwargs)

#Crear una clase genérica para crear un nuevo medico
class MedicoCreateView(CreateView):

    #Indicar el modelo
    model = Medico
    template_name = 'medicos/medicos-form.html'
    form_class = MedicoForm
    success_url = reverse_lazy('sistema:medicos-list')

    def dispatch(self, request, *args, **kwargs):
        # Verifica si el usuario está autenticado.

        if not request.session.get('usuario_autenticado'):
            return redirect('core:login')
        return super().dispatch(request, *args, **kwargs)

#Crear una clase genérica para eliminar un medico
class MedicoDeleteView(DeleteView):

    #Indicar el modelo
    model = Medico
    template_name = 'medicos/medicos-delete.html'
    success_url = reverse_lazy('sistema:medicos-list')
    
    def delete(self, request, *args, **kwargs):
        medico = self.get_object()
        usuario = medico.id_usuario
        
        # Primero eliminar el medico
        response = super().delete(request, *args, **kwargs)
        
        # Luego eliminar el usuario
        usuario.delete()
        
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Médico y Usuario'
        return context
    
    def dispatch(self, request, *args, **kwargs):
        # Verifica si el usuario está autenticado.

        if not request.session.get('usuario_autenticado'):
            return redirect('core:login')
        return super().dispatch(request, *args, **kwargs)
    
#Crear una clase genérica para actualizar un medico
class MedicoUpdateView(UpdateView):
    
    model = Medico
    form_class = MedicoForm
    template_name = 'medicos/medicos-update.html'
    # success_url se manejará dinámicamente en get_success_url
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        medico = self.get_object()
        if medico and medico.id_usuario:
            form.fields['correo'].initial = medico.id_usuario.correo
            form.fields['contrasenia'].initial = medico.id_usuario.contrasenia
        return form
    
    def form_valid(self, form):
        usuario = self.object.id_usuario
        usuario.correo = form.cleaned_data['correo']
        
        if form.cleaned_data.get('contrasenia'):
            usuario.contrasenia = form.cleaned_data['contrasenia']
        usuario.save()
        
        return super().form_valid(form)
    
    def get_success_url(self):
        # Redirigir a medicos-list si es administrador, sino a cuenta
        if self.request.session.get('es_administrador'):
            return reverse_lazy('sistema:medicos-list')
        else:
            return reverse_lazy('sistema:cuenta-view')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Actualizar Médico'  # ✅ Corregido
        context['es_administrador'] = self.request.session.get('es_administrador', False)
        return context
    
    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('usuario_autenticado'):
            return redirect('core:login')
        return super().dispatch(request, *args, **kwargs)
    
def medicos_por_especialidad(request, especialidad_id):
    medicos = Medico.objects.filter(id_especialidad_id=especialidad_id)
    data = {
        'medicos': [
            {
                'id': medico.id_medico,
                'nombres': medico.nombres,
                'apellidos': medico.apellidos,
                'especialidad': medico.id_especialidad.nombre_especialidad
            }
            for medico in medicos
        ]
    }
    return JsonResponse(data)

    
#Crear una clase genérica para mostrar todas las citas
class CitaListView(ListView):
    model = Cita
    template_name = 'citas/citas-list.html'
    context_object_name = 'citas'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('usuario_autenticado'):
            return redirect('core:login')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        usuario_email = self.request.session.get('usuario_email')
        
        if usuario_email:
            from .models import Usuario, Paciente, Medico
            
            try:
                usuario = Usuario.objects.get(correo=usuario_email)
                
                # Si es paciente, mostrar solo sus citas
                try:
                    paciente = Paciente.objects.get(id_usuario=usuario)
                    return Cita.objects.filter(id_paciente=paciente)
                except Paciente.DoesNotExist:
                    # Si es médico, mostrar solo sus consultas
                    try:
                        medico = Medico.objects.get(id_usuario=usuario)
                        return Cita.objects.filter(id_medico=medico)
                    except Medico.DoesNotExist:
                        # Si es administrador, mostrar todas las citas
                        return Cita.objects.all()
            
            except Usuario.DoesNotExist:
                return Cita.objects.none()
        
        return Cita.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario_email = self.request.session.get('usuario_email')
        
        if usuario_email:
            from .models import Usuario, Paciente, Medico, Administrador
            
            try:
                usuario = Usuario.objects.get(correo=usuario_email)
                
                if Paciente.objects.filter(id_usuario=usuario).exists():
                    context['tipo_usuario'] = 'paciente'
                elif Medico.objects.filter(id_usuario=usuario).exists():
                    context['tipo_usuario'] = 'medico'
                elif Administrador.objects.filter(id_usuario=usuario).exists():
                    context['tipo_usuario'] = 'administrador'
                else:
                    context['tipo_usuario'] = 'usuario'
            
            except Usuario.DoesNotExist:
                context['tipo_usuario'] = 'invitado'
        
        return context

#Crear una clase genérica para crear una nueva cita
class CitaCreateView(CreateView):
    model = Cita
    form_class = CitaForm
    template_name = 'citas/citas-form.html'
    success_url = reverse_lazy('sistema:citas-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('usuario_autenticado'):
            return redirect('core:login')
        return super().dispatch(request, *args, **kwargs)

#Crear una clase genérica para eliminar una cita
class CitaDeleteView(DeleteView):
    #Indicar el modelo
    model = Cita
    template_name = 'citas/citas-delete.html'
    success_url = reverse_lazy('sistema:citas-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Cita'
        return context
    
    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('usuario_autenticado'):
            return redirect('core:login')
        
        # Obtener la cita
        cita = self.get_object()
        usuario_id = request.session.get('usuario_id')
        
        if usuario_id:
            usuario = Usuario.objects.get(pk=usuario_id)
            
            # Verificar permisos
            es_admin = Administrador.objects.filter(id_usuario=usuario).exists()
            if es_admin:
                return super().dispatch(request, *args, **kwargs)
            
            try:
                paciente = Paciente.objects.get(id_usuario=usuario)
                if cita.id_paciente == paciente:
                    return super().dispatch(request, *args, **kwargs)
            except Paciente.DoesNotExist:
                pass
            
            messages.error(request, 'No tienes permiso para eliminar esta cita.')
            return redirect('sistema:citas-list')
            
        return super().dispatch(request, *args, **kwargs)

#Crear una clase genérica para actualizar una cita
class CitaUpdateView(UpdateView):
    model = Cita
    template_name = 'citas/citas-update.html'
    success_url = reverse_lazy('sistema:citas-list')

    def get_form_class(self):
        # Determinar qué formulario usar según el tipo de usuario
        usuario_email = self.request.session.get('usuario_email')
        
        if usuario_email:
            from .models import Usuario, Medico
            try:
                usuario = Usuario.objects.get(correo=usuario_email)
                # Si es médico, usar formulario restringido (solo fecha)
                if Medico.objects.filter(id_usuario=usuario).exists():
                    return CitaMedicoForm
            except Usuario.DoesNotExist:
                pass
        
        # Para administradores y pacientes, usar el formulario completo
        return CitaForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pasar el request al formulario si es CitaForm
        if self.get_form_class() == CitaForm:
            kwargs['request'] = self.request
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('usuario_autenticado'):
            return redirect('core:login')
        return super().dispatch(request, *args, **kwargs)
    
#Crear una clase genérica para ver la cuenta del usuario
class CuentaView(View):
    template_name = 'cuenta/cuenta-view.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('usuario_autenticado'):
            return redirect('core:login')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self._get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        usuario_email = request.session.get('usuario_email')
        
        if usuario_email:
            try:
                usuario = Usuario.objects.get(correo=usuario_email)
                administrador = Administrador.objects.get(id_usuario=usuario)
                
                print(f"🔍 DEBUG - Datos recibidos:")
                print(f"Correo: {request.POST.get('correo')}")
                print(f"Nombres: {request.POST.get('nombres')}")
                print(f"Apellidos: {request.POST.get('apellidos')}")
                print(f"Teléfono: {request.POST.get('telefono')}")
                print(f"Contraseña: {'***' if request.POST.get('contrasenia') else 'No cambiada'}")
                
                # Actualizar datos del usuario
                nuevo_correo = request.POST.get('correo')
                if nuevo_correo:
                    usuario.correo = nuevo_correo
                
                nueva_contrasenia = request.POST.get('contrasenia')
                if nueva_contrasenia and nueva_contrasenia.strip():  # Solo actualizar si no está vacía
                    usuario.contrasenia = nueva_contrasenia
                
                usuario.save()
                print("✅ Usuario actualizado")
                
                # Actualizar datos del administrador
                administrador.nombres = request.POST.get('nombres', '')
                administrador.apellidos = request.POST.get('apellidos', '')
                administrador.telefono = request.POST.get('telefono', '')
                administrador.save()
                print("✅ Administrador actualizado")
                
                # Actualizar la sesión con el nuevo email si cambió
                if nuevo_correo and nuevo_correo != usuario_email:
                    request.session['usuario_email'] = nuevo_correo
                
                messages.success(request, '✅ Tus datos se han actualizado correctamente.')
                
            except Usuario.DoesNotExist:
                messages.error(request, '❌ Error: Usuario no encontrado.')
                print("❌ Usuario no encontrado")
            except Administrador.DoesNotExist:
                messages.error(request, '❌ Error: No tienes permisos de administrador.')
                print("❌ Administrador no encontrado")
            except Exception as e:
                messages.error(request, f'❌ Error al actualizar los datos: {str(e)}')
                print(f"❌ Error: {str(e)}")
        
        context = self._get_context_data()
        return render(request, self.template_name, context)

    def _get_context_data(self):
        context = {}
        context['usuario_email'] = self.request.session.get('usuario_email')
        
        usuario_email = self.request.session.get('usuario_email')
        
        if usuario_email:
            try:
                usuario = Usuario.objects.get(correo=usuario_email)
                context['usuario'] = usuario
                
                # Verificar si es paciente
                try:
                    paciente = Paciente.objects.get(id_usuario=usuario)
                    context['paciente'] = paciente
                    context['tipo_usuario'] = 'paciente'
                except Paciente.DoesNotExist:
                    # Verificar si es médico
                    try:
                        medico = Medico.objects.get(id_usuario=usuario)
                        context['medico'] = medico
                        context['tipo_usuario'] = 'medico'
                    except Medico.DoesNotExist:
                        # Verificar si es administrador
                        try:
                            administrador = Administrador.objects.get(id_usuario=usuario)
                            context['administrador'] = administrador
                            context['tipo_usuario'] = 'administrador'
                        except Administrador.DoesNotExist:
                            context['tipo_usuario'] = 'usuario_general'
                        
            except Usuario.DoesNotExist:
                context['tipo_usuario'] = 'invitado'
                
        return context