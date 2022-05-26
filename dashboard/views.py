from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    current_user = request.user
    return render(request, 'dashboard_trades.html', {'current_user': current_user})
