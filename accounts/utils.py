from django.core.exceptions import PermissionDenied

def role_required(required_role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role != required_role:
                raise PermissionDenied  # Return 403 error if not authorized
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
