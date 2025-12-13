from django import forms
from appVeterinaria.models import ClienteVet, Mascota, CitaMascota, Remedio, Veterinario, Razas

class FormClienteVet(forms.ModelForm):
    class Meta:
        model = ClienteVet
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del cliente'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido del cliente'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '912345678'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12.345.678-9'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección completa'}),
        }

class FormMascota(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = '__all__'
        widgets = {
            'nombre_mascota': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la mascota'}),
            'sexo_mascota': forms.Select(attrs={'class': 'form-control'}),
            'edad_mascota': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Edad en años'}),
            'especie_mascota': forms.Select(attrs={'class': 'form-control'}),
            'raza_mascota': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Raza de la mascota'}),
        }

class FormCitaMascota(forms.ModelForm):
    class Meta:
        model = CitaMascota
        fields = '__all__'
        widgets = {
            'dato_cliente': forms.Select(attrs={'class': 'form-control'}),
            'dato_mascota': forms.Select(attrs={'class': 'form-control'}),
            'fecha_cita': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'motivo_cita': forms.Select(attrs={'class': 'form-control'}),
            'remedio_cita': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'veterinario': forms.Select(attrs={'class': 'form-control'}),
        }

class FormRemedio(forms.ModelForm):
    class Meta:
        model = Remedio
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del remedio'}),
            'uso_recomendado': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción del uso'}),
            'frecuencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Cada 8 horas'}),
            'animal': forms.Select(attrs={'class': 'form-control'}),
        }

class FormVeterinario(forms.ModelForm):
    class Meta:
        model = Veterinario
        fields = '__all__'
        widgets = {
            'nombre_veterinario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo del veterinario'}),
            'especialidad': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56912345678'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección del consultorio'}),
        }

class FormRazas(forms.ModelForm):
    class Meta:
        model = Razas
        fields = '__all__'
        widgets = {
            'animal': forms.Select(attrs={'class': 'form-control'}),
            'raza': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Labrador'}),
            'nombre_cientifico': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Canis lupus familiaris'}),
            'edad_aprox_vida': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Edad en años'}),
            'alimentacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tipo de alimentación'}),
            'tiempo_paseo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 30 minutos diarios'}),
            'dato_curioso': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'recomendacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

