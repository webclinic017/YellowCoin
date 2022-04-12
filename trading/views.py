from tempfile import tempdir
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import stack
import requests
from bs4 import BeautifulSoup
import json
import threading
from django.utils import timezone

stocksA = ["INTC:NASDAQ","AAPL:NASDAQ","MSFT:NASDAQ","GOOG:NASDAQ","AMZN:NASDAQ","ITC:NSE","IDEA:NSE","YESBANK:NSE","BHEL:NSE","RELIANCE:NSE","TCS:NSE","HDFC:NSE","ICICIBANK:NSE","MARUTI:NSE","WIPRO:NSE"]
stocks = ["ITC:NSE","AAPL:NASDAQ","RELIANCE:NSE","TCS:NSE","HDFC:NSE","MRF:NSE","YESBANK:NSE"]
dataArrFinal=[]
threads=[]
counter = 0

def thread_function(i,stocks):
    global dataArrFinal
    dataArr=[]
    url="https://www.google.com/finance/quote/"+stocks[i]
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    price = soup.find('div', attrs={"class": "YMlKec fxKbKc"})
    data = soup.find_all('div', attrs={"class": "P6K39c"})
    dataArr.append(stocks[i])
    dataArr.append(price.text)
    for j in range(0,7):
        dataArr.append(data[j].text)
    dataArrFinal.append(dataArr)
    dataArr = []
    print(stocks[i])

def dataB(stocks):
    global dataArrFinal,threads
    for i in range(0,len(stocks)):
        t = threading.Thread(target=thread_function, args=(i,stocks))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    temp = dataArrFinal
    dataArrFinal = []
    threads = []
    return temp

def data(stock):
    global dataArrFinal
    dataArr=[]
    url="https://www.google.com/finance/quote/"+stock
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    price = soup.find('div', attrs={"class": "YMlKec fxKbKc"})
    data = soup.find_all('div', attrs={"class": "P6K39c"})
    dataArr.append(stock)
    dataArr.append(price.text)
    for j in range(0,7):
        dataArr.append(data[j].text)
    dataArrFinal=dataArr
    dataArr = []
    print(stock)
    temp = dataArrFinal
    dataArrFinal=[]
    return temp

@login_required
def home(request):
    current_user = request.user
    return render(request, 'home.html',{'current_user':current_user})


def ws(request):
    return render(request, 'websockets.html')

@login_required
def watchlist(request):
    obj = stack.objects.filter(username=request.user).first()
    print(timezone.localtime())
    # obj.stocks = {"data": []}
    # obj.save()
    temp = dataB(obj.stocks["data"])
    temp.sort(key=lambda x:x[1])
    current_user = request.user
    return render(request, 'watchlist.html',{'dataArrFinal':temp,'stocksA':stocksA,'current_user':current_user})

@login_required
def trades(request):
    obj = stack.objects.filter(username=request.user).first()
    print(timezone.localtime())
    temp = dataB(obj.stocks["data"])
    temp.sort(key=lambda x:x[1])
    current_user = request.user
    return render(request, 'trades.html',{'dataArrFinal':temp,'stocksA':stocksA,'current_user':current_user})


@login_required
def dataDisplay(request):
    #args = request.args
    apiKey = request.GET.get('apiKey')
    symbol = request.GET.get('symbol')
    todo = request.GET.get('todo')
    print(apiKey,symbol)
    if apiKey=="asdfghjkl":
        if symbol!=None:
            try:
                dataArrFinal=data(symbol)
                stringOutput = {"data":[]}
                x={
                    "name":str(dataArrFinal[0]),
                    "price":str(dataArrFinal[1]),
                    "priviousClose":str(dataArrFinal[2]),
                    "dayRange":str(dataArrFinal[3]),
                    "yearRange":str(dataArrFinal[4]),
                    "volume":str(dataArrFinal[5]),
                    "peRatio":str(dataArrFinal[6]),
                    "dividentYield":str(dataArrFinal[7]),
                    "stockExchange":str(dataArrFinal[8])
                }
                stringOutput["data"].append(x)
                return HttpResponse(json.dumps(stringOutput,indent=4), content_type="application/json")
            except:
                return HttpResponse('Invalid Symbol', content_type="application/json")
        else:
            userStack = stack.objects.filter(username=request.user.id).first()
            dataArrFinal=dataB(userStack.stocks["data"])
            stringOutput = {"data":[]}
            for i in dataArrFinal:
                x={
                    "name":str(i[0]),
                    "price":str(i[1]),
                    "priviousClose":str(i[2]),
                    "dayRange":str(i[3]),
                    "yearRange":str(i[4]),
                    "volume":str(i[5]),
                    "peRatio":str(i[6]),
                    "dividentYield":str(i[7]),
                    "stockExchange":str(i[8])
                }
                stringOutput["data"].append(x)
            return HttpResponse(json.dumps(stringOutput,indent=4), content_type="application/json")
    elif apiKey=="qwertyuiop":
        if todo=="get":
            print("get")
            try:
                dataArrFinal=data(symbol)
                stringOutput = {"data":[]}
                x={
                    "name":str(dataArrFinal[0]),
                    "price":str(dataArrFinal[1]),
                    "priviousClose":str(dataArrFinal[2]),
                    "dayRange":str(dataArrFinal[3]),
                    "yearRange":str(dataArrFinal[4]),
                    "volume":str(dataArrFinal[5]),
                    "peRatio":str(dataArrFinal[6]),
                    "dividentYield":str(dataArrFinal[7]),
                    "stockExchange":str(dataArrFinal[8])
                }
                stringOutput["data"].append(x)
                userStack = stack.objects.filter(username=request.user.id).first()
                userStack.stocks["data"].append(symbol)
                userStack.save()
                return HttpResponse(json.dumps(stringOutput,indent=4), content_type="application/json")
            except:
                return HttpResponse('Invalid Symbol', content_type="application/json")
        else:
            print(symbol)
            userStack = stack.objects.filter(username=request.user.id).first()
            userStack.stocks["data"].remove(symbol)
            userStack.save()
            return HttpResponse(json.dumps({}), content_type="application/json")
    else:
        return HttpResponse(HttpResponse('Invalid API Key', content_type="application/json"))