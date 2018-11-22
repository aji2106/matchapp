from django.shortcuts import render
from django.http import HttpResponse, Http404
from matchapp.models import Member, Profile, Hobby
from django.contrib.auth.hashers import make_password

# REST imports
from rest_framework import viewsets
from .serializers import ProfileSerializer, MemberSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    # API endpoint for listing and creating profiles
    queryset = Profile.objects.order_by('user')
    serializer_class = ProfileSerializer

class MemberViewSet(viewsets.ModelViewSet):
    # API endpoint for listing and creating members
    queryset = Member.objects.order_by('username')
    serializer_class = MemberSerializer


appname = 'matchapp'

#should render login page but also include a signup button
def index(request):
	context = {
		'appname' : appname
	}
	# Render the index page
	return render(request,'matchapp/login.html', context)

#user logged in
def loggedin(request):
	return HttpResponse("user logged in")

#terms and conditions
def tc(request):
	return render(request,'matchapp/tc.html')

#should render the signup page
def signup(request):
	return render(request,'matchapp/register.html')


#should render user registered page if unique user is entered
#need validation for email, user, dob, profile image
def register(request):

    if 'username' in request.POST and 'password' in request.POST:
        u = request.POST['user']
        p = request.POST['psw']

        user = Member(username=u)
        user.set_password(p)

        try:
            user.save()
        except:
            Http404("Username " + u + "is already taken")

        context = {
			'username': u
		}

        return render(request,'matchapp/login.html',context)

    else:
       return Http404("Data was not inserted")


#this occurs when user presses login button from index
def login(request):
	#return HttpResponse("login")
    return render(request,'matchapp/login.html')
#render logout page
def logout(request):
	return HttpResponse("logout")

#shows another page with users that have similar interests
#order of most common hobbies first
#@loggedin
def similarHobbies(request):
	return HttpResponse("return list of people with similar hobbies")

#filter button on similarHobbies page which generates
#@loggedin
def filter(request):
	return HttpResponse("filter by gender and age using Ajax")

#user profile edit page
#@loggedin
def profile(request):
	return HttpResponse("user should be able to edit page")

#@loggedin
def upload_Image(request):
	return HttpResponse("user should be able to upload an image")
