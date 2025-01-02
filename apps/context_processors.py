from django.conf import settings

def cfg_assets_root(request):

    return { 
        'ASSETS_ROOT' : settings.ASSETS_ROOT,
        'LOCAL_MEDIA_URL' : settings.LOCAL_MEDIA_URL
    }
    # return { 'MEDIA_ROOT' : settings.MEDIA_ROOT }

