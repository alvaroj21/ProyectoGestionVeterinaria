from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from appVeterinaria.models import (
    ClienteVet, Mascota, CitaMascota,
    Veterinario, Razas, Remedio, Usuario
)
from appVeterinaria.forms import (
    FormClienteVet, FormMascota, FormCitaMascota,
    FormRemedio, FormVeterinario, FormRazas
)

# ============================================================================
# CONFIGURACIÓN DEL SISTEMA DE PERMISOS
# ============================================================================

# Diccionario que define qué módulos puede acceder cada rol de usuario
PERMISOS_ROL = {
    'Administrador': ['clientes', 'mascotas', 'citas', 'veterinarios', 'remedios', 'razas', 'panel_registro', 'usuarios'],
    'Veterinario': ['clientes', 'mascotas', 'citas', 'veterinarios', 'remedios', 'razas', 'panel_registro'],
}

# ============================================================================
# FUNCIONES AUXILIARES DE AUTENTICACIÓN Y PERMISOS
# ============================================================================

def usuario_logueado(request):
    """Verifica si hay un usuario autenticado en la sesión"""
    return request.session.get('user_logged', False)

def tiene_permiso(request, modulo):
    """
    Verifica si el usuario tiene permiso para acceder a un módulo específico
    Args:
        request: HttpRequest object
        modulo: string con el nombre del módulo ('clientes', 'mascotas', etc.)
    Returns:
        bool: True si tiene permiso, False en caso contrario
    """
    if not usuario_logueado(request):
        return False
    rol = request.session.get('rol', '')
    permisos = PERMISOS_ROL.get(rol, [])
    return modulo in permisos

# Vista para la página de inicio
def inicio(request):
    return render(request, 'appVeterinaria/inicio.html')

# ============================================================================
# VISTAS DE AUTENTICACIÓN (LOGIN Y LOGOUT)
# ============================================================================

def login_view(request):
    """Vista para iniciar sesión con el sistema de usuarios personalizado"""
    # Si ya está logueado, redirigir al inicio
    if usuario_logueado(request):
        return redirect('inicio')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        try:
            # Buscar el usuario en la base de datos
            usuario = Usuario.objects.get(username=username)
            
            # Verificar la contraseña (comparación simple)
            if usuario.password == password:
                # Iniciar sesión guardando datos en la sesión
                request.session['user_logged'] = True
                request.session['usuario'] = usuario.username
                request.session['username'] = usuario.username
                request.session['rol'] = usuario.rol
                request.session['nombre'] = usuario.nombre_completo
                request.session['email'] = usuario.email

                messages.success(request, f'Bienvenido {usuario.nombre_completo}!')
                return redirect('inicio')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return redirect('inicio')

def logout_view(request):
    """Vista para cerrar sesión"""
    request.session.flush()
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('inicio')

# ============================================================================
# VISTAS PROTEGIDAS - REQUIEREN AUTENTICACIÓN
# ============================================================================

