from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView, CreateView
from django.contrib import messages
from django.views import View
from django.urls import reverse_lazy
from .forms import CustomLoginForm, RegistroPacienteForm

class LoginView(FormView):
    #Vista de login

    template_name = 'core/registration/sesion.html'
    form_class = CustomLoginForm
    success_url = reverse_lazy('core:menu')
    
    def form_valid(self, form):
        #Guarda el usuario en la sesión cuando el login es exitoso.
        
        usuario = form.get_user()
        # Guardar información del usuario en la sesión
        self.request.session['usuario_id'] = usuario.id_usuario
        self.request.session['usuario_email'] = usuario.correo
        self.request.session['usuario_autenticado'] = True
        return super().form_valid(form)

class MenuView(TemplateView):
    #Vista del menú principal protegida.

    template_name = 'core/componentes/menu.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Verifica si el usuario está autenticado antes de mostrar el menú.

        if not request.session.get('usuario_autenticado'):
            return redirect('core:login')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        #Agrega información del usuario al contexto del template.

        context = super().get_context_data(**kwargs)
        context['usuario_email'] = self.request.session.get('usuario_email')
        return context

class ContactenosView(TemplateView):
    template_name = 'core/componentes/contacto.html'

    def dispatch(self, request, *args, **kwargs):
        # Verifica si el usuario está autenticado.

        if not request.session.get('usuario_autenticado'):
            return redirect('core:login')
        return super().dispatch(request, *args, **kwargs)

class LogoutView(View):
    #Vista para cerrar sesión del usuario.
    
    def get(self, request):
        # Limpiar la sesión
        request.session.flush()
        return redirect('core:login')

class RegistroView(FormView):
    """
    Vista para registrar nuevos pacientes.
    """
    template_name = 'core/registration/registrar.html'
    form_class = RegistroPacienteForm
    success_url = reverse_lazy('core:login')
    
    def form_valid(self, form):
        """
        Cuando el formulario es válido, crea el usuario y paciente.
        """
        try:
            usuario = form.save()
            messages.success(
                self.request, 
                f'¡Paciente {usuario.correo} registrado exitosamente! Ahora puedes iniciar sesión.'
            )
            return super().form_valid(form)
        except Exception as e:
            messages.error(
                self.request, 
                'Error al registrar el paciente. Por favor intenta nuevamente.'
            )
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        """
        Cuando el formulario es inválido, muestra errores.
        """
        messages.error(self.request, 'Por favor corrige los errores en el formulario.')
        return super().form_invalid(form)