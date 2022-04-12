from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import stack
# import db.session


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('You have been logged in!'))
            if stack.objects.filter(username=request.user).exists():
                return redirect('trading:home')
            else:
                print("New stack created for" + request.user.username)
                newstack = stack(username=request.user, stocks={"data": []})
                newstack.save()
                print(newstack)
                return redirect('trading:home')
        else:
            messages.success(request, ('Error logging in - please try again.'))
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
    
@login_required
def logout_user(request):
    logout(request)
    messages.success(request, ('You have been logged out!'))
    return redirect('accounts:login_user')