# Vista para el listado de clientes
def listaClientes(request):
    if not usuario_logueado(request):
        messages.error(request, 'Debes iniciar sesión para acceder a esta sección.')
        return redirect('inicio')
    
    if not tiene_permiso(request, 'clientes'):
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('inicio')
    
    # Obtener el término de búsqueda
    search_query = request.GET.get('search', '')
    
    # Filtrar clientes
    if search_query:
        clientesVet = ClienteVet.objects.filter(
            Q(nombre__icontains=search_query) |
            Q(apellido__icontains=search_query) |
            Q(rut__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(telefono__icontains=search_query)
        ).order_by('nombre')
    else:
        clientesVet = ClienteVet.objects.all().order_by('nombre')
    
    # Paginación
    paginator = Paginator(clientesVet, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    data = {
        'clientesVet': page_obj,
        'search_query': search_query,
        'page_obj': page_obj
    }
    return render(request, 'appVeterinaria/clientesVet.html', data)

# Vista para el listado de mascotas
def listaMascotas(request):
    if not usuario_logueado(request):
        messages.error(request, 'Debes iniciar sesión para acceder a esta sección.')
        return redirect('inicio')
    
    if not tiene_permiso(request, 'mascotas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('inicio')
    
    # Obtener el término de búsqueda
    search_query = request.GET.get('search', '')
    
    # Filtrar mascotas
    if search_query:
        mascotas = Mascota.objects.filter(
            Q(nombre_mascota__icontains=search_query) |
            Q(especie_mascota__icontains=search_query) |
            Q(raza_mascota__icontains=search_query)
        ).order_by('nombre_mascota')
    else:
        mascotas = Mascota.objects.all().order_by('nombre_mascota')
    
    # Paginación
    paginator = Paginator(mascotas, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    data = {
        'mascotas': page_obj,
        'search_query': search_query,
        'page_obj': page_obj
    }
    return render(request, 'appVeterinaria/mascotas.html', data)

# Vista para el listado de citas
def listaCitas(request):
    if not usuario_logueado(request):
        messages.error(request, 'Debes iniciar sesión para acceder a esta sección.')
        return redirect('inicio')
    
    if not tiene_permiso(request, 'citas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('inicio')
    
    # Obtener el término de búsqueda
    search_query = request.GET.get('search', '')
    
    # Filtrar citas
    if search_query:
        citasMascotas = CitaMascota.objects.filter(
            Q(dato_cliente__nombre__icontains=search_query) |
            Q(dato_cliente__apellido__icontains=search_query) |
            Q(dato_mascota__nombre_mascota__icontains=search_query) |
            Q(motivo_cita__icontains=search_query)
        ).order_by('-fecha_cita')
    else:
        citasMascotas = CitaMascota.objects.all().order_by('-fecha_cita')
    
    # Paginación
    paginator = Paginator(citasMascotas, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    data = {
        'citasMascotas': page_obj,
        'search_query': search_query,
        'page_obj': page_obj
    }
    return render(request, 'appVeterinaria/citas.html', data)

# Vista para el listado de veterinarios
def lista_veterinarios(request):
    if not usuario_logueado(request):
        messages.error(request, 'Debes iniciar sesión para acceder a esta sección.')
        return redirect('inicio')
    
    if not tiene_permiso(request, 'veterinarios'):
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('inicio')
    
    # Obtener el término de búsqueda
    search_query = request.GET.get('search', '')
    
    # Filtrar veterinarios
    if search_query:
        veterinarios = Veterinario.objects.filter(
            Q(nombre_veterinario__icontains=search_query) |
            Q(especialidad__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(telefono__icontains=search_query)
        ).order_by('nombre_veterinario')
    else:
        veterinarios = Veterinario.objects.all().order_by('nombre_veterinario')
    
    # Paginación
    paginator = Paginator(veterinarios, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'appVeterinaria/veterinarios.html', {
        'veterinarios': page_obj,
        'search_query': search_query,
        'page_obj': page_obj
    })

# Vista para mostrar remedios (solo lectura desde el admin)
def lista_remedios(request):
    if not usuario_logueado(request):
        messages.error(request, 'Debes iniciar sesión para acceder a esta sección.')
        return redirect('inicio')
    
    if not tiene_permiso(request, 'remedios'):
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('inicio')
    
    # Obtener el término de búsqueda
    search_query = request.GET.get('search', '')
    
    # Filtrar remedios
    if search_query:
        remedios = Remedio.objects.filter(
            Q(nombre_remedio__icontains=search_query) |
            Q(uso_recomendado__icontains=search_query) |
            Q(animal__icontains=search_query)
        ).order_by('nombre_remedio')
    else:
        remedios = Remedio.objects.all().order_by('nombre_remedio')
    
    # Paginación
    paginator = Paginator(remedios, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'appVeterinaria/remedios.html', {
        'remedios': page_obj,
        'search_query': search_query,
        'page_obj': page_obj
    })

# Vista para mostrar razas (requiere autenticación)
def lista_razas(request):
    if not usuario_logueado(request):
        messages.error(request, 'Debes iniciar sesión para acceder a esta sección.')
        return redirect('inicio')
    
    if not tiene_permiso(request, 'razas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('inicio')
    
    # Obtener el término de búsqueda
    search_query = request.GET.get('search', '')
    
    # Filtrar razas
    if search_query:
        razas = Razas.objects.filter(
            Q(nombre_raza__icontains=search_query) |
            Q(tamanio_raza__icontains=search_query) |
            Q(pelaje_raza__icontains=search_query) |
            Q(origen_raza__icontains=search_query)
        ).order_by('nombre_raza')
    else:
        razas = Razas.objects.all().order_by('nombre_raza')
    
    # Paginación
    paginator = Paginator(razas, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'appVeterinaria/lista_razas.html', {
        'razas': page_obj,
        'search_query': search_query,
        'page_obj': page_obj
    })

# ========== NUEVAS VISTAS PARA REGISTRAR DATOS ==========

def panel_registro(request):
    """Vista principal del panel de registro"""
    if not usuario_logueado(request):
        messages.error(request, 'Debes iniciar sesión para acceder a esta sección.')
        return redirect('inicio')
    
    if not tiene_permiso(request, 'panel_registro'):
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('inicio')
    
    return render(request, 'appVeterinaria/panel_registro.html')

def registrar_cliente(request):
    if not usuario_logueado(request):
        messages.error(request, 'Debes iniciar sesión para acceder a esta sección.')
        return redirect('inicio')
    
    if not tiene_permiso(request, 'panel_registro'):
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('inicio')
    
    if request.method == 'POST':
        form = FormClienteVet(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente registrado exitosamente.')
            return redirect('panel_registro')
    else:
        form = FormClienteVet()
    return render(request, 'appVeterinaria/registrar_cliente.html', {'form': form})

def registrar_mascota(request):
    if not usuario_logueado(request):
        messages.error(request, 'Debes iniciar sesión para acceder a esta sección.')
        return redirect('inicio')
    
    if not tiene_permiso(request, 'panel_registro'):
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('inicio')
    
    if request.method == 'POST':
        form = FormMascota(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mascota registrada exitosamente.')
            return redirect('panel_registro')
    else:
        form = FormMascota()
    return render(request, 'appVeterinaria/registrar_mascota.html', {'form': form})

def registrar_cita(request):
    if not usuario_logueado(request):
        messages.error(request, 'Debes iniciar sesión para acceder a esta sección.')
        return redirect('inicio')
    
    if not tiene_permiso(request, 'panel_registro'):
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('inicio')
    
    if request.method == 'POST':
        form = FormCitaMascota(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cita registrada exitosamente.')
            return redirect('panel_registro')
    else:
        form = FormCitaMascota()
    return render(request, 'appVeterinaria/registrar_cita.html', {'form': form})

def registrar_veterinario(request):
    if not usuario_logueado(request):
        messages.error(request, 'Debes iniciar sesión para acceder a esta sección.')
        return redirect('inicio')
    
    if not tiene_permiso(request, 'panel_registro'):
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('inicio')
    
    if request.method == 'POST':
        form = FormVeterinario(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Veterinario registrado exitosamente.')
            return redirect('panel_registro')
    else:
        form = FormVeterinario()
    return render(request, 'appVeterinaria/registrar_veterinario.html', {'form': form})

def registrar_remedio(request):
    if not usuario_logueado(request):
        messages.error(request, 'Debes iniciar sesión para acceder a esta sección.')
        return redirect('inicio')
    
    if not tiene_permiso(request, 'panel_registro'):
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('inicio')
    
    if request.method == 'POST':
        form = FormRemedio(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Remedio registrado exitosamente.')
            return redirect('panel_registro')
    else:
        form = FormRemedio()
    return render(request, 'appVeterinaria/registrar_remedio.html', {'form': form})

def registrar_raza(request):
    if not usuario_logueado(request):
        messages.error(request, 'Debes iniciar sesión para acceder a esta sección.')
        return redirect('inicio')
    
    if not tiene_permiso(request, 'panel_registro'):
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('inicio')
    
    if request.method == 'POST':
        form = FormRazas(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Raza registrada exitosamente.')
            return redirect('panel_registro')
    else:
        form = FormRazas()
    return render(request, 'appVeterinaria/registrar_raza.html', {'form': form})

# ========== VISTAS PÚBLICAS ==========

# Vista para el listado de razas de perros (pública)
def listaRazasPerros(request):
    razas_perros = Razas.objects.all()
    data = {'razas_perros': razas_perros}
    return render(request, 'appVeterinaria/razas_perros.html', data)

def sobre_nosotros(request):
    """Vista para la página Sobre Nosotros (pública)"""
    return render(request, 'appVeterinaria/sobre_nosotros.html')

# ============================================================================
# GESTIÓN DE USUARIOS DEL SISTEMA - SOLO ADMINISTRADORES
# ============================================================================

def lista_usuarios(request):
    """Vista para listar todos los usuarios del sistema - Solo Admin"""
    if not usuario_logueado(request):
        messages.error(request, 'Debes iniciar sesión para acceder a esta sección.')
        return redirect('inicio')
    
    if not tiene_permiso(request, 'usuarios'):
        messages.error(request, 'No tienes permisos para acceder a esta sección. Solo administradores.')
        return redirect('inicio')
    
    # Obtener el término de búsqueda
    search_query = request.GET.get('search', '')
    
    # Filtrar usuarios
    if search_query:
        usuarios = Usuario.objects.filter(
            Q(username__icontains=search_query) |
            Q(nombre_completo__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(rol__icontains=search_query)
        ).order_by('username')
    else:
        usuarios = Usuario.objects.all().order_by('username')
    
    # Paginación
    paginator = Paginator(usuarios, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'rol': request.session.get('rol'),
        'usuarios': page_obj,
        'search_query': search_query,
        'page_obj': page_obj
    }
    return render(request, 'appVeterinaria/usuarios/lista_usuarios.html', datos)

def crear_usuario(request):
    """Vista para crear un nuevo usuario del sistema - Solo Admin"""
    if not usuario_logueado(request):
        messages.error(request, 'Debes iniciar sesión para acceder a esta sección.')
        return redirect('inicio')
    
    if not tiene_permiso(request, 'usuarios'):
        messages.error(request, 'No tienes permisos para acceder a esta sección. Solo administradores.')
        return redirect('inicio')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        confirmar_password = request.POST.get('confirmar_password', '').strip()
        email = request.POST.get('email', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        nombre_completo = request.POST.get('nombre_completo', '').strip()
        rol = request.POST.get('rol', '')
        
        # Validaciones
        if not all([username, password, email, nombre_completo, rol]):
            messages.error(request, 'Todos los campos son obligatorios excepto teléfono.')
        elif password != confirmar_password:
            messages.error(request, 'Las contraseñas no coinciden.')
        elif len(password) < 6:
            messages.error(request, 'La contraseña debe tener al menos 6 caracteres.')
        elif Usuario.objects.filter(username=username).exists():
            messages.error(request, f'El nombre de usuario "{username}" ya existe.')
        else:
            try:
                Usuario.objects.create(
                    username=username,
                    password=password,
                    email=email,
                    telefono=telefono,
                    nombre_completo=nombre_completo,
                    rol=rol
                )
                messages.success(request, f'Usuario "{username}" creado exitosamente.')
                return redirect('lista_usuarios')
            except Exception as e:
                messages.error(request, f'Error al crear usuario: {str(e)}')
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'rol': request.session.get('rol'),
    }
    return render(request, 'appVeterinaria/usuarios/crear_usuario.html', datos)

def editar_usuario(request, usuario_id):
    """Vista para editar un usuario existente - Solo Admin"""
    if not usuario_logueado(request):
        messages.error(request, 'Debes iniciar sesión para acceder a esta sección.')
        return redirect('inicio')
    
    if not tiene_permiso(request, 'usuarios'):
        messages.error(request, 'No tienes permisos para acceder a esta sección. Solo administradores.')
        return redirect('inicio')
    
    try:
        usuario = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        messages.error(request, 'El usuario no existe.')
        return redirect('lista_usuarios')
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        nombre_completo = request.POST.get('nombre_completo', '').strip()
        rol = request.POST.get('rol', '')
        nueva_password = request.POST.get('nueva_password', '').strip()
        confirmar_password = request.POST.get('confirmar_password', '').strip()
        
        # Validaciones
        if not all([email, nombre_completo, rol]):
            messages.error(request, 'Email, nombre completo y rol son obligatorios.')
        elif nueva_password and nueva_password != confirmar_password:
            messages.error(request, 'Las contraseñas no coinciden.')
        elif nueva_password and len(nueva_password) < 6:
            messages.error(request, 'La contraseña debe tener al menos 6 caracteres.')
        else:
            try:
                usuario.email = email
                usuario.telefono = telefono
                usuario.nombre_completo = nombre_completo
                usuario.rol = rol
                if nueva_password:
                    usuario.password = nueva_password
                usuario.save()
                messages.success(request, f'Usuario "{usuario.username}" actualizado exitosamente.')
                return redirect('lista_usuarios')
            except Exception as e:
                messages.error(request, f'Error al actualizar usuario: {str(e)}')
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'rol': request.session.get('rol'),
        'usuario': usuario
    }
    return render(request, 'appVeterinaria/usuarios/editar_usuario.html', datos)

def eliminar_usuario(request, usuario_id):
    """Vista para eliminar un usuario - Solo Admin"""
    if not usuario_logueado(request):
        messages.error(request, 'Debes iniciar sesión para acceder a esta sección.')
        return redirect('inicio')
    
    if not tiene_permiso(request, 'usuarios'):
        messages.error(request, 'No tienes permisos para acceder a esta sección. Solo administradores.')
        return redirect('inicio')
    
    try:
        usuario = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        messages.error(request, 'El usuario no existe.')
        return redirect('lista_usuarios')
    
    # Prevenir que un admin se elimine a sí mismo
    if usuario.username == request.session.get('username'):
        messages.error(request, 'No puedes eliminar tu propio usuario.')
        return redirect('lista_usuarios')
    
    if request.method == 'POST':
        username = usuario.username
        usuario.delete()
        messages.success(request, f'Usuario "{username}" eliminado exitosamente.')
        return redirect('lista_usuarios')
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'rol': request.session.get('rol'),
        'usuario': usuario
    }
    return render(request, 'appVeterinaria/usuarios/eliminar_usuario.html', datos)

# ============================================================================
# CRUD COMPLETO PARA CLIENTES
# ============================================================================

def editar_cliente(request, cliente_id):
    """Editar un cliente existente"""
    if not tiene_permiso(request, 'clientes'):
        messages.error(request, 'No tienes permiso para realizar esta acción.')
        return redirect('inicio')
    
    try:
        cliente = ClienteVet.objects.get(id=cliente_id)
    except ClienteVet.DoesNotExist:
        messages.error(request, 'El cliente no existe.')
        return redirect('clientesVet')
    
    if request.method == 'POST':
        form = FormClienteVet(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, f'Cliente {cliente.nombre} actualizado exitosamente.')
            return redirect('clientesVet')
    else:
        form = FormClienteVet(instance=cliente)
    
    return render(request, 'appVeterinaria/editar_cliente.html', {'form': form, 'cliente': cliente})

def eliminar_cliente(request, cliente_id):
    """Eliminar un cliente"""
    if not tiene_permiso(request, 'clientes'):
        messages.error(request, 'No tienes permiso para realizar esta acción.')
        return redirect('inicio')
    
    try:
        cliente = ClienteVet.objects.get(id=cliente_id)
    except ClienteVet.DoesNotExist:
        messages.error(request, 'El cliente no existe.')
        return redirect('clientesVet')
    
    if request.method == 'POST':
        nombre = f"{cliente.nombre} {cliente.apellido}"
        cliente.delete()
        messages.success(request, f'Cliente {nombre} eliminado exitosamente.')
        return redirect('clientesVet')
    
    return render(request, 'appVeterinaria/eliminar_cliente.html', {'cliente': cliente})

# ============================================================================
# CRUD COMPLETO PARA MASCOTAS
# ============================================================================

def editar_mascota(request, mascota_id):
    """Editar una mascota existente"""
    if not tiene_permiso(request, 'mascotas'):
        messages.error(request, 'No tienes permiso para realizar esta acción.')
        return redirect('inicio')
    
    try:
        mascota = Mascota.objects.get(id=mascota_id)
    except Mascota.DoesNotExist:
        messages.error(request, 'La mascota no existe.')
        return redirect('mascotas')
    
    if request.method == 'POST':
        form = FormMascota(request.POST, instance=mascota)
        if form.is_valid():
            form.save()
            messages.success(request, f'Mascota {mascota.nombre_mascota} actualizada exitosamente.')
            return redirect('mascotas')
    else:
        form = FormMascota(instance=mascota)
    
    return render(request, 'appVeterinaria/editar_mascota.html', {'form': form, 'mascota': mascota})

def eliminar_mascota(request, mascota_id):
    """Eliminar una mascota"""
    if not tiene_permiso(request, 'mascotas'):
        messages.error(request, 'No tienes permiso para realizar esta acción.')
        return redirect('inicio')
    
    try:
        mascota = Mascota.objects.get(id=mascota_id)
    except Mascota.DoesNotExist:
        messages.error(request, 'La mascota no existe.')
        return redirect('mascotas')
    
    if request.method == 'POST':
        nombre = mascota.nombre_mascota
        mascota.delete()
        messages.success(request, f'Mascota {nombre} eliminada exitosamente.')
        return redirect('mascotas')
    
    return render(request, 'appVeterinaria/eliminar_mascota.html', {'mascota': mascota})

# ============================================================================
# CRUD COMPLETO PARA CITAS
# ============================================================================

def editar_cita(request, cita_id):
    """Editar una cita existente"""
    if not tiene_permiso(request, 'citas'):
        messages.error(request, 'No tienes permiso para realizar esta acción.')
        return redirect('inicio')
    
    try:
        cita = CitaMascota.objects.get(id=cita_id)
    except CitaMascota.DoesNotExist:
        messages.error(request, 'La cita no existe.')
        return redirect('citas')
    
    if request.method == 'POST':
        form = FormCitaMascota(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cita actualizada exitosamente.')
            return redirect('citas')
    else:
        form = FormCitaMascota(instance=cita)
    
    return render(request, 'appVeterinaria/editar_cita.html', {'form': form, 'cita': cita})

def eliminar_cita(request, cita_id):
    """Eliminar una cita"""
    if not tiene_permiso(request, 'citas'):
        messages.error(request, 'No tienes permiso para realizar esta acción.')
        return redirect('inicio')
    
    try:
        cita = CitaMascota.objects.get(id=cita_id)
    except CitaMascota.DoesNotExist:
        messages.error(request, 'La cita no existe.')
        return redirect('citas')
    
    if request.method == 'POST':
        cita.delete()
        messages.success(request, 'Cita eliminada exitosamente.')
        return redirect('citas')
    
    return render(request, 'appVeterinaria/eliminar_cita.html', {'cita': cita})

# ============================================================================
# CRUD COMPLETO PARA VETERINARIOS
# ============================================================================

def editar_veterinario(request, veterinario_id):
    """Editar un veterinario existente"""
    if not tiene_permiso(request, 'veterinarios'):
        messages.error(request, 'No tienes permiso para realizar esta acción.')
        return redirect('inicio')
    
    try:
        veterinario = Veterinario.objects.get(id=veterinario_id)
    except Veterinario.DoesNotExist:
        messages.error(request, 'El veterinario no existe.')
        return redirect('lista_veterinarios')
    
    if request.method == 'POST':
        form = FormVeterinario(request.POST, instance=veterinario)
        if form.is_valid():
            form.save()
            messages.success(request, f'Veterinario {veterinario.nombre_veterinario} actualizado exitosamente.')
            return redirect('lista_veterinarios')
    else:
        form = FormVeterinario(instance=veterinario)
    
    return render(request, 'appVeterinaria/editar_veterinario.html', {'form': form, 'veterinario': veterinario})

def eliminar_veterinario(request, veterinario_id):
    """Eliminar un veterinario"""
    if not tiene_permiso(request, 'veterinarios'):
        messages.error(request, 'No tienes permiso para realizar esta acción.')
        return redirect('inicio')
    
    try:
        veterinario = Veterinario.objects.get(id=veterinario_id)
    except Veterinario.DoesNotExist:
        messages.error(request, 'El veterinario no existe.')
        return redirect('lista_veterinarios')
    
    if request.method == 'POST':
        nombre = veterinario.nombre_veterinario
        veterinario.delete()
        messages.success(request, f'Veterinario {nombre} eliminado exitosamente.')
        return redirect('lista_veterinarios')
    
    return render(request, 'appVeterinaria/eliminar_veterinario.html', {'veterinario': veterinario})

# ============================================================================
# CRUD COMPLETO PARA REMEDIOS
# ============================================================================

def editar_remedio(request, remedio_id):
    """Editar un remedio existente"""
    if not tiene_permiso(request, 'remedios'):
        messages.error(request, 'No tienes permiso para realizar esta acción.')
        return redirect('inicio')
    
    try:
        remedio = Remedio.objects.get(id=remedio_id)
    except Remedio.DoesNotExist:
        messages.error(request, 'El remedio no existe.')
        return redirect('lista_remedios')
    
    if request.method == 'POST':
        form = FormRemedio(request.POST, instance=remedio)
        if form.is_valid():
            form.save()
            messages.success(request, f'Remedio {remedio.nombre_remedio} actualizado exitosamente.')
            return redirect('lista_remedios')
    else:
        form = FormRemedio(instance=remedio)
    
    return render(request, 'appVeterinaria/editar_remedio.html', {'form': form, 'remedio': remedio})

def eliminar_remedio(request, remedio_id):
    """Eliminar un remedio"""
    if not tiene_permiso(request, 'remedios'):
        messages.error(request, 'No tienes permiso para realizar esta acción.')
        return redirect('inicio')
    
    try:
        remedio = Remedio.objects.get(id=remedio_id)
    except Remedio.DoesNotExist:
        messages.error(request, 'El remedio no existe.')
        return redirect('lista_remedios')
    
    if request.method == 'POST':
        nombre = remedio.nombre_remedio
        remedio.delete()
        messages.success(request, f'Remedio {nombre} eliminado exitosamente.')
        return redirect('lista_remedios')
    
    return render(request, 'appVeterinaria/eliminar_remedio.html', {'remedio': remedio})

# ============================================================================
# CRUD COMPLETO PARA RAZAS
# ============================================================================

def editar_raza(request, raza_id):
    """Editar una raza existente"""
    if not tiene_permiso(request, 'razas'):
        messages.error(request, 'No tienes permiso para realizar esta acción.')
        return redirect('inicio')
    
    try:
        raza = Razas.objects.get(id=raza_id)
    except Razas.DoesNotExist:
        messages.error(request, 'La raza no existe.')
        return redirect('lista_razas')
    
    if request.method == 'POST':
        form = FormRazas(request.POST, instance=raza)
        if form.is_valid():
            form.save()
            messages.success(request, f'Raza {raza.nombre_raza} actualizada exitosamente.')
            return redirect('lista_razas')
    else:
        form = FormRazas(instance=raza)
    
    return render(request, 'appVeterinaria/editar_raza.html', {'form': form, 'raza': raza})

def eliminar_raza(request, raza_id):
    """Eliminar una raza"""
    if not tiene_permiso(request, 'razas'):
        messages.error(request, 'No tienes permiso para realizar esta acción.')
        return redirect('inicio')
    
    try:
        raza = Razas.objects.get(id=raza_id)
    except Razas.DoesNotExist:
        messages.error(request, 'La raza no existe.')
        return redirect('lista_razas')
    
    if request.method == 'POST':
        nombre = raza.nombre_raza
        raza.delete()
        messages.success(request, f'Raza {nombre} eliminada exitosamente.')
        return redirect('lista_razas')
    
    return render(request, 'appVeterinaria/eliminar_raza.html', {'raza': raza})
