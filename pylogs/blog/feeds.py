#!/usr/bin/env python
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

current_site = Site.objects.get_current().name

global_title_template = 'blog/feeds/title.html'
global_description_template = 'blog/feeds/description.html'
global_item_copyright = getattr(settings,"FEED_COPYRIGHT",'Pylogs by Sky')
global_title = getattr(settings,"FEED_GLOBAL_TITLE","Pylogs: Latest Posts")
global_description = getattr(settings,"FEED_GLOBAL_DESCRIPTION","logging your life...")
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
        return getattr(settings,"FEED_POST_AUTHOR_NAME",'Sky') #item.author.username
    
    def item_link(self, item):
        blog_url_prefix = getattr(settings,"FEED_BLOG_URL_PREFIX","/")
        return  urlparse.urljoin(blog_url_prefix, item.get_absolute_url())
    
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
        return getattr(settings,"FEED_POST_AUTHOR_NAME",'Sky') #item.author.username    
    
    def item_link(self, item):
        blog_url_prefix = getattr(settings,"FEED_BLOG_URL_PREFIX","/")
        return  urlparse.urljoin(blog_url_prefix, item.get_absolute_url())
    
    def item_pubdate(self, item):
        return item.pubdate
