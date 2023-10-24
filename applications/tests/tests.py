from django.urls import reverse
from .utils import BaseTestCase
from .. import views


# Create your tests here.
class TestViewsTemplates(BaseTestCase):
    def setUp(self):
        super(TestViewsTemplates, self).setUp()

    def test_inicio_view_template_used(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("inicio"))
        self.assertTemplateUsed(response, "applications/inicio.html")

    def test_lista_tableros_view_template_used(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("lista_tableros"))
        self.assertTemplateUsed(response, "applications/lista_tableros.html")


class TestUrls(BaseTestCase):
    def setUp(self):
        super(TestUrls, self).setUp()

    def test_inicio_view_url(self):
        self.assertEqual(reverse("inicio"), "/tableros/")

    def test_lista_tableros_view_url(self):
        self.assertEqual(reverse("lista_tableros"), "/tableros/lista_tableros")

    def test_tablero_view_url(self):
        self.assertEqual(reverse("tablero", kwargs={"pk": 1}), "/tableros/tablero/1/")
