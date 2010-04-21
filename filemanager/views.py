#coding=utf-8
import os
import re
from datetime import datetime

from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render_to_response
from django.utils.http import urlquote
from django.utils.translation import ugettext as _
from django.contrib.admin.views.decorators import staff_member_required  
from django.utils.http import urlquote
from django.core.urlresolvers import reverse

from models import Path
import settings
from settings import MEDIA_ROOT,MEDIA_URL,ALLOW_FILE_TYPES

#ALLOW_FILE_TYPES = ('.jpg','.gif','.png')
#try:
#    ALLOW_FILE_TYPES = settings.ALLOW_FILE_TYPES
#except:pass

@staff_member_required
def index(request,p=None):   
    #render path list        
    dirs,files = [],[]
    #set default path root is MEDIA_ROOT/upload
    path = os.path.join(MEDIA_ROOT,'upload')
    dir_url_prefix = reverse('filemanager',args=[''])
    file_url_prefix = os.path.join(MEDIA_URL,'upload') + '/'
    is_showup = False
    
    if p:
        is_showup = True
        path = os.path.join(path,p)
        file_url_prefix += p
        dir_url_prefix += p
    
    #check the path is exists?
    if not os.path.exists(path):
        os.makedirs(path)   
    msg = ''    
    #upload files to this path
    if request.method == 'POST':       
        up_file = request.FILES.get('up_file')        
        new_dirname = request.POST.get('newdir')
        if up_file:            
            filename = up_file.name
            if not check_file_type(filename):
                return HttpResponse('<script>alert("%s");\
                                    window.location.href = window.location.href;\
                                    </script>'%
                                'Upload this file type is not allowed!')   
            filename = get_safe_filename(path,filename)            
            #fd = open('%s/%s' % (path, filename), 'wb')   
            #fd.write(up_file['content'])   
            #fd.close()
            upload_file(up_file,'%s/%s' % (path, filename))
            msg = _('Upload successful,filename is %s') % filename
            return HttpResponse('<script>alert("%s");\
                                window.location.href = window.location.href;\
                                </script>'% msg)   
        if new_dirname:
            #create new dir
            msg = ''
            new_dirname = os.path.join(path,new_dirname)
            try:
                os.mkdir(new_dirname)
                msg = _('Create directory successful!')
            except:
                msg = _('Sorry,create directory failed!')
            return HttpResponse('<script>alert("%s");\
                                window.location.href = window.location.href;\
                                </script>'% msg)   
    list_path(path,dirs,files,file_url_prefix,dir_url_prefix)
    current_loc = p
    for f in files:
        dirs.append(f)
    return render_to_response('filemanager/index.html',
                              {'dirs':dirs,
                                'is_showup':is_showup,
                                'current_location':current_loc,
                                'msg':msg,
                                'allow_types':ALLOW_FILE_TYPES})

def get_safe_filename(path,filename):
    #get the safe filename on the server    
    if os.path.exists(os.path.join(path,filename)):
        r = re.compile(r'(\w+)\((\d+)\)$',re.I)
        filename_info = os.path.splitext(filename)
        m = r.match(filename_info[0])
        if m:
            f1 = m.groups(0)[0]
            f2 = int(m.groups(0)[1])
            filename =  '%s(%s)%s' % (f1,f2+1,filename_info[1])            
        else:
            filename = filename_info[0] + '(1)'+filename_info[1]
        return get_safe_filename(path,filename)
    else:        
        return filename
                
def list_path( path, dirs,files,file_url_prefix,dir_url_prefix):
    for fname in os.listdir(path):
        p = Path()
        p.name = fname
        fname = os.path.join(path,fname)
        #p.physical = os.path.normpath(fname)
        p.lastmodified = datetime.fromtimestamp(os.path.getmtime(fname))
        if os.path.isdir(fname):
            p.url = url_join(dir_url_prefix,p.name)
            p.is_dir = True
            dirs.append(p)            
        elif os.path.isfile(fname):
            p.url = url_join(file_url_prefix,p.name,True)
            p.size = os.path.getsize(fname)
            
            files.append(p)
            
def url_join(url1,url2,isfile = False):
    '''join a url'''
    url = '/'.join([url1,url2])
    if not isfile:
        url = url + '/'
    url = url.replace('//','/')
    return urlquote(url)

def check_file_type(filename):    
    name,ext = os.path.splitext(filename)
    if not ext or ext.lower() not in ALLOW_FILE_TYPES:
        return False
    else:
        return True
    
def upload_file(file,destination):
    path,filename = os.path.split(destination)
    if not os.path.exists(path):
        os.makedirs(path)    
    destination = open(destination, 'wb+')
    for chunk in file.chunks():
        destination.write(chunk)
   