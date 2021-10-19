from functools import wraps
from django.http import HttpResponseRedirect

def teacher_required(function):
	@wraps(function)
	def wrap(request , *args,**kwargs):
		profile = request.user.userprofile
		if profile.role == 'teacher':
			return function(request,*args,**kwargs)
		else:
			return HttpResponseRedirect('/management/')
	return wrap

def student_required(function):
	@wraps(function)
	def wrap(request , *args,**kwargs):
		profile = request.user.userprofile
		if profile.role == 'student':
			return function(request,*args,**kwargs)
		else:
			return HttpResponseRedirect('/management/')
	return wrap

def role_required(function):
	@wraps(function)
	def wrap(request,*args,**kwargs):
		profile = request.user.userprofile
		role = ['teacher','student']
		if profile.role in role:
			return function(request,*args,**kwargs)
		else:
			return HttpResponseRedirect('/management/')
	return wrap
