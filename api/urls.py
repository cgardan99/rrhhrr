from django.urls import include, path

from .views import TableroView

urlpatterns = [
    path("tablero/", TableroView.as_view(), name="api_tablero"),
]
