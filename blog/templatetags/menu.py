#coding=utf-8
from django import template
from django.template import Library,Context
from django.utils.translation import ugettext as _

from blog.models import Post
from blog.templatetags.themes import theme_template_url

register = Library()   
class SiteMenu(template.Node):
    def __init__(self,menus):
        self.menus = menus
    def render(self, context):
        t = template.loader.select_template([theme_template_url() + '/blog/tags/menu.html',
                                             'blog/tags/menu.html'])
        context['menus'] = self.menus
        return t.render(context)

def do_get_menus(parser,token):
    pages = Post.objects.filter(post_type__exact='page',
                                post_status__iexact = 'publish',
                                post_parent__isnull = True).order_by('menu_order')   
    menus = [] 
    if pages:
        for page in pages:           
            menus.append(page)    
    return SiteMenu(menus)
register.tag('site_menu',do_get_menus)
    