from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Notification
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST



@login_required(login_url='login')
def index(request):
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False).count()
    return render(request, 'index.html', {'unread_notifications': unread_notifications})

# @login_required(login_url='login')
# def notification_list(request):
#     notifications = Notification.objects.filter(user=request.user).order_by("-created_at")
#     return render(request, 'notification_list.html', {'notifications': notifications})


@login_required(login_url='login')
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by("-created_at")

    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        mark_notification_as_read(request.user, notification_id)

    return render(request, 'notification_list.html', {'notifications': notifications})

@require_POST
def mark_notification_as_read(request):
    notification_id = request.POST.get('notification_id')
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)

    # Update is_read to True
    Notification.objects.filter(id=notification_id).update(is_read=True)

    # Redirect to the notification_details page with the updated notification
    return redirect('notification_details', notification_id=notification_id)

def notification_details(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    return render(request, 'notification_details.html', {'notification': notification})

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            user = User.objects.create_user(username=username, password=password1)
            login(request, user)
            return redirect('index')

    return render(request, 'signup.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

