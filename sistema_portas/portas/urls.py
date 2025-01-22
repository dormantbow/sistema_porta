from django.urls import path
from . import views

urlpatterns = [
    path("portas/", views.listar_portas, name="listar_portas"),
    path("agendar/", views.agendar_porta, name="agendar_porta"),
]
