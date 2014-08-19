from django.shortcuts import render, render_to_response
from login.forms import UserForm
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

def register(request):
	context = RequestContext(request)
	registered = False

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		
		if user_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			registered = True
		else:
			print user_form.errors
	else:
		user_form=UserForm() 
	return render_to_response(
            'login/register.html',
            {'user_form': user_form, 'registered': registered},
            context)

def user_login(request):
	context = RequestContext(request)
	
	if request.method =='POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('mesh_index'))
			else:
				return HttpResponse('we are sorry, but it seems like your account is inactive')
		else:
			return render_to_response(
            			'login/user_login.html'
			)

   
	else:
               return render_to_response(
            			'login/user_login.html'
			)
