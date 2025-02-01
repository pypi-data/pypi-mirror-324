import logging
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.timezone import now
from .models import HoneypotAdminLog


def admin_honeypot(request):
    if request.method == 'POST':
        ip = get_client_ip(request)
        username = request.POST.get('username')
        password = request.POST.get('password')
        timestamp = now()

        login_attempt = HoneypotAdminLog.objects.create(ip=ip, username=username, password=password, timestamp=timestamp)

        return redirect('admin_honeypot') # Refresh page

    return render(request, 'django-security-tools/index.html')  # Render the honeypot login

def get_client_ip(request):
    """Get the client's IP address."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
