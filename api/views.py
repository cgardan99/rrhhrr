from api.serializers import FaseSerializer, TableroSerializer, CandidatoSerializer
from rest_framework import views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import datetime as dt

from applications.models import Tablero

from django.views.generic import View
from django.shortcuts import redirect


# Create your views here.
class TableroView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, response, format=None):
        mensajes = []
        error = False
        fases_del_tablero = self.request.data["fases"]
        nombre_del_tablero = self.request.data["nombre"]
        fecha_creacion = dt.datetime.utcnow()
        tablero_serializer = TableroSerializer(
            data={
                "nombre": nombre_del_tablero,
                "modificado_por": self.request.user.pk,
                "creado_el": fecha_creacion,
                "ultima_actualizacion": fecha_creacion,
            }
        )
        if tablero_serializer.is_valid():
            tablero = tablero_serializer.save()
            tablero.save()
            nro_fase = 1
            anterior_fase = None
            for fase in fases_del_tablero:
                fase_serializer = FaseSerializer(
                    data={
                        "tablero": tablero.pk,
                        "nombre": fase["titulo"],
                        "descripcion": fase["descripcion"],
                        "creado_el": dt.datetime.utcnow(),
                        "ultima_actualizacion": dt.datetime.utcnow(),
                        "activa": True,
                        "es_primer_fase": nro_fase == 1,
                    }
                )
                if fase_serializer.is_valid():
                    fase_actual = fase_serializer.save()
                    fase_actual.save()
                    if anterior_fase:
                        anterior_fase.siguiente_fase = fase_actual
                        anterior_fase.save()
                    anterior_fase = fase_actual
                else:
                    try:
                        tablero.delete()
                    except ValueError:
                        pass
                    error = True
                    mensajes.append("Por favor, verifica la integridad de las fases.")
                nro_fase += 1
        else:
            error = True
            mensajes.append(
                "Por favor, verifica la integridad de los datos del tablero."
            )
        return Response(
            {"messages": mensajes},
            status=status.HTTP_201_CREATED
            if not error
            else status.HTTP_400_BAD_REQUEST,
        )


class EliminarTableroView(View):
    def get(self, request, tablero_id):
        try:
            tablero_id = int(tablero_id)
        except (TypeError, ValueError):
            return redirect("lista_tableros")
        tablero = Tablero.objects.get(pk=tablero_id)
        tablero.delete()
        return redirect("lista_tableros")


class CandidatoView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, response, format=None):
        mensajes = []
        error = False
        candidato_serializer = CandidatoSerializer(data=self.request.data)
        if candidato_serializer.is_valid():
            candidato = candidato_serializer.save()
            candidato.save()
        else:
            error = True
            mensajes.append(
                "Por favor, verifica la integridad de los datos del candidato."
            )
            for tipo, mensaje in candidato_serializer.errors.items():
                mensajes.append(f"{tipo}, {mensaje[0]}")
        return Response(
            {"messages": mensajes},
            status=status.HTTP_201_CREATED
            if not error
            else status.HTTP_400_BAD_REQUEST,
        )
