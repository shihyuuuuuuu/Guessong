from django.urls import path
from . import views

urlpatterns = [
            path('', views.index, name='index'),
            path('addsong/', views.addsong, name='addsong'),
        ]
