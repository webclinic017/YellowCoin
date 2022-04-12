from django.urls import path
from trading.consumer import wsConsumer

ws_urlpatterns = [
    path('ws/some_url/', wsConsumer.as_asgi()),
]