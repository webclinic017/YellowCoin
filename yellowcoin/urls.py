from django.contrib import admin
from django.urls import include,path
from . import views

urlpatterns = [
    path('' , views.index, name='index'),
    path('admin/', admin.site.urls),
    path('trading/', include('trading.urls')),
    path('accounts/', include('accounts.urls')),
]
