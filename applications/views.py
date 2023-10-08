from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.shortcuts import render

from applications.models import Tablero


# Create your views here.
class InicioView(LoginRequiredMixin, TemplateView):
    template_name = "applications/inicio.html"


class TableroListView(ListView):
    model = Tablero
    template_name = "applications/lista_tableros.html"


class TableroView(LoginRequiredMixin, TemplateView):
    template_name = "applications/tablero.html"


class NuevoTableroView(LoginRequiredMixin, TemplateView):
    template_name = "applications/nuevo_tablero.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["modo_edicion"] = False
        return context
