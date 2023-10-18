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

    def to_json(self):
        return {
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "puesto_deseado": self.puesto_deseado,
            "fecha_de_nacimiento": str(self.fecha_de_nacimiento),
            "agregado_el": str(self.agregado_el),
            "estado_civil": self.estado_civil,
            "email": self.email,
            "telefono": self.telefono,
            "fase_actual": self.fase_actual.pk,
            "comentarios": [x.to_json() for x in self.comentario_set.all()],
            "archivos": [x.to_json() for x in self.archivo_set.all()],
        }


class Comentario(models.Model):
    comentado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE)
    texto = models.TextField()
    creado_el = models.DateTimeField(auto_now_add=True)

    def to_json(self):
        return {
            "pk": self.pk,
            "tipo": "COMENTARIO",
            "comentado_por": self.comentado_por.username,
            "fase": self.fase.nombre,
            "texto": self.texto,
            "creado_el": str(self.creado_el),
        }


class Archivo(models.Model):
    subido_por = models.ForeignKey(User, on_delete=models.CASCADE)
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE)
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    creado_el = models.DateTimeField(auto_now_add=True)
    archivo = models.FileField(upload_to="")
    descripcion = models.CharField(max_length=100)

    def to_json(self):
        return {
            "pk": self.pk,
            "tipo": "ARCHIVO",
            "subido_por": self.subido_por.username,
            "fase": self.fase.nombre,
            "descripcion": self.descripcion,
            "archivo": self.archivo,
            "creado_el": str(self.creado_el),
        }
