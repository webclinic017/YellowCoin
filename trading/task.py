from celery import shared_task
from views import dataB


@shared_task(bind=True)
def update_data(self, stocks):
    temp = dataB(stocks)
    print("done")