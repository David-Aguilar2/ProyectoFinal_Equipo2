#Importar el método path
from django.urls import path
#Importar las vistas
from .views import (
    #Especialidades
    EspecialidadListView,
    EspecialidadCreateView,
    EspecialidadDeleteView,
    EspecialidadUpdateView,
    #Pacientes
    PacienteListView,
    PacienteCreateView,
    PacienteDeleteView,
    PacienteUpdateView,
    #Medicos
    MedicoListView,
    MedicoCreateView,
    MedicoDeleteView,
    MedicoUpdateView,
    #Citas
    CitaListView,
    CitaCreateView,
    CitaUpdateView,
    CitaDeleteView,
)

#Nombre descriptivo para la url
app_name = 'sistema'

#Crear el enrrutamiento de las urls
urlpatterns = [
    #Especialidades
    path('especialidades/', EspecialidadListView.as_view(), name='especialidad-list'),
    path('especialidades/nuevo/', EspecialidadCreateView.as_view(), name='especialidad-create'),
    path('especialidades/eliminar/<int:pk>/', EspecialidadDeleteView.as_view(), name='especialidad-delete'),
    path('especialidades/actualizar/<int:pk>/', EspecialidadUpdateView.as_view(), name='especialidad-update'),
    #Pacientes
    path('pacientes/', PacienteListView.as_view(), name='pacientes-list'),
    path('pacientes/nuevo/', PacienteCreateView.as_view(), name='pacientes-create'),
    path('pacientes/eliminar/<int:pk>/', PacienteDeleteView.as_view(), name='pacientes-delete'),
    path('pacientes/actualizar/<int:pk>/', PacienteUpdateView.as_view(), name='pacientes-update'),
    #Medicos
    path('medicos/', MedicoListView.as_view(), name='medicos-list'),
    path('medicos/nuevo/', MedicoCreateView.as_view(), name='medicos-create'),
    path('medicos/eliminar/<int:pk>/', MedicoDeleteView.as_view(), name='medicos-delete'),
    path('medicos/actualizar/<int:pk>/', MedicoUpdateView.as_view(), name='medicos-update'),

    #Citas
    path('citas/', CitaListView.as_view(), name='citas-list'),
    path('citas/nuevo/', CitaCreateView.as_view(), name='citas-create'),
    path('citas/eliminar/<int:pk>/', CitaDeleteView.as_view(), name='citas-delete'),
    path('citas/actualizar/<int:pk>/', CitaUpdateView.as_view(), name='citas-update'),
]