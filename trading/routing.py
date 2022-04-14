from django.urls import re_path
from . import consumer

ws_urlpatterns = [
    re_path(r'ws/stock/(?P<room_name>\w+)/$', consumer.StockConsumer.as_asgi()),
]