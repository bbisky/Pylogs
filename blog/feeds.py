#coding=utf-8
import urlparse

from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist
from django.utils.feedgenerator import Atom1Feed
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.syndication.feeds import Feed


from models import Post,Category
from utils import html
from blog import models
from django.conf import settings
from templatetags.config import site_name, site_subtitle, author_name

global_title_template = 'blog/feeds/title.html'
global_description_template = 'blog/feeds/description.html'
global_item_copyright = site_name()
global_title = site_name()
global_description = site_subtitle()
domain = Site.objects.get_current().domain

class RssLatestPosts(Feed):
    """
    RSS Feed of the most recently published posts.    
    """    
    title_template = global_title_template
    description_template = global_description_template
    item_copyright = global_item_copyright
    title = global_title
    link = "/"
    description = global_description
    author = "Pylogs RSS generator"
    
    
    def items(self):
        posts = Post.objects.filter(post_type__iexact='post',
                                    post_status__iexact = models.POST_STATUS[0][0])[:15]
        for post in posts:
            post.content = html.htmlDecode(post.content)
        return posts
    
    def item_author_name(self, item):
        return author_name()
    
    def item_link(self, item):      
        return urlparse.urljoin(domain, item.get_absolute_url())       
    
    def item_pubdate(self, item):
        return item.pubdate
    
class AtomLatestPosts(Feed):
    """
    Atom Feed of the most recently published posts.    
    """
    feed_type = Atom1Feed
    title_template = global_title_template
    description_template = global_description_template
    item_copyright = global_item_copyright
    title = global_title
    link = "/"
    subtitle = global_description
    author = "Pylogs ATOM generator"
        
    def items(self):
        posts = Post.objects.filter(post_type__iexact='post',
                                    post_status__iexact = models.POST_STATUS[0][0])[:15]
        for post in posts:
            post.content = html.htmlDecode(post.content)
        return posts

    def item_author_name(self, item):
        return author_name()   
    
    def item_link(self, item):        
        return  urlparse.urljoin(domain, item.get_absolute_url())
    
    def item_pubdate(self, item):
        return item.pubdate
