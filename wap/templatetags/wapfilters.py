#coding=utf-8
import re

from django import template
from django.template.defaultfilters import striptags, linebreaksbr
from django.utils.safestring import mark_safe

register = template.Library()
def safewml(value):
    br = re.compile('<br\s?/>')
    value = br.sub('\r\n',value)
    value = value.replace('&nbsp;',' ')
    value = striptags(value)
    value = linebreaksbr(value)
    value = value.replace('&ldquo;','"')
    value = value.replace('&rdquo;','"')
    return mark_safe(value)
safewml.is_safe = True
safewml = register.filter(safewml)
    
def safewml2(value):
    #safetags = re.compile('(<[^img,br,a,em].*?>)',re.I|re.M)
    safetags = re.compile('(<(?!em>|/em>|img\s|br\s*/>|a\s|/a\s*>).*?>)',re.I|re.M)
    value = safetags.sub('',value)
    a = re.compile('<a [href,title,class,id]')
    value = value.replace('&','&amp;')
    value = a_attribute(value)
    value = img_attribute(value)
    return mark_safe(value)
#safewml.is_safe = True
#safewml = register.filter(safewml)


def a_attribute(html):
    '''clear invalid attr for a tags'''
    a = re.compile('<a.*?>',re.I|re.M)
    r = re.compile('(href|title|class|id)\s?=\s?("|\')[^",\']+("|\')',re.I|re.M)
    a_tags = a.findall(html)
    text = a.sub('$A$',html)
    for i in range(0,len(a_tags)):    
        a_new = "<a "    
        while(r.search(a_tags[i])):        
            a_new += r.search(a_tags[i]).group()
            a_new += " "
            a_tags[i] = r.sub('',a_tags[i],count=1)
        a_new += ">"      
        text = text.replace('$A$',a_new.lower(),1)        
    return text

def img_attribute(html):
    '''clear invalid attr for img tags'''
    a = re.compile('<img.*?/>',re.I|re.M)
    r = re.compile('(align|alt|class|id|height|hspace|localsrc|src|vspace|width|title)\s?=\s?("|\')[^",\']+("|\')',re.I|re.M)
    img_tags = a.findall(html)
    text = a.sub('$A$',html)
    for i in range(0,len(img_tags)):    
        a_new = "<img "    
        while(r.search(img_tags[i])):        
            a_new += r.search(img_tags[i]).group()
            a_new += " "
            img_tags[i] = r.sub('',img_tags[i],count=1)
        a_new += "/>"       
        text = text.replace('$A$',a_new.lower(),1)
    return text
    

