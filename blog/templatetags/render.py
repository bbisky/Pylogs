#-*- coding:utf-8 -*-
from django import template
from utils import markdown

register = template.Library()



@register.filter
def markup(content,markup_system):
    if markup_system == u"markdown":
        content  = markdown.markdown(content)
    return content
