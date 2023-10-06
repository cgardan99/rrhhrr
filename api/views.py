from api.serializers import FaseSerializer, TableroSerializer
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import datetime as dt


# Create your views here.
class TableroView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, response):
        fases_del_tablero = self.request.data["fases"]
        nombre_del_tablero = self.request.data["nombre"]
        fecha_creacion = dt.datetime.utcnow()
        import pdb; pdb.set_trace()
        tablero_serializer = TableroSerializer()
        fase_serializer = FaseSerializer()
