from django.urls import include, path

from .views import InicioView, NuevoTableroView, ListaTablerosView, TableroView

urlpatterns = [
    path("", InicioView.as_view(), name="inicio"),
    path("lista_tableros", ListaTablerosView.as_view(), name="tablero"),
    path("tablero", TableroView.as_view(), name="tablero"),
    path("nuevo_tablero", NuevoTableroView.as_view(), name="nuevo_tablero"),
]
