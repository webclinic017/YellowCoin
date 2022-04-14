from .views import dataB
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
from asgiref.sync import async_to_sync,sync_to_async
from django_celery_beat.models import PeriodicTask,IntervalSchedule

stocksA = ["INTC:NASDAQ","AAPL:NASDAQ","MSFT:NASDAQ","GOOG:NASDAQ","AMZN:NASDAQ","ITC:NSE","IDEA:NSE","YESBANK:NSE","BHEL:NSE","RELIANCE:NSE","TCS:NSE","HDFC:NSE","ICICIBANK:NSE","MARUTI:NSE","WIPRO:NSE"]
stocks = ["ITC:NSE","AAPL:NASDAQ","RELIANCE:NSE","TCS:NSE","HDFC:NSE","MRF:NSE"]

class StockConsumer(AsyncWebsocketConsumer):
    @sync_to_async
    def addToCeleryBeat(self, stocks):
        task = PeriodicTask.objects.filter(name="every-10-seconds")
        if len(task) > 0:
            task = task.first()
            args = json.loads(task.args)
            args = args[0]
            for stock in stocks:
                if stock not in args:
                    args.append(stock)
            task.args = json.dumps([args])
            task.save()
            print("Task created 1")
        else:
            schedule,created = IntervalSchedule.objects.get_or_create(every=10, period=IntervalSchedule.SECONDS)
            task = PeriodicTask.objects.create(name="every-10-seconds", task="trading.tasks.stock_update", interval = schedule, args=json.dumps([stocks]))
            print("Task created 2 ")




    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'stock_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Parse query string argument
        query_string = parse_qs(self.scope['query_string'].decode())
        print(query_string)
        stocks = query_string['stock']
        await self.addToCeleryBeat(stocks)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'stock_update',
                'message': message
            }
        )

    # Receive message from room group
    async def send_stock_update(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))
        