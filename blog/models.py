#coding=utf-8
from datetime import datetime

from django.utils.translation import ugettext as _
from django.db import models
from django.core.urlresolvers import reverse


#post types
POST_TYPES = (    
    ('post', _('Post')),
    ('page', _('Page')),
    )
#post status
POST_STATUS = (   
    ('publish', _('Published')),
    ('draft', _('Draft')),
    ('private', _('Private')),
)
#comment approve status
COMMENT_APPROVE_STATUS = (
    ('0',_('UnApproved')),
    ('1',_('Approved')),
    ('spam',_('Spam'))
)
#comment status
POST_COMMENT_STATUS = (
    ('open',_('Allow Comments')),
    ('closed',_('Disallow Comments')),
    ('registered',_('Allow Register Comments')),
    ('free',_('No Need Approve')),
)

#markup lanaguage choices
MARKUP_LANGUAGE_CHOICES = (
    ("html",_("HTML")),
    ("markdown",_("MARKDOWN")),
)

class Tags(models.Model):
    '''Tag entity'''
    name = models.CharField(_('Name'),unique=True,max_length=64)
    slug = models.CharField(_('Slug'),max_length=255,unique=True,blank=True,
                            help_text=_('Use as url'))
    reference_count = models.IntegerField(_('Reference count'),default=0,
                                          editable=False)
    
    def save(self,force_insert=False, force_update=False):
        #override save
        if not self.slug:
            #replace the special char of name as slug
            self.slug = self.name.replace(' ','-')
            self.slug = self.slug.replace(u'　','-')
            self.slug = self.slug.replace('.','')
        super(Tags,self).save(force_insert,force_update)
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self): 
        return reverse('tagname', kwargs={'tagname':self.slug})    
    
    class Meta:
        #ordering = ['-pubdate']
        verbose_name=_('Tag')
        verbose_name_plural = _('Tags')
    
    class Admin():
        list_display = ('name','slug','reference_count')
        search_fields = ['name']
 
class Category(models.Model):
    '''category entity'''    
    name = models.CharField(_('Name'),max_length=255,unique=True)
    desc = models.CharField(_('Description'),max_length=1024)
    enname = models.CharField(_('English name'),max_length=255,
                              unique=True,blank=True,help_text=_('Use as url'))
    def save(self,force_insert=False, force_update=False):
        #override save
        if not self.enname:
	    #replace the space of title
            self.enname = self.name.replace(' ','-')
            self.enname = self.enname.replace(u'　','-')
            self.enname = self.enname.replace('.','')
        super(Category,self).save(force_insert, force_update)
        
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        if self.enname:
            return reverse('category_name', kwargs={'catname':self.enname})
        else:
            return reverse('category_id', kwargs={'catid':self.id})
    
    class Meta:
        ordering=['name']
        verbose_name=_('Category')
        verbose_name_plural = _('Categories')
    
    class Admin:
        list_display = ('name','desc')
        search_fields = ['name']

class Post(models.Model):    
    '''Post Entity'''
    title = models.CharField(_('Title'),max_length=255)
    #add markup field sql: ALTER TABLE blog_post ADD `markup` VARCHAR(64) NOT NULL DEFAULT 'html';
    markup = models.CharField(_('Markup'),max_length=64,choices=MARKUP_LANGUAGE_CHOICES,default="html")  
    content = models.TextField(_('Content'))
    category = models.ManyToManyField(Category,null=True,blank=True,
                                      verbose_name=_('Category'))
    post_name = models.CharField(_('Post name'),max_length=255,unique=True,
                                 blank=True,help_text=_('Use as url'))
    post_type = models.CharField(_('Post type'),max_length=10,default='post',
                                 choices=POST_TYPES)
    post_status = models.CharField(_('Post status'),max_length=10,default='publish',
                                   choices = POST_STATUS)
    post_parent = models.ForeignKey('self',null=True, blank=True,
                                    related_name='child_set',
                                    limit_choices_to = {'post_type__exact':POST_TYPES[1][0]},
                                    verbose_name=_('Parent page'))
    pubdate = models.DateTimeField(_('Pubdate'),auto_now_add=True)
    hits = models.IntegerField(_('Hits'),default=0,editable=False)
    menu_order = models.IntegerField(_('Menu order'),default=0)
    comment_status = models.CharField(_('Comment status'),
                                      default= POST_COMMENT_STATUS[0][0],
                                      max_length=10,choices = POST_COMMENT_STATUS)
    comment_count = models.IntegerField(_('Comment count'),default=0,editable=False)
    tags = models.ManyToManyField(Tags,null=True,blank=True,
                                  verbose_name=_('Tags'),related_name='post_set')
    
    def save(self,force_insert=False, force_update=False):
        #override save
        if not self.post_name:
            #replace the space of title
            self.post_name = self.title.replace(' ','-')
            self.post_name = self.post_name.replace(u'　','-')
            self.post_name = self.post_name.replace('.','')

        super(Post,self).save(force_insert, force_update)
    
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        #if is page,return page url
        if self.post_type == POST_TYPES[1][0]:
            return reverse('page',args=[self.post_name])
        else:
            if self.post_name:
                return reverse('post_name',args=[self.pubdate.year,
                                          self.pubdate.month,
                                          self.pubdate.day,
                                          self.post_name])
            else:
                return reverse('post_id',args=[self.pubdate.year,
                                          self.pubdate.month,
                                          self.pubdate.day,
                                          self.id])
            
    def get_cat_str(self):
        '''return the categories string '''
        cats = self.category.all()
        cat_strs = ''
        for cat in cats:
            if len(cat_strs)>0:
                cat_strs += ','
            cat_strs += cat.name
        return cat_strs
    get_cat_str.short_description = _('Post categories')    
 
    def get_comments(self):
        '''Get post or page approved comments'''
        comments = self.comments_set.filter(comment_approved__iexact=
                                            COMMENT_APPROVE_STATUS[1][0]).order_by('id')       
        return comments
    
    
    class Meta:
        ordering = ['-pubdate']
        verbose_name=_('Post')
        verbose_name_plural = _('Posts')
       
    class Admin:
        list_display = ('title','get_cat_str','pubdate','hits')
        search_fields = ['title']
        list_filter =('post_type','category')
        js = (
                '/media/js/tiny_mce/tiny_mce.js',
                '/media/js/admin_textarea.js',
            )

