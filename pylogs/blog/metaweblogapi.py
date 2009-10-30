import os
import xmlrpclib
import datetime
import time

from settings import MEDIA_ROOT,MEDIA_URL
from django.contrib.auth.models import User
from django.db.models import ObjectDoesNotExist
from django.contrib.sites.models import Site

from models import Category, Post, POST_STATUS

def convert_time(t):
	return datetime.datetime.fromtimestamp(time.mktime(time.strptime(str(t)[:17], '%Y%m%dT%H:%M:%S')))

def authenticated(func):
	"""
	A decorator for functions that will authenticated against
	the users model and check with the picturefolders owner.
	Relies on the position of those parameters.
	"""

	def _wrapper(blogid, username, password, *args, **kw):
		try:
			user = User.objects.get(username=username, is_staff=True)
			if user.check_password(password):
				return func(user, blogid, *args, **kw)
			else: raise ValueError("Authentication Failure")
		except User.DoesNotExist: raise ValueError("Authentication Failure")
	
	return _wrapper

def newPost(user, blogid, struct, publish):
	"""
	Add a new posting. Actually this is a faked posting, as the posting
	is just used to decide what folder to move the referenced image to.
	"""
	folder = struct.get('categories',[''])
	categories = Category.objects.filter(name__in=struct.get('categories',['']))
#	if struct.has_key('dateCreated'):
#		mtime = time.mktime(time.strptime(struct['dateCreated'], '%Y%m%dT%H:%M:%S'))
	status = POST_STATUS[1][0]
	if publish:
		status = POST_STATUS[0][0]
	post = Post(title=struct['title'], content=struct['description'], 
		pubdate=convert_time(struct['dateCreated']), post_status=status
		)
	post.save()
	for c in categories:
		post.category.add(c)
	return post.id

newPost = authenticated(newPost)

def editPost(user, blogid, struct, publish):
	"""
	Add a new posting. Actually this is a faked posting, as the posting
	is just used to decide what folder to move the referenced image to.
	"""
	folder = struct.get('categories',[''])
	categories = Category.objects.filter(name__in=struct.get('categories',['']))
	post = Post.objects.get(pk=int(blogid))
	
	status = POST_STATUS[1][0]
	if publish:
		status = POST_STATUS[0][0]
#	if struct.has_key('dateCreated'):
#		mtime = time.mktime(time.strptime(struct['dateCreated'], '%Y%m%dT%H:%M:%S'))
	post.title = struct['title']
	post.content = struct['description']
	post.pubdate = convert_time(struct['dateCreated'])
	post.post_status = status
	
	post.save()
	post.category.clear()
	for c in categories:
		post.category.add(c)
	return post.id

editPost = authenticated(editPost)


def getCategories(user, blogid):
	"""
	Return the tree of directories for a given picturefolder as
	a list of categories.
	"""
	objs = Category.objects.all()
	categories = []
	
	for o in objs:
		categories.append({'title':o.name, 'description':o.desc})
	return categories

getCategories = authenticated(getCategories)
	

def getPost(user, postid):
	if isinstance(postid, str):
		postid = int(postid)
	try:
		post = Post.objects.get(pk=postid)
	except ObjectDoesNotExist:
		raise ValueError("Post is not existed")
	
	return make_post(post)
		
getPost = authenticated(getPost)

def getUsersBlogs(user,appkey):
	site = Site.objects.get_current()
	if not site.domain.startswith('http://'):
		site.domain = 'http://%s' % site.domain
	return [{'blogid': 1,
		'url': site.domain,
		'blogName': site.name}]

getUsersBlogs = authenticated(getUsersBlogs)
def make_post(post):
	d = { 'permaLink': post.id,
			 'title':post.title,
			 'description':post.content, 
			 'postid':str(post.id),
			 'categories':[c.name for c in post.category.all()],
			 'dateCreated':xmlrpclib.DateTime(post.pubdate.isoformat()) }
	return d
	
def getRecentPosts(user, blogid, number):	
	if isinstance(number, str):
		number = int(number)
	objs = Post.objects.all()[:number]
	s = []
	for obj in objs:
		s.append(make_post(obj))		
	return s
getRecentPosts = authenticated(getRecentPosts)

def newMediaObject(user, blogid, struct):
	"""
	Store a new fileupload in a hidden upload folder so that
	later posts can reference the file and move it to the
	destination directory.
	"""	
	datestr = datetime.datetime.today().strftime('%Y%m')
	upath = os.path.join(MEDIA_ROOT, 'upload',datestr)	
	url = os.path.join(MEDIA_URL,'upload',datestr)		
	(base, ext) = struct['type'].split('/')
	if base != 'image': raise ValueError('%s not supported' % struct['type'])
	(base, ext) = os.path.splitext(struct['name'])
	imagefile = os.path.realpath(os.path.join(upath, base+ext))
	if not imagefile.startswith(upath): raise ValueError('to %s disallowed' % upath)
	p = os.path.dirname(imagefile)
	if not os.path.exists(p): os.mkdir(p)
	f = open(imagefile, 'wb+')
	f.write(struct['bits'].data)	
	f.close()	
	return {
		'url': os.path.join(url,struct['name']).replace('\\','/')
	}

newMediaObject = authenticated(newMediaObject)

