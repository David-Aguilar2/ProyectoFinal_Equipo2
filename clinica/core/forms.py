from django import forms
from sistema.models import Usuario, Paciente

class CustomLoginForm(forms.Form):
    """
    Formulario personalizado para autenticación con TU modelo Usuario.
    Utiliza los campos correo y contrasenia de tu modelo personalizado.
    """
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Correo electrónico'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Contraseña'
        })
    )
    
    def clean(self):
        """
        Valida las credenciales contra TU modelo Usuario.
        """
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            try:
                # Buscar en TU modelo Usuario por correo
                usuario = Usuario.objects.get(correo=email)
                
                # Verificar contraseña (comparación directa ya que está en texto plano)
                if usuario.contrasenia == password:
                    self.usuario_cache = usuario
                else:
                    raise forms.ValidationError("Correo o contraseña incorrectos.")
                    
            except Usuario.DoesNotExist:
                raise forms.ValidationError("Correo o contraseña incorrectos.")

        return self.cleaned_data

    def get_user(self):
        """
        Retorna el objeto Usuario autenticado.
        """
        return self.usuario_cache
    
class RegistroPacienteForm(forms.Form):
    """
    Formulario para registrar nuevos pacientes (Usuario + Paciente).
    """
    nombres = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombres'
        })
    )
    apellidos = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apellidos'
        })
    )
    telefono = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Teléfono'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Correo electrónico'
        })
    )
    contrasenia = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Contraseña'
        })
    )
    
    def clean_email(self):
        """
        Verifica que el email no esté ya registrado.
        """
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(correo=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email
    
    def save(self):
        """
        Crea un Usuario y un Paciente en la base de datos.
        """
        # Crear el Usuario primero
        usuario = Usuario.objects.create(
            correo=self.cleaned_data['email'],
            contrasenia=self.cleaned_data['contrasenia']
        )
        
        # Crear el Paciente asociado al Usuario
        paciente = Paciente.objects.create(
            id_usuario=usuario,
            nombres=self.cleaned_data['nombres'],
            apellidos=self.cleaned_data['apellidos'],
            telefono=self.cleaned_data['telefono']
        )
        
        return usuario