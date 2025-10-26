from django.shortcuts import render
#Importar las vistas genéricas
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
#Importar las clases
from .models import Especialidad, Paciente, Medico, Cita
#Importar el método reverse_lazy
from django.urls import reverse_lazy
#Importar los formularios
from .forms import EspecialidadForm, PacienteForm, MedicoForm, CitaForm

# Create your views here.

#Crear una clase genérica para mostrar todas las especialidades
class EspecialidadListView(ListView):

    #Indicar el modelo
    model = Especialidad
    template_name = 'especialidad/especialidad-list.html'
    context_object_name = 'especialidad'

#Crear una clase genérica para crear una nueva especialidad
class EspecialidadCreateView(CreateView):

    #Indicar el modelo
    model = Especialidad
    template_name = 'especialidad/especialidad-form.html'
    form_class = EspecialidadForm
    success_url = reverse_lazy('sistema:especialidad-list')

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

#Crear una clase genérica para mostrar todos los pacientes
class PacienteListView(ListView):

    #Indicar el modelo
    model = Paciente
    template_name = 'pacientes/pacientes-list.html'
    context_object_name = 'pacientes'

#Crear una clase genérica para crear un nuevo paciente
class PacienteCreateView(CreateView):

    #Indicar el modelo
    model = Paciente
    template_name = 'pacientes/pacientes-form.html'
    form_class = PacienteForm
    success_url = reverse_lazy('sistema:pacientes-list')

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

#Crear una clase genérica para actualizar un paciente
class PacienteUpdateView(UpdateView):
    
    #Indicar el modelo
    model = Paciente
    form_class = PacienteForm
    template_name = 'pacientes/pacientes-update.html'
    success_url = reverse_lazy('sistema:pacientes-list')
    
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Actualizar Paciente'
        return context

#Crear una clase genérica para mostrar todos los medicos
class MedicoListView(ListView):

    #Indicar el modelo
    model = Medico
    template_name = 'medicos/medicos-list.html'
    context_object_name = 'medicos'

#Crear una clase genérica para crear un nuevo medico
class MedicoCreateView(CreateView):

    #Indicar el modelo
    model = Medico
    template_name = 'medicos/medicos-form.html'
    form_class = MedicoForm
    success_url = reverse_lazy('sistema:medicos-list')

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
    
#Crear una clase genérica para actualizar un medico
class MedicoUpdateView(UpdateView):
    
    #Indicar el modelo
    model = Medico
    form_class = MedicoForm
    template_name = 'medicos/medicos-update.html'
    success_url = reverse_lazy('sistema:medicos-list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Pre-cargar el correo y contraseña del usuario en el formulario
        medico = self.get_object()
        if medico and medico.id_usuario:
            form.fields['correo'].initial = medico.id_usuario.correo
            form.fields['contrasenia'].initial = medico.id_usuario.contrasenia
        return form
    
    def form_valid(self, form):
        # Primero actualizar el usuario
        usuario = self.object.id_usuario
        usuario.correo = form.cleaned_data['correo']
        
        # Solo actualizar contraseña si se proporcionó una nueva
        if form.cleaned_data.get('contrasenia'):
            usuario.contrasenia = form.cleaned_data['contrasenia']
        usuario.save()
        
        #Actualizar el médico
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Actualizar Paciente'
        return context
    


#Crear una clase genérica para mostrar todas las citas
class CitaListView(ListView):

    #Indicar el modelo
    model = Cita
    template_name = 'citas/citas-list.html'
    context_object_name = 'citas'

#Crear una clase genérica para crear una nueva cita
class CitaCreateView(CreateView):

    #Indicar el modelo
    model = Cita
    template_name = 'citas/citas-form.html'
    form_class = CitaForm
    success_url = reverse_lazy('sistema:citas-list')

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

#Crear una clase genérica para actualizar una cita
class CitaUpdateView(UpdateView):
    
    #Indicar el modelo
    model = Cita
    form_class = CitaForm
    template_name = 'citas/citas-update.html'
    success_url = reverse_lazy('sistema:citas-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Actualizar Cita'
        return context