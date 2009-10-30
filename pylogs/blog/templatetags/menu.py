#coding=utf-8
from django.template import Library
from django.utils.translation import ugettext as _

from blog.models import Post
from blog.templatetags.themes import theme_template_url
register = Library()

def get_menus(context):
    '''
    get the top nav menus
    '''
    pages = Post.objects.filter(post_type__exact='page',post_status__iexact = 'publish').order_by('menu_order')   
    menus = [] 
    if pages:
        for page in pages:           
            menus.append(page)
    return {'menus':menus}    
register.inclusion_tag(['%s/blog/tags/menu.html' % theme_template_url(),
                        'blog/tags/menu.html'],
                        takes_context=True)(get_menus)
