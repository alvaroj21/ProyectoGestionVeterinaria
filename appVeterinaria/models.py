from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import (
    MinValueValidator, MaxValueValidator,
    EmailValidator, RegexValidator,
    MinLengthValidator, MaxLengthValidator
)

# ============================================
# MODELO USUARIO - SISTEMA DE AUTENTICACIÓN
# ============================================
class Usuario(models.Model):
    ROLES_CHOICES = [
        ('Administrador', 'Administrador'),
        ('Veterinario', 'Veterinario'),
    ]
    
    username = models.CharField(max_length=45, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=15, blank=True)
    nombre_completo = models.CharField(max_length=100)
    rol = models.CharField(max_length=45, choices=ROLES_CHOICES)

    def __str__(self):
        return f"{self.username} - {self.rol}"
    
    class Meta:
        ordering = ['username']
        verbose_name = "Usuario del Sistema"
        verbose_name_plural = "Usuarios del Sistema"

# ------------------------------
class ClienteVet(models.Model):
    nombre = models.CharField(
        max_length=60,
        validators=[RegexValidator(
            regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
            message="El nombre solo puede contener letras y espacios.")]
    )
    apellido = models.CharField(
        max_length=45,
        validators=[RegexValidator(
            regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
            message="El apellido solo puede contener letras y espacios.")]
    )
    telefono = models.CharField(
        max_length=12,
        validators=[RegexValidator(
            regex=r'^\d{9,12}$',
            message="El teléfono debe contener entre 9 y 12 dígitos.")]
    )
    email = models.EmailField(
        max_length=80,
        unique=True,
        error_messages={"unique": "Este correo electrónico ya está registrado."}
    )
    rut = models.CharField(
        max_length=13,
        unique=True,
        validators=[RegexValidator(
            regex=r'^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$',
            message="El RUT debe tener el formato 12.345.678-K.")]
    )
    direccion = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(10, "La dirección debe tener al menos 10 caracteres.")]
    )
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# ------------------------------
class Remedio(models.Model):
    ANIMAL_CHOICES = [
        ('Perro', 'Perro'),
        ('Gato', 'Gato'),
        ('Otro', 'Otro'),
    ]

    nombre = models.CharField(max_length=50, unique=True)

    uso_recomendado = models.TextField(
        help_text="¿Para qué se recomienda este remedio?",
        default="No especificado",  # ✔ Valor por defecto
        blank=True,
        null=True
    )

    frecuencia = models.CharField(
        max_length=100,
        default='Una vez al día',
        blank=True,
        null=True,
        help_text="Ej: Cada 8 horas, una vez al día, etc."
    )

    animal = models.CharField(
        max_length=10,
        choices=ANIMAL_CHOICES,
        default='Perro',
        blank=True,
        null=True,
        help_text="Seleccione el tipo de animal al que va dirigido el remedio."
    )

    def __str__(self):
        return self.nombre

# ------------------------------
class CitaMascota(models.Model):
    MOTIVO_CHOICES = [
        ('control', 'Control'),
        ('urgencia', 'Urgencia'),
        ('rutina', 'Rutina'),
        ('primer_control', 'Primer Control'),
        ('operacion', 'Operación'),
    ]

    dato_cliente = models.ForeignKey('ClienteVet', on_delete=models.CASCADE)
    dato_mascota = models.ForeignKey('Mascota', on_delete=models.CASCADE)
    fecha_cita = models.DateField()
    motivo_cita = models.CharField(max_length=100, choices=MOTIVO_CHOICES)
    remedio_cita = models.ManyToManyField(Remedio, blank=True)  # Permite múltiples remedios o ninguno
    veterinario = models.ForeignKey('Veterinario', on_delete=models.SET_NULL, null=True, blank=True)

# ------------------------------
class Mascota(models.Model):
    SEXO_CHOICES = [('Macho', 'Macho'), ('Hembra', 'Hembra')]
    ESPECIE_CHOICES = [('Perro', 'Perro'), ('Gato', 'Gato'), ('Otro', 'Otro')]

    nombre_mascota = models.CharField(max_length=50)
    sexo_mascota = models.CharField(max_length=10, choices=SEXO_CHOICES)
    edad_mascota = models.IntegerField(
        validators=[
            MinValueValidator(0, message="Edad inválida."),
            MaxValueValidator(30, message="Edad inválida.")
        ]
    )
    especie_mascota = models.CharField(max_length=60, choices=ESPECIE_CHOICES)
    raza_mascota = models.CharField(max_length=30)

    def clean(self):
        if self.especie_mascota == 'Otro' and not self.raza_mascota.strip():
            raise ValidationError({'raza_mascota': 'Si la especie es "Otro", debes especificar qué animal es en la raza.'})

    def __str__(self):
        return self.nombre_mascota

# ------------------------------
class Veterinario(models.Model):
    ESPECIALIDAD_CHOICES = [
        ('Perros', 'Perros'),
        ('Gatos', 'Gatos'),
        ('Otros', 'Otros'),
    ]

    nombre_veterinario = models.CharField(
        max_length=100,
        unique=True,
        validators=[MinLengthValidator(2)],
        verbose_name="Nombres y Apellidos"
    )
    especialidad = models.CharField(
        max_length=100,
        choices=ESPECIALIDAD_CHOICES,
        verbose_name="Especialidad"
    )
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator()],
        verbose_name="Correo Electrónico"
    )
    telefono = models.CharField(
        max_length=15,
        unique=True,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="El número de teléfono debe tener entre 9 y 15 dígitos."
        )],
        verbose_name="Teléfono"
    )
    direccion = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(5)],
        verbose_name="Dirección"
    )

    def __str__(self):
        return self.nombre_veterinario

# ------------------------------
class Razas(models.Model):
    ANIMALES_OPCIONES = [('Perro', 'Perro'), ('Gato', 'Gato'), ('Otro', 'Otro')]

    animal = models.CharField(
        max_length=50,
        choices=ANIMALES_OPCIONES,
        default='Perro',
        help_text="Selecciona 'Perro', 'Gato' u 'Otro'."
    )
    raza = models.CharField(
        max_length=50,
        unique=True,
        help_text="Por ejemplo: 'Labrador' o 'Siamese'. Este nombre debe ser único."
    )
    nombre_cientifico = models.CharField(
        max_length=100,
        help_text="Por ejemplo: 'Canis lupus familiaris' o 'Felis catus'."
    )
    edad_aprox_vida = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(30)
        ],
        help_text="Edad aproximada de vida en años (máximo 30)."
    )
    alimentacion = models.CharField(max_length=255)
    tiempo_paseo = models.CharField(max_length=100)
    dato_curioso = models.TextField()
    recomendacion = models.TextField()

    def clean(self):
        if self.animal not in dict(self.ANIMALES_OPCIONES).keys():
            raise ValidationError({'animal': "Selecciona una opción válida ('Perro', 'Gato' o 'Otro')."})

    def __str__(self):
        return self.raza
