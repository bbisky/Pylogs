#!/usr/bin/env python
from django.template import Library
from blog.models import Post,Category,Comments, POST_STATUS,POST_TYPES
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
register.inclusion_tag('blog/tags/related_posts.html')(get_tagged_posts)

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
register.inclusion_tag('blog/tags/archivelist.html',
    takes_context=True)(get_archivelist)

def get_categories(context):  
    cats = Category.objects.all()
    return {'cats':cats}   
register.inclusion_tag('blog/tags/category.html',
                       takes_context=True)(get_categories)


def get_latest_posts(context):
    '''
    get the top nav menus
    '''
    posts = Post.objects.filter(post_type__exact='post',
                                post_status__exact = POST_STATUS[0][0])[:5]    
    return {'posts':posts}    
register.inclusion_tag('blog/tags/recent_posts.html',
                        takes_context=True)(get_latest_posts)

def get_popular_posts(context):
    '''
    get the top 5 Popular posts
    '''
    posts = Post.objects.filter(post_type__exact='post',
                                post_status__exact = POST_STATUS[0][0]).order_by('-hits')[:5]    
    return {'posts':posts}    
register.inclusion_tag('blog/tags/recent_posts.html', 
                        takes_context=True)(get_popular_posts)

def get_latest_comments(context):
    '''get the top 5 comments'''
    comments = Comments.objects.filter(comment_approved__exact='1')[:5]
    return {'comments':comments}
register.inclusion_tag('blog/tags/recent_comments.html',
                        takes_context=True)(get_latest_comments)

def get_child_pages(context,pageid):
    '''
    get child pages
    '''
    pages = Post.objects.filter(post_type__exact=POST_TYPES[1][0],
                                    post_status__exact = POST_STATUS[0][0],
                                    post_parent__id__exact = pageid).order_by('menu_order')
    return {'childpages':pages}
register.inclusion_tag('blog/tags/childpages.html',
                         takes_context=True)(get_child_pages)
 

def paginator(ol,querystr=''):
    '''
    paginator tag
    @ol:        the Paginator page object
    @querystr:  additional querystring attach to pager url link
    '''
    pag = ol.paginator
    page_range = [1,2,3,4,5,6,7,8,9,10]
    if len(pag.page_range) >10:
        if ol.number >= 10:
            page_range = [1,'...']
            end = ol.number+8            
            if end > pag.page_range[-1]:
                end = pag.page_range[-1]+1            
            for p in range(ol.number-2,end):
                page_range.append(p)
        if page_range[-1] < pag.page_range[-1]:
            page_range.append('...')
            
    else:
        page_range = pag.page_range
    return {'ol':ol,'page_range':page_range,'querystr':querystr}
register.inclusion_tag('paginator.html')(paginator)