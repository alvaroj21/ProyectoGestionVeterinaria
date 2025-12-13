from django.contrib import admin
from appVeterinaria.models import ClienteVet, Mascota, CitaMascota, Veterinario, Razas, Remedio

# Personalización del encabezado del panel de administración
admin.site.site_header = "Veterinaria Amigos de Patas Admin"
admin.site.site_title = "Panel de Administración"
admin.site.index_title = "Bienvenido al Panel de Control"

# Personalización visual (inyectando CSS personalizado)
from django.template.response import TemplateResponse

class CustomAdminSite(admin.AdminSite):
    site_header = "Veterinaria Amigos de Patas Admin"
    site_title = "Panel de Administración"
    index_title = "Bienvenido al Panel de Control"

    def each_context(self, request):
        context = super().each_context(request)
        context['admin_css'] = 'css/admin_custom.css'
        return context

    def index(self, request, extra_context=None):
        context = {
            **self.each_context(request),
            'title': self.index_title,
        }
        return TemplateResponse(request, 'admin/index.html', context)

# ----------------------------
class ClienteVetAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'telefono', 'email', 'rut', 'direccion']

admin.site.register(ClienteVet, ClienteVetAdmin)

# ----------------------------
class MascotaAdmin(admin.ModelAdmin):
    list_display = ['nombre_mascota', 'sexo_mascota', 'edad_mascota', 'especie_mascota', 'raza_mascota']

admin.site.register(Mascota, MascotaAdmin)

# ----------------------------
class CitaMascotaAdmin(admin.ModelAdmin):
    list_display = ['dato_cliente', 'dato_mascota', 'fecha_cita', 'motivo_cita', 'mostrar_remedios', 'veterinario']

    def mostrar_remedios(self, obj):
        return ", ".join([r.nombre for r in obj.remedio_cita.all()])

    mostrar_remedios.short_description = 'Remedios'

admin.site.register(CitaMascota, CitaMascotaAdmin)

# ----------------------------
class VeterinarioAdmin(admin.ModelAdmin):
    list_display = ['nombre_veterinario', 'especialidad', 'email', 'telefono', 'direccion']

admin.site.register(Veterinario, VeterinarioAdmin)

# ----------------------------
class RazaPerroAdmin(admin.ModelAdmin):
    list_display = ['animal', 'raza', 'nombre_cientifico', 'edad_aprox_vida', 'alimentacion', 'tiempo_paseo']
    search_fields = ['raza', 'animal']
    list_filter = ['raza', 'animal']

admin.site.register(Razas, RazaPerroAdmin)

# ----------------------------
class RemedioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'animal', 'frecuencia']
    search_fields = ['nombre', 'animal']
    list_filter = ['animal']
    fieldsets = (
        (None, {
            'fields': ('nombre', 'animal')
        }),
        ('Detalles del remedio', {
            'fields': ('uso_recomendado', 'frecuencia'),
            'description': 'Información adicional sobre el remedio veterinario.'
        }),
    )
admin.site.register(Remedio)



