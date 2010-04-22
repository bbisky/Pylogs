from django.db import models

class Path:
    '''file object'''
    name = ''
    is_dir = False
    size = 0
    physical = ''
    url = ''
    lastmodified = ''
