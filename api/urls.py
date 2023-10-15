from django.urls import include, path

from .views import TableroView, CandidatoView, EliminarTableroView

urlpatterns = [
    path("tablero/", TableroView.as_view(), name="api_tablero"),
    path(
        "tablero/eliminar/<tablero_id>",
        EliminarTableroView.as_view(),
        name="eliminar_tablero",
    ),
    path("candidato/", CandidatoView.as_view(), name="api_candidato"),
]
