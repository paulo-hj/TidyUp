from django.contrib import admin
from django.urls import path
from app import views

#from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('generate_script/', views.generate_script, name='generate_script'),
    path('sobre/', views.sobre, name='about'),
    path('tutorial/', views.tutorial, name='tutorial'),
    path('ferramentas/', views.ferramentas, name='ferramentas'),
]
