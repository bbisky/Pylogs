#coding=utf-8
from django.template import Library
from django.utils.translation import ugettext as _

from blog.models import Post, Category

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
register.inclusion_tag('wap/tags/menu.html',
                        takes_context=True)(get_menus)

def get_categories(context):
    cats = Category.objects.all()
    return {'cats':cats}   
register.inclusion_tag('wap/tags/categories.html', takes_context=True)(get_categories)

def get_tagged_posts(tags,number_of_posts,exclude_id = None):
    '''相关文章'''
    posts = []
    for tag in tags:        
        if len(posts) < number_of_posts:
            for p in tag.post_set.filter(post_type__iexact='post')[:number_of_posts-len(posts)]:
                if (not exclude_id or p.id != exclude_id) and p not in posts:
                    posts.append(p)                   
        else:
            break    
    return {'posts':posts}
register.inclusion_tag('wap/tags/related_posts.html')(get_tagged_posts)


