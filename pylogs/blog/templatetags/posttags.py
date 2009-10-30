#!/usr/bin/env python
from django.template import Library
from blog.models import Post,Category,Comments, POST_STATUS
from django.utils.dateformat import format
from blog.templatetags.themes import theme_template_url

register = Library()
def get_tagged_posts(tags,number_of_posts,exclude_id = None):
    '''get tagged related posts'''
    posts = []
    for tag in tags:        
        if len(posts) < number_of_posts:
            for p in tag.post_set.filter(post_type__iexact='post')[:number_of_posts-len(posts)]:
                if (not exclude_id or p.id != exclude_id) and p not in posts:
                    posts.append(p)                   
        else:
            break    
    return {'posts':posts}
register.inclusion_tag(['%s/blog/tags/related_posts.html' % theme_template_url(),
                        'blog/tags/related_posts.html'])(get_tagged_posts)

class archive:
    link = ''
    title = ''
    
def get_archivelist(context):
    '''
    get the month list which have posts
    ''' 
    months = Post.objects.dates('pubdate','month',order='DESC')
    archive_months = []    
    for mon in months:
        m = archive()
        m.link = "/" + format(mon,'Y/m') + "/"
        m.title = format(mon,'b,Y')
        archive_months.append(m)    
    return {'archive_months':archive_months}
register.inclusion_tag(['%s/blog/tags/archivelist.html' % theme_template_url(),
                        'blog/tags/archivelist.html'],
    takes_context=True)(get_archivelist)

def get_categories(context):  
    cats = Category.objects.all()
    return {'cats':cats}   
register.inclusion_tag(['%s/blog/tags/category.html' % theme_template_url(),
                        'blog/tags/category.html'], takes_context=True)(get_categories)


def get_latest_posts(context):
    '''
    get the top nav menus
    '''
    posts = Post.objects.filter(post_type__exact='post',
                                post_status__exact = POST_STATUS[0][0])[:5]    
    return {'posts':posts}    
register.inclusion_tag(['%s/blog/tags/recent_posts.html' % theme_template_url(),
                        'blog/tags/recent_posts.html'],
                        takes_context=True)(get_latest_posts)

def get_popular_posts(context):
    '''
    get the top 5 Popular posts
    '''
    posts = Post.objects.filter(post_type__exact='post',
                                post_status__exact = POST_STATUS[0][0]).order_by('-hits')[:5]    
    return {'posts':posts}    
register.inclusion_tag(['%s/blog/tags/recent_posts.html' % theme_template_url(),
                        'blog/tags/recent_posts.html'], 
                        takes_context=True)(get_popular_posts)

def get_latest_comments(context):
    '''get the top 5 comments'''
    comments = Comments.objects.filter(comment_approved__exact='1')[:5]
    return {'comments':comments}
register.inclusion_tag(['%s/blog/tags/recent_comments.html' % theme_template_url(),
                        'blog/tags/recent_comments.html'],
                        takes_context=True)(get_latest_comments)