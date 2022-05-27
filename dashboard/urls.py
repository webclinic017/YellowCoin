from django.urls import path

from . import views
app_name = 'dashboard'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('trade_entry/', views.trade_entry, name='trade_entry'),
]
