# def force_default_language_middleware(get_response):
#     # """
#     #     Ignore Accept-Language HTTP headers

#     #     This will force the I18N machinery to always choose settings.LANGUAGE_CODE
#     #     as the default initial language, unless another one is set via sessions or cookies

#     #     Should be installed *before* any middleware that checks request.META['HTTP_ACCEPT_LANGUAGE'],
#     #     namely django.middleware.locale.LocaleMiddleware
#     #     """

#     def middleware(request):
#         if 'HTTP_ACCEPT_LANGUAGE' in request.META:
#             del request.META['HTTP_ACCEPT_LANGUAGE']

#         print "middleware"
#         response = get_response(request)

#         return response

#     return middleware

class DefaultLanguageMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if 'HTTP_ACCEPT_LANGUAGE' in request.META:
            del request.META['HTTP_ACCEPT_LANGUAGE']

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response