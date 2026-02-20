from fiches.models import Server


def global_context(request):
    """Context processor pour rendre certaines variables disponibles partout"""
    context = {
        'all_servers': Server.objects.all().order_by('name') if request.user.is_authenticated else [],
    }
    return context