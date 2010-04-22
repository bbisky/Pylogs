#coding=utf-8
from django.template import Library
from django.conf import settings
from django.db.models.signals import post_save

from utils.version import get_svn_revision
from blog.models import Setting

register = Library()
VERSION = getattr(settings,'VERSION','unknown')

CONFIG_CACHE = {}
def get_version():
    """
    Returns the version as a human-format string.
    """
    v = '.'.join([str(i) for i in VERSION[:-1]])
    if VERSION[-1]: 	   
        v = '%s%s %s' % (v, VERSION[-1],get_svn_revision())
    return v

def site_name():
    '''site name'''    
    sitename = get_setting_section('SiteName')
    if sitename:
        return sitename
    else:
        return 'Pylogs'
    
def site_subtitle():
    '''
    get site subtitle
    '''
    subtitle = get_setting_section('SiteSubTitle')
    if subtitle:
        return subtitle
    else:
        return 'Simple is beautiful...'
    
def theme():
    '''
    get site theme settings
    '''    
    return get_setting_section('Theme')

def author_name():
    '''
    get site author name settings
    for rss atom feed use
    '''
    author = get_setting_section('AuthorName')
    if author:
        return author
    else:
        return 'Sky'
    
def site_description():
    '''
    get the site desctiption for html META element
    '''
    desc = get_setting_section('SiteDescription')
    if desc:
        return desc
    else:
        return 'Pylogs is a Django based blog system,project page:http://code.google.com/p/pylogs,demo site:http://oteam.cn Simple is beautiful...'
        
def site_keywords():
    '''
    get the site desctiption for html META element
    '''
    keywords = get_setting_section('SiteKeywords')
    if keywords:
        return keywords
    else:
        return 'Pylogs,blog,python,Django'
    
register.simple_tag(get_version)
register.simple_tag(site_name)
register.simple_tag(site_subtitle)
register.simple_tag(theme)
register.simple_tag(site_description)
register.simple_tag(site_keywords)

def get_setting_section(section):
    if CONFIG_CACHE.has_key(section): 
        return CONFIG_CACHE[section]
    else:        
        setting_object = Setting.objects.filter(setting_name__exact=section)
        if setting_object:
            CONFIG_CACHE[section] = setting_object[0].setting_value
            return CONFIG_CACHE[section]
        else:
            return ''

def update_config_cache(sender,instance,**kwargs):
    """
    update the CONFIG_CACHE value
    """    
    key = instance.setting_name
    if instance.setting_value:	
	CONFIG_CACHE[key] = instance.setting_value
	
post_save.connect(update_config_cache, sender=Setting)