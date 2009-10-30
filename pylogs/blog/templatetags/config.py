#!/usr/bin/env python
#coding=utf-8
from django.template import Library
from django.conf import settings

from utils.version import get_svn_revision

register = Library()
VERSION = getattr(settings,'VERSION','unknown')
def get_version():
    """
    Returns the version as a human-format string.
    """
    v = '.'.join([str(i) for i in VERSION[:-1]])
    if VERSION[-1]: 	   
        v = '%s%s %s' % (v, VERSION[-1],get_svn_revision())
    return v

register.simple_tag(get_version)