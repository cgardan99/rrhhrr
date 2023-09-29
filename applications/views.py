from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render


# Create your views here.
class InicioView(LoginRequiredMixin, TemplateView):
    template_name = "applications/inicio.html"


class ListaTablerosView(LoginRequiredMixin, TemplateView):
    template_name = "applications/lista_tableros.html"


class TableroView(LoginRequiredMixin, TemplateView):
    template_name = "applications/tablero.html"


class NuevoTableroView(LoginRequiredMixin, TemplateView):
    template_name = "applications/nuevo_tablero.html"
