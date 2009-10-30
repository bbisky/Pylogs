import sys
import time
import xmlrpclib

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.conf import settings

import metaweblogapi

DEBUG = 0
if hasattr(settings, 'DEBUG_RPC'):
	DEBUG = settings.DEBUG_RPC
	
def call(request):
	"""
	This is the view you need to map into your URL space to process RPC
	calls.
	"""
	if request.POST:		
		p, u = xmlrpclib.getparser()
		p.feed(request.raw_post_data)
		p.close()

		args = u.close()
		method = u.getmethodname()		
		func = getattr(__import__('blog'), 'metaweblogapi')
		func = getattr(func,str(method.split('.')[1]))		
		if DEBUG: print method, func, args
		if func is not None:
			try:
				result = func(*args)
				xml = xmlrpclib.dumps((result,), methodresponse=1)
				if DEBUG: print result
			except Exception, e:
				if DEBUG: print e
				xml = xmlrpclib.dumps(xmlrpclib.Fault(-32400, 'system error: %s' % e), methodresponse=1)				
		else:
			xml = xmlrpclib.dumps(xmlrpclib.Fault(-32601, 'method unknown: %s' % method), methodresponse=1)
			
		return HttpResponse(xml, mimetype='text/xml; charset=utf-8')
	else:
		raise Http404

