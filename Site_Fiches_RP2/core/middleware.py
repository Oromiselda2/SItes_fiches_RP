from .models import AuditLog

class AuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Code à exécuter avant la vue
        response = self.get_response(request)
        
        # Code à exécuter après la vue
        # Vous pouvez logger certaines actions automatiquement ici
        
        return response