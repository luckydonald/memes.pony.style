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
from django.template import TemplateSyntaxError
from django.template.base import token_kwargs, Node
from django.template.loader import get_template
from django.template.loader_tags import construct_relative_path
from django.template.loaders import filesystem

# noinspection PyUnresolvedReferences
# from django.template.loaders.filesystem import Loader  # needed for settings.py

register = template.Library()


@register.tag(name='include_with')
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
    name_map = options.get('with', {})
    template_name = parser.compile_filter(template_name)  # "string" vs variable
    return IncludeWithNode(
        template_name=template_name, isolated_context=isolated_context, name_map=name_map, origin_template_name=parser.origin.template_name
    )
# end def


class IncludeWithNode(Node):
    def __init__(self, template_name, isolated_context, name_map, origin_template_name):
        self.template_name = template_name
        self.isolated_context = isolated_context
        self.name_map = name_map
        self.origin_template_name = origin_template_name
        super().__init__()
    # end def

    def render(self, context):
        """
        Ripped from IncludeNode
        """
        # Does this quack like a Template?
        template_name = self.template_name.resolve(context)
        template_name = construct_relative_path(self.origin_template_name, template_name)
        template = get_template(template_name)
        if not callable(getattr(template, 'render', None)):
            raise TypeError("Must have .render(...) method")
        # end def

        values = {
            name: var.resolve(context)
            for name, var in self.name_map.items()
        }
        if self.isolated_context:
            return template.render(context.new(values))
        with context.push(**values):
            return template.render(context)
        # end if
    # end def
# end class


class Loader(filesystem.Loader):
    pass
# end class

