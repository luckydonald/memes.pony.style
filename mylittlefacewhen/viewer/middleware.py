import random
from datetime import datetime, timedelta

from django.http import HttpResponse
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.utils import deprecation
from django.utils.cache import add_never_cache_headers
from django.utils.html import strip_spaces_between_tags
from luckydonaldUtils.eastereggs.ponies import WAIFU


class ContentTypeMiddleware(object):
    def process_request(self, request):
        if request.method in ['PUT'] and request.META['CONTENT_TYPE'].count(";") > 0:
            request.META['CONTENT_TYPE'] = [c.strip() for c in request.META['CONTENT_TYPE'].split(";")][0]
        return None

# Opera supported .webp from ver 11.10


class RedirectIE9(deprecation.MiddlewareMixin):
    """
    Internet Explorer doesnt support pushstate history. This breaks links
    opened by IE, pasted by other browsers and we need to redirect IE to
    hashed url.
    """
    def process_request(self, request):
        if request.META.get("HTTP_USER_AGENT", "").find("MSIE 9.0") != -1 and request.path != "/" and not request.path.startswith("/api/"):
            to = ""
            if request.is_secure():
                to += "https://"
            else:
                to += "http://"
            to += request.get_host() + "/#" + request.path[1:]

            return HttpResponseRedirect(to)
        else:
            return None


class RedirectDomain(deprecation.MiddlewareMixin):
    """
    I want everyone to use the main domain so 302 for "www." subdomain and for
    mlfw.info shortener.
    """
    def process_request(self, request):
        host = request.META.get("HTTP_HOST")
        if not host:
            return None
        if host not in ("memes.pony.style", "127.0.0.1", "127.0.0.1:8000", "localhost", "localhost:8000"):  # TODO: env
            url = "https://memes.pony.style" + request.path     # TODO: env
            return HttpResponsePermanentRedirect(url)


class SpacelessHTML(deprecation.MiddlewareMixin):
    def process_response(self, request, response):
        if 'text/html' in response['Content-Type']:
            response.content = strip_spaces_between_tags(response.content)
        return response


class Style(deprecation.MiddlewareMixin):
    def process_request(self, request):
        pony = request.GET.get("best_pony")
        if pony:
            try:
                request.COOKIES.pop("best_pony")
            except:
                pass
        else:
            pony = request.COOKIES.get("best_pony")

        if pony not in WAIFU:
            request.best_pony = random.choice(WAIFU)
        else:
            request.best_pony = pony
        return None

    def process_response(self, request, response):
        pony = request.COOKIES.get("best_pony", "")
        if pony not in WAIFU:
            expires = datetime.utcnow() + timedelta(days=365)
            try:
                best_pony = request.best_pony
            except:
                return response
            response.set_cookie("best_pony", value=best_pony, expires=expires, httponly=True)
        return response


class NoCache(deprecation.MiddlewareMixin):
    def process_response(self, request, response):
        add_never_cache_headers(response)
        return response


class AllowPieforkMiddleware(deprecation.MiddlewareMixin):
    def process_request(self, request):
        if request.method == 'OPTIONS':
            return HttpResponse()

    def process_response(self, request, response):
        if request.META.get('HTTP_ORIGIN'):
            response['Access-Control-Allow-Origin'] = request.META.get('HTTP_ORIGIN')
            response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, DELETE, PUT, PATCH'
            response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
