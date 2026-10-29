from django.contrib import admin
from django.urls import path

from academia import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("alunos/", views.lista_alunos, name="lista_alunos"),
]