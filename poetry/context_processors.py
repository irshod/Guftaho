from django.conf import settings

def site_context(request):
    """Add common site data to all templates"""
    return {
        'site_name': 'Гуфтугў',
        'site_description': 'Китобхонаи шеъри тоҷик',
        'pagination_settings': getattr(settings, 'PAGINATION_SETTINGS', {}),
        'current_url': request.path,
    }