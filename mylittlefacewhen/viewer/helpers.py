from typing import Dict

from somewhere import SUPPORT_EMAIL_ADDRESS

UPDATED = 17


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def standard_r2r(function):
    from django.http import HttpResponse
    from django.shortcuts import render

    def inner(request, *args, **kwargs):
        response = function(request, *args, **kwargs)
        try:
            to_template: Dict
            template, to_template = response
        except ValueError:
            pass
        else:
            response = template
        # end try

        if isinstance(response, HttpResponse):
            return response

        to_template.update({"updated": UPDATED})

        return render(
            request=request,
            template_name=template,
            context=to_template,
        )

    return inner


def get_meta(request, title=None, description=None):
    from django.conf import settings
    meta = {
        "path": request.path,
        "static_prefix": settings.STATIC_URL,
        "title": "Pony Reaction Pictures",
        "description": "Express yourself with ponies",
        "default_image": settings.STATIC_URL + "cheerilee-square-300.png",
        "support_mail_address": SUPPORT_EMAIL_ADDRESS,
    }

    if title is not None:
        meta["title"] = title
    if description is not None:
        meta["description"] = description

    return meta
