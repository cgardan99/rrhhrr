from django.urls import include, path

from .views import (
    TableroView,
    CandidatoView,
    EliminarTableroView,
    ComentarioView,
    ArchivoView,
    CambiarFaseView,
    EliminarElementoView,
)

urlpatterns = [
    path("tablero/", TableroView.as_view(), name="api_tablero"),
    path(
        "tablero/eliminar/<tablero_id>",
        EliminarTableroView.as_view(),
        name="eliminar_tablero",
    ),
    path("candidato/", CandidatoView.as_view(), name="api_candidato"),
    path(
        "candidato/<candidato_id>/", CandidatoView.as_view(), name="detalle_candidato"
    ),
    path("comentario/", ComentarioView.as_view(), name="api_comentario"),
    path("archivo/", ArchivoView.as_view(), name="api_archivo"),
    path(
        "cambiar_fase/<candidato_id>/<fase_id>/",
        CambiarFaseView.as_view(),
        name="api_cambiar_fase",
    ),
    path(
        "eliminar/<tipo>/<pk>/",
        EliminarElementoView.as_view(),
        name="api_cambiar_fase",
    ),
]
