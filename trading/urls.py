from django.urls import path

from . import views

app_name = 'trading'
urlpatterns = [
    path('', views.home, name='home'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('trades/', views.trades, name='trades'),
    path('data/', views.dataDisplay, name='dataDisplay'),
    path('websocket/', views.ws, name='ws'),
]