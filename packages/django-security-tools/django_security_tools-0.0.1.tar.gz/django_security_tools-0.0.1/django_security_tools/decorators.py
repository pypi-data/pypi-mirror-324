from functools import wraps
import re

from .models import XSSPayload

def log_xss(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.method == 'POST':
            for key, value in request.POST.items():
                if re.search(r"<.*?script.*?>", value, re.IGNORECASE):
                    return HttpResponseBadRequest("XSS detected in form input.")
            return view_func(request, *args, **kwargs)
    return wrapper