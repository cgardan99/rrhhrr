from django.urls import include, path

from .views import TableroView, CandidatoView, EliminarTableroView, ComentarioView

urlpatterns = [
    path("tablero/", TableroView.as_view(), name="api_tablero"),
    path(
        "tablero/eliminar/<tablero_id>",
        EliminarTableroView.as_view(),
        name="eliminar_tablero",
    ),
    path("candidato/", CandidatoView.as_view(), name="api_candidato"),
    path("candidato/<candidato_id>/", CandidatoView.as_view(), name="detalle_candidato"),
    path("comentario/", ComentarioView.as_view(), name="api_comentario"),
]
