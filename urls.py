from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

from blog import feeds
from blog.models import Post

admin.autodiscover()

# Info for feeds.
feed_dict = {    
    'rss': feeds.RssLatestPosts,
    'atom': feeds.AtomLatestPosts,
    }
info_dict = {    
    'queryset': Post.objects.all(),
    'date_field': 'pubdate',
}
urlpatterns = patterns('',                       
                       ('^admin/(.*)', admin.site.root),                                                  
                        url(r'^utils/vcode/$', 'utils.validatecode.get_validatecode_img', name='validate_code'),  
                        )

# url for static
if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': settings.STATIC_PATH}),                    
                            )
#urls for wap
urlpatterns += patterns('',                        
                        (r'^wap/*',include('wap.urls')),
                        #wap pre url
                        url(r'wap','wap.views.index',name='wap_pre'),
                        )

# url for todo
urlpatterns += patterns('todo.views',
                        url(r'^todo/$','index',name='todo'),
                        (r'^todo/task/add/', 'task_add'),
                        (r'^todo/task/done/','task_done'),
                        (r'^todo/task/undone/','task_undone'),
                        (r'^todo/task/delete/','task_del'),
                        (r'^todo/project/add/', 'project_add'),
                        (r'^todo/project/delete/', 'project_del'),
                        (r'^todo/project/change_type/', 'project_chg_type'),                        
                        )

# url for filemanager
urlpatterns += patterns('',                        
                        url(r'^filemanager/(?P<p>.*)$','filemanager.views.index',name='filemanager'),                        
                        )
#urls for feeds
urlpatterns += patterns('',
                        url(r'^feeds/(?P<url>.*)/$','django.contrib.syndication.views.feed',
                        {'feed_dict':feed_dict},name='feeds'),
                        url(r'^rpc/$','blog.rpc.call',name='rpc'),
                        )
# urls for blog
urlpatterns += patterns('blog.views',  
                        (r'^$', 'index'),
                        #tags
                        url(r'^tags/$','tags',name='tags'),
                        url(r'^tags/(?P<tagname>.*)/$','tags',name='tagname'),                        
                        url(r'^(\d{4})/(\d{1,2})/(\d{1,2})/(?P<postname>[^/]+)/$','post',name='post_name'),
                        url(r'^post/(?P<postid>(\d+))/comment$','post_comment',name='post_comment'),
                        #category view
                        url(r'^category/(?P<catid>\d+)/$','categoryView',name="category_id"),
                        url(r'^category/(?P<catname>[^/]+)/$','categoryView',name="category_name"),                        
                        (r'^(?P<year>\d{4})/(?P<month>(\d{1,2})?)/?(?P<date>(\d{1,2})?)/?$','dateposts'),
                        url(r'^(?P<pagename>\w+)/$','page',name='page'),                        
                        )
