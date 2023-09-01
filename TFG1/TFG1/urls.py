"""
URL configuration for TFG1 analisis.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoanalisis.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from myapp import views

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),    
    path('', views.index, name='index'),
    path('myapp/', include('myapp.urls')), #Página principal
    path('registro/', views.registro, name='registro'),
    path('iniciarsesion/', views.iniciarsesion, name='iniciarsesion'),
    path('welcome/', views.welcome, name='welcome'),
    path('upload_files/', views.upload_files, name='upload_files'),
    path('vista_previa/', views.vista_previa, name='vista_previa'),
    #path('mandarArchivo/', views.mandarArchivo, name='mandarArchivo'),
    path('logout/', views.logout_view, name='logout'),
    path('resultados/', views.resultados, name='resultados')
]
