from ecomstore import settings


def ecomstore(request):
    """ context processor for the site templates """
    return {
            'site_name': settings.SITE_NAME,
            'meta_keywords': settings.META_KEYWORDS,
            'meta_description': settings.META_DESCRIPTION,
            'analytics_tracking_id': settings.ANALYTICS_TRACKING_ID,
            'request': request
            }
