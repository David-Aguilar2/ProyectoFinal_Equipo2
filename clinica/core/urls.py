from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('menu/', views.MenuView.as_view(), name='menu'),
    path('contactenos/', views.ContactenosView.as_view(), name='contactenos'),
    path('registrar/', views.RegistroView.as_view(), name='registrar'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]