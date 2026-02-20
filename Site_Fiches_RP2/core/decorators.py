from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def owner_required(function):
    """Seul l'owner peut accéder"""
    def check_owner(user):
        if not user.is_authenticated:
            return False
        return user.is_owner
    
    decorator = user_passes_test(check_owner, login_url='home')
    return decorator(function)

def admin_or_owner_required(function):
    """Admin ou owner peuvent accéder"""
    def check_admin_or_owner(user):
        if not user.is_authenticated:
            return False
        return user.is_staff or user.is_owner
    
    decorator = user_passes_test(check_admin_or_owner, login_url='home')
    return decorator(function)