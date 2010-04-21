#!/usr/bin/env python
#coding=utf-8
from django import forms
textarea_attrs = { 'class': 'textbox textarea' }
class CommentForm(forms.Form):
    comment_author = forms.CharField(max_length=32)
    comment_author_email = forms.EmailField()
    comment_author_url = forms.URLField(required=False)
    comment_content = forms.CharField(widget=forms.Textarea(attrs=textarea_attrs),
                                      max_length=1024)
