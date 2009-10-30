from django import template
from django.template.defaultfilters import striptags
from django.utils.encoding import force_unicode

register = template.Library()
def substring(value,length):
    '''substring'''
    str=striptags(value)
    str = force_unicode(str)
    s = ''   
    index = 0
    len = int(length)
    while len>0:
        char = str[index:index+1]
        index += 1
        if char > u'\x80':
            len -= 2
        else:
            len -= 1
        s += char
    #if len<0:
    #    s = s[:-1]
    if s != str:
        s += '...'
    return s
register.filter(substring)

def priority_name(value):
    '''return priority name'''    
    if value == 2:      
        return 'high'
    elif value == 1:
        return 'medium'
    else:
        return 'low'    
register.filter('priority_name',priority_name)
