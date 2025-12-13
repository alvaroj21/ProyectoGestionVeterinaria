"""veterinariaIngSoftware URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from appVeterinaria import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Páginas públicas
    path('razas_perros/', views.listaRazasPerros, name='razas_perros'),
    path('sobre-nosotros/', views.sobre_nosotros, name='sobre_nosotros'),
    
    # Páginas protegidas (requieren autenticación)
    path('clientes/', views.listaClientes, name='clientesVet'),
    path('mascotas/', views.listaMascotas, name='mascotas'),
    path('citas/', views.listaCitas, name='citas'),
    path('veterinarios/', views.lista_veterinarios, name='lista_veterinarios'),
    path('remedios/lista/', views.lista_remedios, name='lista_remedios'),
    
    # Nuevas rutas para el panel de registro (protegidas)
    path('panel-registro/', views.panel_registro, name='panel_registro'),
    path('registrar/cliente/', views.registrar_cliente, name='registrar_cliente'),
    path('registrar/mascota/', views.registrar_mascota, name='registrar_mascota'),
    path('registrar/cita/', views.registrar_cita, name='registrar_cita'),
    path('registrar/veterinario/', views.registrar_veterinario, name='registrar_veterinario'),
    path('registrar/remedio/', views.registrar_remedio, name='registrar_remedio'),
    path('registrar/raza/', views.registrar_raza, name='registrar_raza'),
    
    # Gestión de usuarios del sistema (solo Admin)
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    
    # CRUD Clientes
    path('clientes/editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
    
    # CRUD Mascotas
    path('mascotas/editar/<int:mascota_id>/', views.editar_mascota, name='editar_mascota'),
    path('mascotas/eliminar/<int:mascota_id>/', views.eliminar_mascota, name='eliminar_mascota'),
    
    # CRUD Citas
    path('citas/editar/<int:cita_id>/', views.editar_cita, name='editar_cita'),
    path('citas/eliminar/<int:cita_id>/', views.eliminar_cita, name='eliminar_cita'),
    
    # CRUD Veterinarios
    path('veterinarios/editar/<int:veterinario_id>/', views.editar_veterinario, name='editar_veterinario'),
    path('veterinarios/eliminar/<int:veterinario_id>/', views.eliminar_veterinario, name='eliminar_veterinario'),
    
    # CRUD Remedios
    path('remedios/editar/<int:remedio_id>/', views.editar_remedio, name='editar_remedio'),
    path('remedios/eliminar/<int:remedio_id>/', views.eliminar_remedio, name='eliminar_remedio'),
    
    # CRUD Razas
    path('razas/editar/<int:raza_id>/', views.editar_raza, name='editar_raza'),
    path('razas/eliminar/<int:raza_id>/', views.eliminar_raza, name='eliminar_raza'),
    
    # Lista de razas (vista protegida)
    path('razas/', views.lista_razas, name='lista_razas'),
]