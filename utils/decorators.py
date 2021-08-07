from functools import wraps

from django.http import HttpResponseForbidden, HttpResponseNotAllowed

def authenticate_required(function):
    
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        return function(request, *args, **kwargs)
    
    return wrapper


def request_methods(allowed=[]):
    
    def decorator(function):

        @wraps(function)
        def wrapper(request, *args, **kwargs):
            if request.method not in allowed:
                return HttpResponseNotAllowed(allowed)
            return function(request, *args, **kwargs)
        
        return wrapper
    
    return decorator