from django.urls import path
from . import views

urlpatterns = [
            path('', views.index, name='index'),
            path('addsong/', views.addsong, name='addsong'),
            path('updateleader/', views.updateleader, name='updateleader'),
            path('leaderboard/', views.LeaderBoardView.as_view(), name='leaderboard'),
        ]
