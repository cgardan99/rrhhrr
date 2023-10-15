from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tablero(models.Model):
    nombre = models.CharField(max_length=100)
    modificado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    creado_el = models.DateTimeField()
    ultima_actualizacion = models.DateTimeField(auto_now_add=True)


class Fase(models.Model):
    tablero = models.ForeignKey(Tablero, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    creado_el = models.DateTimeField()
    ultima_actualizacion = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)
    es_primer_fase = models.BooleanField(default=False)
    siguiente_fase = models.ForeignKey(
        "self", blank=True, null=True, on_delete=models.CASCADE
    )


class Candidato(models.Model):
    ESTADOS_CIVILES = (
        ("SOLTERO", "Soltero"),
        ("CASADO", "Casado"),
        ("DIVORCIADO", "Divorciado"),
        ("VIUDO", "Viudo"),
    )
    tablero_asignado = models.ForeignKey(Tablero, on_delete=models.CASCADE)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    puesto_deseado = models.CharField(max_length=100)
    fecha_de_nacimiento = models.DateField()
    agregado_el = models.DateTimeField(auto_now_add=True)
    estado_civil = models.CharField(
        max_length=10, choices=ESTADOS_CIVILES, default="SOLTERO"
    )
    email = models.EmailField()
    telefono = models.IntegerField()
    fase_actual = models.ForeignKey(Fase, on_delete=models.CASCADE)


class Comentario(models.Model):
    comentado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE)
    texto = models.TextField()
    creado_el = models.DateTimeField()


class Archivo(models.Model):
    subido_por = models.ForeignKey(User, on_delete=models.CASCADE)
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE)
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    creado_el = models.DateTimeField()
    archivo = models.FileField(upload_to="")
    descripcion = models.CharField(max_length=100)
