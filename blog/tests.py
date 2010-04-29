import unittest

from datetime import datetime
from django.core.urlresolvers import reverse
from django.test.testcases import TestCase
from django.test.client import Client

from models import Tags, Category, Comments, Post, Links,POST_TYPES,POST_STATUS,COMMENT_APPROVE_STATUS,POST_COMMENT_STATUS

class ModelTest(TestCase):
    def setUp(self):
        self.tag = Tags.objects.create(name='tag1',slug='tag1')
        self.category = Category.objects.create(name='category1',desc='category1 desc',enname='category1')
        self.now = datetime.now()
        self.post = Post.objects.create(title='post1',
                                        content='content1',                                        
                                        post_name = 'post1',
                                        post_type = POST_TYPES[0][0],
                                        post_status = POST_STATUS[0][0], 
                                        post_parent = None,
                                        pubdate = self.now,
                                        hits = 0,
                                        menu_order = 0, 
                                        comment_status = POST_COMMENT_STATUS[0][0], 
                                        comment_count = 1
                                        )
        self.post.category.add(self.category)
        self.post.tags.add(self.tag)
        
        self.page = Post.objects.create(title='page1',
                                        content='page content1',
                                        #category=[self.category],
                                        post_name = 'page1',
                                        post_type = POST_TYPES[1][0],
                                        post_status = POST_STATUS[0][0], 
                                        post_parent = None,
                                        pubdate = self.now,
                                        hits = 0,
                                        menu_order = 0, 
                                        comment_status = POST_COMMENT_STATUS[0][0], 
                                        comment_count = 1
                                        )
        
        self.comment = Comments.objects.create(post = self.post,
                                                comment_author = 'deng',
                                                comment_author_email = 'bbisky@sohu.com',
                                                comment_author_url = 'http://oteam.cn',
                                                comment_author_IP = '127.0.0.1',
                                                comment_date = self.now,
                                                comment_content = 'comment1 content',
                                                comment_approved = COMMENT_APPROVE_STATUS[1][0],
                                                comment_agent = 'unknown',
                                                user_id = 0 )
        
        self.link = Links.objects.create(link_url = 'http://oteam.cn',
                                         link_title ='pylogs',
                                         link_desc = 'a opensource blog system based Python and Django.',
                                         link_image = None,
                                         link_order = 0,
                                         link_updated = self.now)
        self.client = Client()
        
    def test_models(self):
        '''
        Models testing
        '''
        self.assertEquals(self.tag.name,'tag1')
        self.assertEquals(self.tag.get_absolute_url(),'/tags/tag1/')
        
        self.assertEquals(self.category.get_absolute_url(),reverse('category_name',kwargs={'catname':self.category.enname}))
        self.assertEquals(self.post.get_absolute_url(),'/%s/%s/%s/post1/'%(self.now.year,self.now.month,self.now.day))
        
        self.assertEquals(self.page.get_absolute_url(),'/page1/')
        
        self.assertEqual(self.comment.post,self.post)
        self.assertEqual(self.link.link_url,'http://oteam.cn')
    
    
    def test_index(self):
        '''Views testing: "index"'''        
        response = self.client.get('/')
        self.failUnlessEqual(response.status_code,200)
        self.failUnlessEqual(response.context['tab'],'home')
        self.failUnlessEqual(len(response.context['ol'].object_list),1)        
    
    def test_view_post_name(self):
        '''Views testing: single post'''        
        response = self.client.get(self.post.get_absolute_url())
        self.failUnlessEqual(response.status_code,200)
        self.failUnlessEqual(response.context[0]['post'],self.post)
        
    def test_view_page(self):
        '''Views testing: single page'''
        response = self.client.get(self.page.get_absolute_url())
        self.failUnlessEqual(response.status_code,200)
        self.failUnlessEqual(response.context[0]['post'],self.page)
        
    def test_view_category(self):
        '''Views testing: category list'''
        response = self.client.get(self.category.get_absolute_url())
        self.failUnlessEqual(response.status_code,200)
        self.failUnlessEqual(len(response.context['ol'].object_list),1)
    
    def test_view_tags(self):
        '''Views testing: tags list'''
        response = self.client.get(self.tag.get_absolute_url())
        self.failUnlessEqual(response.status_code,200)
        self.failUnlessEqual(len(response.context['ol'].object_list),1)
    
    def test_view_dateposts(self):
        '''Views testing: dateposts list'''
        response = self.client.get('/%s/%s/%s/'%(self.now.year,self.now.month,self.now.day))
        self.failUnlessEqual(response.status_code,200)
        self.failUnlessEqual(len(response.context['ol'].object_list),1)
        
    def test_feeds(self):
        '''Feed testing'''
        response = self.client.get(reverse('feeds',kwargs={'url':'rss'}))
        self.failUnlessEqual(response.status_code,200)
        self.assertEqual(response['Content-Type'],'application/rss+xml')
        self.assertContains(response,self.post.title)
        response = self.client.get(reverse('feeds',kwargs={'url':'atom'}))
        self.failUnlessEqual(response.status_code,200)
        self.assertEqual(response['Content-Type'],'application/atom+xml')
        self.assertContains(response,self.post.title)
        
    def test_post_comment(self):
        '''Ajax post comment testing'''        
        #post comment
        self.client.defaults = {'REMOTE_ADDR':'127.0.0.1','HTTP_USER_AGENT':'Python UnitTest/0.1'}
        response = self.client.post(reverse('post_comment',kwargs={'postid':self.post.id}),{'author':'deng',
                                                           'email':'bbisky@sohu.com',
                                                           'url':'http://oteam.cn',
                                                           'content':'this is a test comment',
                                                           'vcode': self.client.session.get('vcode','')},
                                                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.failUnlessEqual(response.status_code,200)        
        self.assertEqual(response['Content-Type'],'application/x-javascript')
        self.assertContains(response,'success')
        #test post comment count
        comments = self.post.get_comments()
        self.assertEquals(len(comments),1)  
