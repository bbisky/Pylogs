#!/usr/bin/env python
#coding=utf-8
#html utility methods
import re
r = re.compile(r'\b(([A-Z]+[a-z]+){2,})\b')
def htmlDecode(str):
    """处理页面换行等，替换为html编码。并且将回车符转为<br>"""
    str = re.sub(r'[\n\r]+', '<br>', str)
    #str = re.sub(r'[\s]+','&nbsp;',str)
    return str