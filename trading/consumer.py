from channels.generic.websocket import WebsocketConsumer
import json
from random import randint
from time import sleep, time

from psycopg2 import connect
from .views import dataB

stocksA = ["INTC:NASDAQ","AAPL:NASDAQ","MSFT:NASDAQ","GOOG:NASDAQ","AMZN:NASDAQ","ITC:NSE","IDEA:NSE","YESBANK:NSE","BHEL:NSE","RELIANCE:NSE","TCS:NSE","HDFC:NSE","ICICIBANK:NSE","MARUTI:NSE","WIPRO:NSE"]
stocks = ["ITC:NSE","AAPL:NASDAQ","RELIANCE:NSE","TCS:NSE","HDFC:NSE","MRF:NSE"]
dataArrFinal=[]
threads=[]
counter = 0

class wsConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        temp = dataB(stocks)
        temp.sort(key=lambda x:x[1])
        self.send(json.dumps({'data': temp}))
        
    def disconnect(self, close_code):
        self.close()
        
    def receive(self, text_data):
        print(text_data)
        if(text_data=="update"):
            temp = dataB(stocks)
            temp.sort(key=lambda x:x[1])
            for i in range(0,len(temp)):
                temp[i][1] = str(randint(1,100))
                temp[i][2] = str(randint(1,100))
                temp[i][3] = str(randint(1,100))
            self.send(json.dumps({'data': temp}))
        
        