class Comments(models.Model):
    '''user comments'''
    post = models.ForeignKey(Post,verbose_name=_('Post'),
                             related_name='comments_set')
    comment_author = models.CharField(_('Author'),max_length=32)
    comment_author_email = models.EmailField(verbose_name=_('Email'))
    comment_author_url = models.URLField(_('URL'),null=True,blank=True,
                                         verify_exists=False)
    comment_author_IP = models.IPAddressField(verbose_name=_('IP'),null=True,
                                              editable=False)
    comment_date = models.DateTimeField(verbose_name=_('Pubdate'),
                                        auto_now_add=True,editable=False)
    comment_content = models.TextField(verbose_name=_('Content'))
    comment_approved = models.CharField(_('Approve status'),max_length=32,
                                        choices=COMMENT_APPROVE_STATUS)
    comment_agent = models.CharField(_('User agent info'),editable=False,
                                     max_length=255,null=True)
    user_id = models.IntegerField(_('UserId'),editable=False,null=True)
    
    def save(self,force_insert=False, force_update=False):                     
        super(Comments,self).save(force_insert, force_update)
        #if comment is approved,update related post comment count
        if self.comment_approved == str(COMMENT_APPROVE_STATUS[1][0]):          
            self.post.comment_count = \
            self.post.comments_set.filter( \
            comment_approved__iexact=COMMENT_APPROVE_STATUS[1][0]).count()
            self.post.save() 
        
    def __unicode__(self):
        return self.comment_author_email
   
    def get_absolute_url(self):        
        return self.post.get_absolute_url() + '#comment'
    
    class Meta:
        ordering = ['-comment_date']
        verbose_name=_('Comment')
        verbose_name_plural = _('Comments')

    class Admin:
        list_filter =('comment_approved',)
        list_display = ('comment_author','comment_author_email',
                        'comment_date','comment_approved')
        search_fields = ['comment_author']

class Links(models.Model):
    '''Friend links entity'''
    link_url = models.URLField(_('URL'),verify_exists=False)
    link_title = models.CharField(_('Title'),unique=True,max_length=32)
    link_desc = models.CharField(_('Description'),null=True,blank=True,
                                 max_length=255)
    link_image = models.CharField(_('Image'),null=True,blank=True,
                                  max_length=255)
    link_order = models.IntegerField(_('Order'),default=0,
                                     help_text=_('Minimal at front'))
    link_updated = models.DateTimeField(_('Pubdate'),auto_now=True,
                                        editable=False)
    
    def __unicode__(self):
        return self.link_title
   
    def get_absolute_url(self):        
        return self.link_url
    
    class Meta:
        ordering = ['link_order']
        verbose_name=_('Link')
        verbose_name_plural = _('Links')    

class Setting(models.Model):
    '''blog setting options'''
    setting_name = models.CharField(_('SettingName'), max_length=32, unique=True)
    setting_value = models.CharField(_('SettingValue'),max_length=255, null=True, blank=True)
    setting_desc = models.CharField(_('Description'),null=True,blank=True,
                                 max_length=255)
    
    def __unicode__(self):
	return self.setting_name
    
    class Meta:
	verbose_name = _('Setting')
	verbose_name_plural = _('Settings')
	
