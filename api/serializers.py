from applications.models import Fase, Tablero, Candidato
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class TableroSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=100)
    modificado_por = serializers.IntegerField()
    creado_el = serializers.DateTimeField()
    ultima_actualizacion = serializers.DateTimeField()

    class Meta:
        fields = (
            "nombre",
            "modificado_por",
            "creado_el",
            "ultima_actualizacion",
        )
        Model = Tablero

    def create(self, validated_data):
        validated_data["modificado_por"] = User.objects.get(
            pk=validated_data["modificado_por"]
        )
        return Tablero(**validated_data)


class FaseSerializer(serializers.Serializer):
    tablero = serializers.IntegerField()
    nombre = serializers.CharField(max_length=100)
    descripcion = serializers.CharField()
    creado_el = serializers.DateTimeField()
    ultima_actualizacion = serializers.DateTimeField()
    activa = serializers.BooleanField(default=True)
    es_primer_fase = serializers.BooleanField(default=False)

    class Meta:
        fields = (
            "tablero",
            "nombre",
            "descripcion",
            "creado_el",
            "ultima_actualizacion",
            "activa",
            "es_primer_fase",
            "siguiente_fase",
        )
        Model = Fase

    def create(self, validated_data):
        validated_data["tablero"] = Tablero.objects.get(pk=validated_data["tablero"])
        return Fase(**validated_data)


class CandidatoSerializer(serializers.Serializer):
    tablero_asignado = serializers.IntegerField()
    nombres = serializers.CharField(max_length=100)
    apellidos = serializers.CharField(max_length=100)
    puesto_deseado = serializers.CharField(max_length=100)
    fecha_de_nacimiento = serializers.DateField()
    estado_civil = serializers.CharField(max_length=10)
    email = serializers.EmailField()
    telefono = serializers.IntegerField()

    class Meta:
        fields = (
            "tablero_asignado",
            "nombres",
            "apellidos",
            "puesto_deseado",
            "fecha_de_nacimiento",
            "estado_civil",
            "email",
            "telefono",
        )
        Model = Fase

    def create(self, validated_data):
        tablero = Tablero.objects.get(pk=validated_data["tablero_asignado"])
        validated_data["tablero_asignado"] = tablero
        candidato = Candidato(**validated_data)
        candidato.fase_actual = tablero.fase_set.get(es_primer_fase=True)
        candidato.save()
        return candidato       
