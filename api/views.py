from api.serializers import FaseSerializer, TableroSerializer
from rest_framework import views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import datetime as dt


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
                else:
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
