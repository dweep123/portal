from django.shortcuts import render
from django.http import HttpResponse,HttpRequest
from django.template import RequestContext
from django.shortcuts import render_to_response
from dashboard.models import Community,SysterUser
from dashboard.forms import CommunityForm
from dashboard.forms import SysterUserForm,UserForm,UserEditForm
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def index(request):
	context=RequestContext(request)
	return render_to_response('dashboard/index.html',{},context)

def profiles(request,user_name_url):
	context=RequestContext(request)
	user_name=user_name_url
	context_dic={'user_name':user_name}
	try:
		user=User.objects.get(username=user_name)
		systeruser=SysterUser.objects.get(user=user)
		context_dic['user']=user
		context_dic['systeruser']=systeruser
	except User.DoesNotExist:
		pass
	return render_to_response('dashboard/profile.html',context_dic,context)

def register(request):
		context=RequestContext(request)
		registered = False
		if request.method=='POST':
			userform=UserForm(data=request.POST)
	    		systeruserform=SysterUserForm(data=request.POST)
		 	if userform.is_valid(): 
				user=userform.save()
				user.set_password(user.password)
				user.save()
				systeruser=SysterUser(user=user)
			        systeruser.save()
			        new_user = authenticate(username=request.POST['username'],
			        password=request.POST['password'])
			 	login(request, new_user)
				registered=True
			else:
			 	print userform.errors
		else:
		  	userform=UserForm()
		  	systeruserform=SysterUserForm()
		return render_to_response('dashboard/register.html',{'userform':userform,'systeruserform':systeruserform,'registered':registered},context)

@login_required
def edit_profile(request):
		context=RequestContext(request)
		if request.method=='POST':
			userform=UserEditForm(data=request.POST,instance=request.user)
	    		systeruserform=SysterUserForm(data=request.POST,instance=SysterUser.objects.get(user=request.user))
		 	if userform.is_valid() and systeruserform.is_valid():
				user=userform.save()
				systeruser=systeruserform.save(commit=False)
				if 'Profilepicture' in request.FILES:
					systeruser.Profilepicture=request.FILES['Profilepicture']
				systeruser.save()
				return HttpResponseRedirect('/dashboard/profile/'+user.username+'/')

			else:
			 	print userform.errors,systeruserform.errors
		else:
		  	userform=UserEditForm(instance=request.user)
		  	systeruserform=SysterUserForm(instance=SysterUser.objects.get(user=request.user))
		return render_to_response('dashboard/edit_profile.html',{'userform':userform,'systeruserform':systeruserform},context)


def user_login(request):
	context=RequestContext(request)
	if request.method=='POST':
		username=request.POST['username']
		password=request.POST['password']
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request,user)
				return HttpResponseRedirect('/dashboard/')
			else:
				return HttpResponse("Your Systers account is disabled.")
		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")
	else:
	        return render_to_response('dashboard/login.html', {}, context)

@login_required
def user_logout(request):
	context=RequestContext(request)
	logout(request)
	return HttpResponseRedirect('/dashboard/')

@login_required
def change_password(request):
	context=RequestContext(request)
	if request.method=='POST':
		user=request.user
		password=request.POST['password']
		repeatpassword=request.POST['repeatpassword']
		if password==repeatpassword:
			user.set_password(password)
			user.save()
			return HttpResponseRedirect('/dashboard/')
		else:
			print "Passwords don't match"
			return HttpResponse("Passwords don't maatch")
	else:
	        return render_to_response('dashboard/passwdchange.html', {}, context)
