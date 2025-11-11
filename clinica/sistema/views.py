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
    model = Paciente
    form_class = PacienteForm
    template_name = 'pacientes/pacientes-update.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        paciente = self.get_object()
        if paciente and paciente.id_usuario:
            form.fields['correo'].initial = paciente.id_usuario.correo
            form.fields['contrasenia'].initial = paciente.id_usuario.contrasenia
        return form
    
    def form_valid(self, form):
        usuario = self.object.id_usuario
        usuario.correo = form.cleaned_data['correo']
        
        if form.cleaned_data.get('contrasenia'):
            usuario.contrasenia = form.cleaned_data['contrasenia']
        usuario.save()
        
        return super().form_valid(form)
    
    def get_success_url(self):
        # Obtener el usuario actual
        usuario_email = self.request.session.get('usuario_email')
        if usuario_email:
            try:
                from .models import Usuario, Medico, Administrador
                usuario = Usuario.objects.get(correo=usuario_email)
                
                # Verificar si el usuario que está editando es el mismo que está logueado
                paciente_editado = self.get_object()
                usuario_actual_es_paciente_editado = (
                    hasattr(paciente_editado, 'id_usuario') and 
                    paciente_editado.id_usuario == usuario
                )
                
                # Si está editando su propia cuenta, redirigir a cuenta-view
                if usuario_actual_es_paciente_editado:
                    return reverse_lazy('sistema:cuenta-view')
                
                # Si es administrador y está editando otro paciente, redirigir a lista
                elif Administrador.objects.filter(id_usuario=usuario).exists():
                    return reverse_lazy('sistema:pacientes-list')
                    
                # Si es médico, redirigir a donde corresponda
                elif Medico.objects.filter(id_usuario=usuario).exists():
                    return reverse_lazy('sistema:medicos-list')
                    
            except Usuario.DoesNotExist:
                pass
        
        # Redirección por defecto
        return reverse_lazy('sistema:cuenta-view')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Actualizar Paciente'
        
        # Determinar si está editando su propia cuenta
        usuario_email = self.request.session.get('usuario_email')
        if usuario_email:
            try:
                from .models import Usuario
                usuario = Usuario.objects.get(correo=usuario_email)
                paciente_editado = self.get_object()
                
                # Verificar si está editando su propia cuenta
                context['editando_propia_cuenta'] = (
                    hasattr(paciente_editado, 'id_usuario') and 
                    paciente_editado.id_usuario == usuario
                )
                
                # También pasar si es administrador para el botón cancelar
                from .models import Administrador
                context['es_administrador'] = Administrador.objects.filter(id_usuario=usuario).exists()
                
            except Usuario.DoesNotExist:
                context['editando_propia_cuenta'] = False
                context['es_administrador'] = False
        
        return context
    
    def dispatch(self, request, *args, **kwargs):
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
        # Obtener el usuario actual
        usuario_email = self.request.session.get('usuario_email')
        if usuario_email:
            try:
                from .models import Usuario, Medico, Administrador
                usuario = Usuario.objects.get(correo=usuario_email)
                
                # Verificar si el usuario que está editando es el mismo que está logueado
                medico_editado = self.get_object()
                usuario_actual_es_medico_editado = (
                    hasattr(medico_editado, 'id_usuario') and 
                    medico_editado.id_usuario == usuario
                )
                
                # Si está editando su propia cuenta, redirigir a cuenta-view
                if usuario_actual_es_medico_editado:
                    return reverse_lazy('sistema:cuenta-view')
                
                # Si es administrador y está editando otro médico, redirigir a lista
                elif Administrador.objects.filter(id_usuario=usuario).exists():
                    return reverse_lazy('sistema:medicos-list')
                    
                # Si es médico editando otro médico (no debería pasar), redirigir a cuenta
                elif Medico.objects.filter(id_usuario=usuario).exists():
                    return reverse_lazy('sistema:cuenta-view')
                    
            except Usuario.DoesNotExist:
                pass
        
        # Redirección por defecto
        return reverse_lazy('sistema:cuenta-view')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Actualizar Médico'
        
        # Determinar si está editando su propia cuenta
        usuario_email = self.request.session.get('usuario_email')
        if usuario_email:
            try:
                from .models import Usuario
                usuario = Usuario.objects.get(correo=usuario_email)
                medico_editado = self.get_object()
                
                # Verificar si está editando su propia cuenta
                context['editando_propia_cuenta'] = (
                    hasattr(medico_editado, 'id_usuario') and 
                    medico_editado.id_usuario == usuario
                )
                
                # También pasar si es administrador para el botón cancelar
                from .models import Administrador
                context['es_administrador'] = Administrador.objects.filter(id_usuario=usuario).exists()
                
            except Usuario.DoesNotExist:
                context['editando_propia_cuenta'] = False
                context['es_administrador'] = False
        
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
        correo_original = usuario_email
        
        if usuario_email:
            try:
                usuario = Usuario.objects.get(correo=usuario_email)
                nuevo_correo = request.POST.get('correo')
                correo_cambiado = nuevo_correo and nuevo_correo != usuario_email
                
                # Actualizar datos según el tipo de usuario
                usuario_actualizado = self._actualizar_usuario_segun_tipo(request, usuario)
                
                if not usuario_actualizado:
                    messages.error(request, '❌ Error: No se pudo actualizar los datos.')
                    context = self._get_context_data()
                    return render(request, self.template_name, context)
                
                # Si el correo cambió, cerrar sesión y redirigir
                if correo_cambiado:
                    request.session.flush()
                    # CORREGIDO: Usar la ruta correcta
                    return render(request, 'core/componentes/sesion-cerrada.html')
                
                messages.success(request, '✅ Tus datos se han actualizado correctamente.')
                
            except Usuario.DoesNotExist:
                messages.error(request, '❌ Error: Usuario no encontrado.')
            except Exception as e:
                messages.error(request, f'❌ Error al actualizar los datos: {str(e)}')
        
        context = self._get_context_data()
        return render(request, self.template_name, context)

    def _actualizar_usuario_segun_tipo(self, request, usuario):
        """Actualiza los datos según el tipo de usuario"""
        try:
            nuevo_correo = request.POST.get('correo')
            nueva_contrasenia = request.POST.get('contrasenia')
            
            # Actualizar datos básicos del usuario
            if nuevo_correo:
                usuario.correo = nuevo_correo
            
            if nueva_contrasenia and nueva_contrasenia.strip():
                usuario.contrasenia = nueva_contrasenia
            
            usuario.save()
            
            # Actualizar datos específicos según el tipo de usuario
            from .models import Paciente, Medico, Administrador
            
            # Verificar si es paciente
            try:
                paciente = Paciente.objects.get(id_usuario=usuario)
                paciente.nombres = request.POST.get('nombres', '')
                paciente.apellidos = request.POST.get('apellidos', '')
                paciente.telefono = request.POST.get('telefono', '')
                paciente.save()
                return True
                
            except Paciente.DoesNotExist:
                # Verificar si es médico
                try:
                    medico = Medico.objects.get(id_usuario=usuario)
                    medico.nombres = request.POST.get('nombres', '')
                    medico.apellidos = request.POST.get('apellidos', '')
                    medico.telefono = request.POST.get('telefono', '')
                    medico.save()
                    return True
                    
                except Medico.DoesNotExist:
                    # Verificar si es administrador
                    try:
                        administrador = Administrador.objects.get(id_usuario=usuario)
                        administrador.nombres = request.POST.get('nombres', '')
                        administrador.apellidos = request.POST.get('apellidos', '')
                        administrador.telefono = request.POST.get('telefono', '')
                        administrador.save()
                        return True
                        
                    except Administrador.DoesNotExist:
                        return False  # No se encontró en ninguna tabla
            
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
            return False

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