A set of security tools for Django.

# Install the package:

`pip install django-security-tools`

# Add the app to INSTALLED_APPS:

```
INSTALLED_APPS = [
    # Other apps...
    'django_security_tools',
]
```

# Apply migrations:

`python manage.py migrate`

# Add secret admin route

urls.py
```
from django.contrib import admin
from django.urls import path
from django_security_tools.views import admin_honeypot

urlpatterns = [
    path('admin/', admin_honeypot, name='admin_honeypot'),
    path('secret/', admin.site.urls), # Your real admin
]
```