"""
Custom template loader, template and templatetag to handle mustache templates.

PystacheTemplate and Loader are pretty much copies of their parent classes
with one line modifications or so.

do_mustache allows template tags like
{% mustache "main.mustache" %}
and
{% mustache "main.mustache" main_vars %}

where main_vars is a dict containing variables needed by the mustache.

"""

from django import template
from django.conf import settings
from django.shortcuts import render
from django.template import Template, TemplateDoesNotExist, TemplateSyntaxError
# from django.template.base import TemplateEncodingError, TemplateDoesNotExist,
from django.template.base import Origin, token_kwargs
# from django.template.loader import make_origin
from django.template.loader import get_template
from django.template.loader_tags import IncludeNode, construct_relative_path
from django.template.loaders import filesystem
# from django.utils.encoding import smart_unicode
from pystache import render as pystache_render

from django.template.loaders.base import Loader
from django.template.engine import Engine

register = template.Library()


@register.tag('include_with')
def include_with(parser, token):
    """
    Load a template and render it with the current context. You can pass
    additional context using keyword arguments.

    Example::

        {% include "foo/some_include" %}
        {% include "foo/some_include" with bar="BAZZ!" baz="BING!" %}

    Use the ``only`` argument to exclude the current context when rendering
    the included template::

        {% include "foo/some_include" only %}
        {% include "foo/some_include" with bar="1" only %}
    """
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError(
            "%r tag takes at least one argument: the name of the template to "
            "be included." % bits[0]
        )
    template_name = bits[1]
    remaining_bits = bits[2:]
    options = {}
    while remaining_bits:
        option = remaining_bits.pop(0)
        if option in options:
            raise TemplateSyntaxError('The %r option was specified more '
                                      'than once.' % option)
        if option == 'with':
            value = token_kwargs(remaining_bits, parser, support_legacy=False)
            if not value:
                raise TemplateSyntaxError('"with" in %r tag needs at least '
                                          'one keyword argument.' % bits[0])
        elif option == 'only':
            value = True
        else:
            raise TemplateSyntaxError('Unknown argument for %r tag: %r.' %
                                      (bits[0], option))
        options[option] = value
    isolated_context = options.get('only', False)
    namemap = options.get('with', {})
    template_name = construct_relative_path(parser.origin.template_name, template_name)
    template = get_template(template_name)
    return template.render(context=namemap)
