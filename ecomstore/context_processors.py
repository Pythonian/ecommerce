from ecomstore import settings


def ecomstore(request):
    """ context processor for the site templates """
    return {
        'site_name': 'Modern Musician',
        'meta_keywords': 'Music, instruments, sheet music, musician',
        'meta_description': 'Modern Musician is an online supplier of \
             instruments, sheet music, and other accessories for musicians',
        'analytics_tracking_id': settings.ANALYTICS_TRACKING_ID,
        'request': request
    }
