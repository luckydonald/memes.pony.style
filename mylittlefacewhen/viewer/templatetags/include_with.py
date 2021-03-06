"""
Custom template tag to let the template engine be chosen automatically.

{% include_with "foo/some_include" %}
{% include_with "foo/some_include" with bar="BAZZ!" baz="BING!" %}
{% include_with some_variable with bar=other_variable baz="BING!" %}
where main_vars is a dict containing variables needed by the mustache.

"""
import re

from django.template.base import token_kwargs, Node, kwarg_re
from django.template.loader import get_template
from django.template.loaders import filesystem
from django.template.library import Library
from django.template.exceptions import TemplateSyntaxError
from django.template.loader_tags import construct_relative_path
from luckydonaldUtils.holder import Holder

register = Library()
kwargs_re = re.compile(r"\*\*(?P<var>\w+)")


@register.tag(name='include_with')
def do_include_with(parser, token):
    """
    Load a template and render it with the current context. You can pass
    additional context using keyword arguments.

    Example::

        {% include_with "foo/some_include" %}
        {% include_with "foo/some_include" with bar="BAZZ!" baz="BING!" %}

    Use the ``only`` argument to exclude the current context when rendering
    the included template::

        {% include_with "foo/some_include" only %}
        {% include_with "foo/some_include" with bar="1" only %}

    This method is mostly ripped out of django.template.loader_tags.do_include(...).
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
    match = Holder()
    while remaining_bits:
        option = remaining_bits.pop(0)
        if option in options:
            raise TemplateSyntaxError('The %r option was specified more than once.' % option)
        if option == 'with':
            value = token_kwargs_better(remaining_bits, parser, support_legacy=False)
            if not value:
                raise TemplateSyntaxError('"with" in %r tag needs at least one keyword argument.' % bits[0])
        elif option == 'only':
            value = True
        elif match.set() and match.get().group(1):
            for key in parser.compile_filter(value):
                options[key] = value
        else:
            raise TemplateSyntaxError('Unknown argument for %r tag: %r.' %
                                      (bits[0], option))
        options[option] = value
    isolated_context = options.get('only', False)
    name_map = options.get('with', {})
    template_name = parser.compile_filter(template_name)  # resolve `"string"` vs `variable`
    return IncludeWithNode(  # as we don't have the context available we need to return object having `.render(context)`
        template_name=template_name, isolated_context=isolated_context,
        name_map=name_map, origin_template_name=parser.origin.template_name,
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
        Partly ripped from django.template.loader_tags.IncludeNode
        """
        template_name = self.template_name.resolve(context)
        template_name = construct_relative_path(self.origin_template_name, template_name)
        template = get_template(template_name)
        # Does this quack like a Template?
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


def token_kwargs_better(bits, parser, support_legacy=False):
    """
    Parse token keyword arguments and return a dictionary of the arguments
    retrieved from the ``bits`` token list.

    `bits` is a list containing the remainder of the token (split by spaces)
    that is to be checked for arguments. Valid arguments are removed from this
    list.

    `support_legacy` - if True, the legacy format ``1 as foo`` is accepted.
    Otherwise, only the standard ``foo=1`` format is allowed.

    There is no requirement for all remaining token ``bits`` to be keyword
    arguments, so return the dictionary as soon as an invalid argument format
    is reached.

    NEW:
    **kwargs

    """
    if not bits:
        return {}
    match = kwarg_re.match(bits[0])
    kwarg_format = match and match.group(1)
    kwargs_match = kwargs_re.match(bits[0])
    kwargs_format = kwargs_match and kwargs_match.group(1)
    if not kwarg_format and not kwargs_format:
        if not support_legacy:
            return {}
        if len(bits) < 3 or bits[1] != 'as':
            return {}
        # end if
    # end if

    kwargs = {}
    while bits:
        if kwarg_format or kwargs_format:
            match = kwarg_re.match(bits[0])
            kwargs_match = kwargs_re.match(bits[0])
            if not match or not match.group(1):
                return kwargs
            key, value = match.groups()
            del bits[:1]
        else:
            if len(bits) < 3 or bits[1] != 'as':
                return kwargs
            key, value = bits[2], bits[0]
            del bits[:3]
        kwargs[key] = parser.compile_filter(value)
        if bits and not kwarg_format:
            if bits[0] != 'and':
                return kwargs
            del bits[:1]
    return kwargs


