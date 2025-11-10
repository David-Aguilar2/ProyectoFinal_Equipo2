from django import forms
from .models import Usuario, Especialidad, Paciente, Medico, Cita

#Crear un formulario para el modelo especialidad
class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = ['nombre_especialidad', 'descripcion']
        widgets = {
            'nombre_especialidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la especialidad'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción',"rows": 3 }),
        }

#Crear un formulario para el modelo Paciente
class PacienteForm(forms.ModelForm):

    # Campos adicionales para crear el usuario
    correo = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Correo electrónico'}),
        label="Correo electrónico"
    )
    
    contrasenia = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Contraseña', 'type': 'password'}),
        label="Contraseña"
    )
    
    class Meta:
        model = Paciente
        fields = ['nombres', 'apellidos', 'telefono']
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
        }
    
    def save(self, commit=True):
        # Si es un NUEVO paciente (no tiene PK)
        if not self.instance.pk:
            # Crear nuevo usuario
            usuario = Usuario.objects.create(
                correo=self.cleaned_data['correo'],
                contrasenia=self.cleaned_data['contrasenia']
            )
            
            # Crear paciente asociado al usuario
            paciente = super().save(commit=False)
            paciente.id_usuario = usuario
        else:
            # Si es ACTUALIZACIÓN, obtener el paciente existente
            paciente = super().save(commit=False)
            # NO crear nuevo usuario, ya existe
        
        if commit:
            paciente.save()
        
        return paciente
    
#Crear un formulario para el modelo Medico
class MedicoForm(forms.ModelForm):

    # Campos adicionales para crear el usuario
    correo = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Correo electrónico'}),
        label="Correo electrónico"
    )
    
    contrasenia = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Contraseña', 'type': 'password'}),
        label="Contraseña"
    )

    class Meta:
        model = Medico
        fields = ['nombres', 'apellidos', 'telefono', 'id_especialidad']
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'id_especialidad': forms.Select(attrs={'class': 'form-control'}),
        }
    def save(self, commit=True):
        # Si es un NUEVO Médico (no tiene PK)
        if not self.instance.pk:
            # Crear nuevo usuario
            usuario = Usuario.objects.create(
                correo=self.cleaned_data['correo'],
                contrasenia=self.cleaned_data['contrasenia']
            )
            
            # Crear médico asociado al usuario
            medico = super().save(commit=False)
            medico.id_usuario = usuario
        else:
            # Si es ACTUALIZACIÓN, obtener el médico existente
            medico = super().save(commit=False)
            # NO crear nuevo usuario, ya existe
        
        if commit:
            medico.save()
        
        return medico

#Crear un formulario para el modelo Cita
class CitaForm(forms.ModelForm):
    especialidad = forms.ModelChoiceField(
        queryset=Especialidad.objects.all(),
        required=False,
        label="Filtrar por Especialidad",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_especialidad_filter'
        })
    )
    
    class Meta:
        model = Cita
        fields = ['motivo_consulta', 'fecha_cita', 'id_medico', 'id_paciente']
        widgets = {
            'motivo_consulta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Motivo de consulta'}),
            'fecha_cita': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'id_medico': forms.Select(attrs={'class': 'form-control', 'id': 'id_medico'}),
            'id_paciente': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'id_paciente': 'Paciente',
            'id_medico': 'Médico',
            'motivo_consulta': 'Motivo de Consulta',
            'fecha_cita': 'Fecha y Hora de Cita'
        }
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CitaForm, self).__init__(*args, **kwargs)
        
        # Reorganizar campos para que especialidad aparezca antes de médico
        self.fields['especialidad'] = forms.ModelChoiceField(
            queryset=Especialidad.objects.all(),
            required=False,
            label="Filtrar por Especialidad",
            widget=forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_especialidad_filter'
            })
        )
        
        # Mover el campo especialidad después de fecha_cita
        field_order = ['motivo_consulta', 'fecha_cita', 'especialidad', 'id_medico', 'id_paciente']
        self.order_fields(field_order)
        
        # Personalizar campos
        self.fields['id_medico'].label_from_instance = lambda obj: f"Dr. {obj.nombres} {obj.apellidos} - {obj.id_especialidad.nombre_especialidad}"
        
        # Si es paciente, mostrar solo su nombre
        if self.request and hasattr(self.request, 'session'):
            usuario_email = self.request.session.get('usuario_email')
            if usuario_email:
                from .models import Usuario, Paciente
                try:
                    usuario = Usuario.objects.get(correo=usuario_email)
                    paciente = Paciente.objects.get(id_usuario=usuario)
                    self.fields['id_paciente'].queryset = Paciente.objects.filter(id_paciente=paciente.id_paciente)
                    self.fields['id_paciente'].label_from_instance = lambda obj: f"{obj.nombres} {obj.apellidos}"
                    self.fields['id_paciente'].empty_label = None
                except (Usuario.DoesNotExist, Paciente.DoesNotExist):
                    self.fields['id_paciente'].label_from_instance = lambda obj: f"{obj.nombres} {obj.apellidos} - Tel: {obj.telefono}"
                    
#Formulario para que el médico pueda actualizar solo la fecha de la cita
class CitaMedicoForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['fecha_cita']  # Solo puede editar la fecha
        widgets = {
            'fecha_cita': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
        labels = {
            'fecha_cita': 'Fecha y Hora de Cita'
        }