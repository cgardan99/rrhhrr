from django.urls import include, path

from .views import InicioView, NuevoTableroView

urlpatterns = [
    path("", InicioView.as_view(), name="inicio"),
    path("nuevo_tablero", NuevoTableroView.as_view(), name="nuevo_tablero"),
]
