from django.contrib import admin
from django.urls import path
from app import views

#from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('gerarScript/', views.gerarScript, name='gerarScript'),
    path('sobre/', views.sobre, name='about'),
    path('tutorial/', views.tutorial, name='tutorial'),
    path('ferramentas/', views.ferramentas, name='ferramentas'),
]
