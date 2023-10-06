from applications.models import Fase, Tablero
from rest_framework import serializers


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
        return Tablero(**validated_data)


class FaseSerializer(serializers.Serializer):
    tablero_id = serializers.IntegerField()
    nombre = serializers.CharField(max_length=100)
    descripcion = serializers.CharField()
    creado_el = serializers.DateTimeField()
    ultima_actualizacion = serializers.DateTimeField()
    activa = serializers.BooleanField(default=True)
    es_primer_fase = serializers.BooleanField(default=False)
    siguiente_fase = serializers.IntegerField()

    class Meta:
        fields = (
            "tablero_id",
            "nombre",
            "descripcion",
            "creado_el",
            "ultima_actualizacion",
            "activa",
            "es_primer_fase",
            "siguiente_fase",
        )
        Model = Fase


