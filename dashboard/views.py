from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    current_user = request.user
    if current_user.username == 'admin':
        return render(request, 'dashboard_trades.html', {'current_user': current_user})
    else:
        return render(request, 'user_dashboard_trades.html', {'current_user': current_user})


@login_required
def trade_entry(request):
    if current_user.is_superuser:
        current_user = request.user
        return render(request, 'dashboard_trade_entry.html', {'current_user': current_user})
