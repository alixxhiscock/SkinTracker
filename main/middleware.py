from django.utils.cache import patch_cache_control

class CacheControl:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process the request before the view
        response = self.get_response(request)

        # Add cache headers to the response
        if request.path.startswith('/media/static'):  # Only for static files
            patch_cache_control(response, public=True, max_age=3600)  # Cache for 1 hour
        return response
