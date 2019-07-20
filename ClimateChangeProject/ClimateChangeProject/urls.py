"""Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,include
from app import views

urlpatterns = [
	path('app/', include('app.urls')),
    path('admin/',views.admin,name='admin'),
    path('charts/',views.charts,name='charts'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('add_temperature/', views.add_temperature, name='add-temperature'),
    path('delete_temperature/', views.delete_temperature, name='delete_temperature'),
    path('update_temperature/', views.update_temperature, name='update_temperature'),
]
