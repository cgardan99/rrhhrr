from django.urls import include, path

from .views import InicioView, NuevoTableroView, TableroListView, TableroView

urlpatterns = [
    path("", InicioView.as_view(), name="inicio"),
    path("lista_tableros", TableroListView.as_view(), name="lista_tableros"),
    path("tablero/<pk>/", TableroView.as_view(), name="tablero"),
    path("nuevo_tablero", NuevoTableroView.as_view(), name="nuevo_tablero"),
]
