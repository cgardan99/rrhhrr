from api.serializers import (
    FaseSerializer,
    TableroSerializer,
    CandidatoSerializer,
    ComentarioSerializer,
    ArchivoSerializer,
)
from rest_framework import views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import datetime as dt

from applications.models import Tablero, Candidato, Fase, Archivo, Comentario

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

    def get(self, response, candidato_id, format=None):
        try:
            candidato = Candidato.objects.get(pk=candidato_id)
        except Candidato.DoesNotExist:
            candidato = None
        return Response(
            {"messages": [], "candidato": candidato.to_json()}
            if candidato
            else {"messages": ["Candidato no Encontrado"]},
            status=status.HTTP_404_NOT_FOUND if not candidato else status.HTTP_200_OK,
        )

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

    def patch(self, response, format=None):
        mensajes = []
        error = False
        try:
            candidato = Candidato.objects.get(
                pk=self.request.data["current_candidato_id"]
            )
            candidato.nombres = self.request.data["nombres"]
            candidato.apellidos = self.request.data["apellidos"]
            candidato.puesto_deseado = self.request.data["puesto_deseado"]
            candidato.fecha_de_nacimiento = self.request.data["fecha_de_nacimiento"]
            candidato.email = self.request.data["email"]
            candidato.telefono = self.request.data["telefono"]
            candidato.estado_civil = self.request.data["estado_civil"]
            candidato.save()
        except Candidato.DoesNotExist:
            error = True
            mensajes.append(
                "Por favor, verifica la integridad de los datos del candidato."
            )
        return Response(
            {"messages": mensajes},
            status=status.HTTP_201_CREATED
            if not error
            else status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, response, candidato_id, format=None):
        try:
            candidato = Candidato.objects.get(pk=candidato_id)
            candidato.delete()
        except Candidato.DoesNotExist:
            candidato = None
        return Response(
            {"messages": []}
            if candidato
            else {"messages": ["Candidato no Encontrado"]},
            status=status.HTTP_404_NOT_FOUND if not candidato else status.HTTP_200_OK,
        )


class ComentarioView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, response, format=None):
        mensajes = []
        error = False
        comentario_serializer = ComentarioSerializer(data=self.request.data)
        if comentario_serializer.is_valid():
            candidato = comentario_serializer.save()
            candidato.save()
        else:
            error = True
            mensajes.append(
                "Por favor, verifica la integridad de los datos del comentario."
            )
            for tipo, mensaje in comentario_serializer.errors.items():
                mensajes.append(f"{tipo}, {mensaje[0]}")
        return Response(
            {"messages": mensajes},
            status=status.HTTP_201_CREATED
            if not error
            else status.HTTP_400_BAD_REQUEST,
        )


class ArchivoView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, response, format=None):
        mensajes = []
        error = False
        archivo_serializer = ArchivoSerializer(data=self.request.data)
        if archivo_serializer.is_valid():
            archivo = archivo_serializer.save()
            archivo.save()
        else:
            error = True
            mensajes.append(
                "Por favor, verifica la integridad de los datos del comentario."
            )
            for tipo, mensaje in archivo_serializer.errors.items():
                mensajes.append(f"{tipo}, {mensaje[0]}")
        return Response(
            {"messages": mensajes},
            status=status.HTTP_201_CREATED
            if not error
            else status.HTTP_400_BAD_REQUEST,
        )


class CambiarFaseView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, response, candidato_id, fase_id, format=None):
        try:
            candidato = Candidato.objects.get(pk=candidato_id)
            fase = Fase.objects.get(pk=fase_id)
            candidato.fase_actual = fase
            candidato.save()
        except (Candidato.DoesNotExist, Fase.DoesNotExist):
            candidato = None
            fase = None
        return Response(
            {"messages": []}
            if (candidato and fase)
            else {"messages": ["Fase y/o Candidato no Encontrado"]},
            status=status.HTTP_404_NOT_FOUND if not candidato else status.HTTP_200_OK,
        )


class EliminarElementoView(views.APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, response, tipo, pk, format=None):
        try:
            elemento = (
                Comentario.objects.get(pk=pk)
                if tipo == "comentario"
                else Archivo.objects.get(pk=pk)
            )
            elemento.delete()
        except Candidato.DoesNotExist:
            elemento = None
        return Response(
            {"messages": []} if elemento else {"messages": ["Elemento no Encontrado"]},
            status=status.HTTP_404_NOT_FOUND if not elemento else status.HTTP_200_OK,
        )
