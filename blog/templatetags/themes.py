#!/usr/bin/env python
from django.template import TemplateSyntaxError,TemplateDoesNotExist,Library
from django.conf import settings
from django.template.loader_tags import ExtendsNode
from django.template.loader import select_template,get_template, get_template_from_string, find_template_source

from config import theme

register = Library()

class ThemeExtendsNode(ExtendsNode):
    must_be_first = False
    def __init__(self, nodelist, parent_name, parent_name_expr, template_dirs=None):
        self.nodelist = nodelist
        self.parent_name, self.parent_name_expr = parent_name, parent_name_expr
        self.template_dirs = template_dirs
        
    def get_parent(self, context):
        if self.parent_name_expr:
            self.parent_name = self.parent_name_expr.resolve(context)
        parent = theme_template_url() +'/'+ self.parent_name        
        if not parent:
            error_msg = "Invalid template name in 'extends' tag: %r." % parent
            if self.parent_name_expr:
                error_msg += " Got this from the '%s' variable." % self.parent_name_expr.token
            raise TemplateSyntaxError, error_msg
        try:
            source, origin = find_template_source(parent, self.template_dirs)
        except TemplateDoesNotExist:
            raise TemplateSyntaxError, "Template %r cannot be extended, because it doesn't exist" % parent
        else:
            return get_template_from_string(source, origin, parent)
        #
        #try:
        #    return select_template(parent)
        #except TemplateDoesNotExist:
        #    raise TemplateSyntaxError, "Template %r cannot be extended, because it doesn't exist" % parent

def do_theme_extends(parser,token):
    """
    template based extends
    """
    bits = token.contents.split()
    if len(bits) != 2:
        raise TemplateSyntaxError, "'%s' takes one argument" % bits[0]
    parent_name, parent_name_expr = None, None
    if bits[1][0] in ('"', "'") and bits[1][-1] == bits[1][0]:
        parent_name = bits[1][1:-1]
    else:
        parent_name_expr = parser.compile_filter(bits[1])
    nodelist = parser.parse()    
    if nodelist.get_nodes_by_type(ExtendsNode):
        raise TemplateSyntaxError,"'%s' cannot appear more than once in the same template" % bits[0]
    return ThemeExtendsNode(nodelist,parent_name,parent_name_expr)
register.tag('theme_extends',do_theme_extends)

def get_theme_name():
    """
    get the theme name from settings.py
    """
    theme_name = theme()
    if theme_name:
        return theme_name
    else:
        return 'default'   

def media_url():
    """
    Returns the common media url
    """    
    return getattr(settings,'MEDIA_URL','')
    
media_url = register.simple_tag(media_url)


def theme_media_url():
    """
    Returns the themes media url
    """   
    return media_url() + '/themes/'+ get_theme_name()
    
register.simple_tag(theme_media_url)

def theme_template_url():
    """
    Returns the themes template url
    """
    url = 'themes/'+ get_theme_name()
    print 'theme_template_url:%s' % url
    return url