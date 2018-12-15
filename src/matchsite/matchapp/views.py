from django.shortcuts import render, redirect
from django.db.models import Count
from django.http import HttpResponse, Http404, HttpResponseRedirect
from matchapp.models import Member, Profile, Hobby, Number
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.http import QueryDict
from .forms import *
from django.db import IntegrityError
from django.shortcuts import render_to_response
from datetime import datetime
from django.contrib.auth import get_user_model

from matchapp.templatetags.extras import display_matches

# REST imports
from rest_framework import viewsets
from .serializers import ProfileSerializer, MemberSerializer

User = get_user_model()


class ProfileViewSet(viewsets.ModelViewSet):
    # API endpoint for listing and creating profiles
    queryset = Profile.objects.order_by('user')
    serializer_class = ProfileSerializer


class MemberViewSet(viewsets.ModelViewSet):
    # API endpoint for listing and creating members
    queryset = Member.objects.order_by('username')
    serializer_class = MemberSerializer


appname = 'matchapp'

# should render login page but also include a signup button


def index(request):
	# Render the index page
    form = UserLogInForm()
    """if 'username' in request.session:
        return redirect('displayProfile')"""
    """else:"""
    return render(request, 'matchapp/index.html', {'form': form, 'loggedIn': False})



# user logged in


def loggedin(view):
    def mod_view(request):
        form = UserLogInForm()
        if 'username' in request.session:
            username = request.session['username']
            try: user = Member.objects.get(username=username)
            except Member.DoesNotExist: raise Http404('Member does not exist')
            return view(request, user)
        else:
            return render(request, 'matchapp/index.html', {'form': form, 'loggedIn': False})
    return mod_view

# terms and conditions


def tc(request):
	return render(request, 'matchapp/tc.html')


# once user clicks register button
# should render user registered page if unique user is entered
# need validation for email, user, dob, profile image


def register(request):

	# form = UserRegForm()

     if request.method == "POST":
		# form_class is class of form name NEED TO CHANGE
        form = UserRegForm(request.POST)

        if form.is_valid():

			# user = form.save(commit=False)
			# normalized data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = Member(username=username)
            user.set_password(password)

            try:user.save()
            except: #IntegrityError:
                #raise Http404('Username '+ str(user)+' already taken: Username must be unique')

			#return redirect('index')
                context = {
                    'appname':appname,
                    'form': form,
                    'error':'Username '+ str(user) +' already taken: Usernames must be unique',
                    }
            # login(request,user)
                return render(request, 'matchapp/register.html', context)

            form = UserLogInForm()

            return render(request, 'matchapp/index.html', {'form': form, 'loggedIn': False})


     else:
        form = UserRegForm()
        return render(request, 'matchapp/register.html', {'form': form})

# this occurs when user presses login button from index


def login(request):
    if "username" in request.session:
        return redirect('displayProfile')
    if request.method == "POST":
        form = UserLogInForm(request.POST)
        if 'username' in request.POST and 'password' in request.POST:
            if form.is_valid():

                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")

                user = authenticate(username=username, password=password)

                if user is not None:
                    if user.is_active:
                        request.session['username'] = username
                        request.session['password'] = password
                        form = UserProfile()
                        person = Member.objects.get(id=user.id)
                        hobby = Hobby.objects.all()

                        context = {
                            'appname':appname,
                            'form': form,
                            'user': person,
                            'hobbies': hobby,
                            'loggedIn': True
                        }
						# login(request,user)

                        #where should it go after user logged in?
                        return render(request, 'matchapp/displayProfile.html', context)

                # return HttpResponse("<span> User or password is wrong </span")

                else:
                    #raise Http404('User or password is incorrect')
                    context = {
                        'appname':appname,
                        'form': form,
                        'error':'User or password entered is incorrect'
                    }
                    # login(request,user)
                    return render(request, 'matchapp/index.html', context)

    else:
        #return displayProfile(request,)
        form = UserLogInForm()
        context = {
        'appname':appname,
        'form': form,
        'loggedIn': False
        }
        return render(request, 'matchapp/index.html', context)

# render logout page


@loggedin
def logout(request, user):
	request.session.flush()
	return redirect("/")

# shows another page with users that have similar interests
# order of most common hobbies first


@loggedin
def similarHobbies(request, user):
    # Get all the other users exclude current logged in user
    exclude = Member.objects.exclude(id=user.id)
    # Filter based on the current logged in user on same hobbies
    common = exclude.filter(hobbies__in=user.hobbies.all())
    # Get the number of hobbies of other users
    hobbies = common.annotate(hob_count=Count('hobbies'))
    # Process the matches in decending
    # Note to self do not need the gt thing check first
    match = hobbies.order_by('-hob_count')

    context = {
        'appname': appname,
        'matches': match,
        'numberOfhobbies': hobbies.count(),
        'loggedIn': True
        }

    return render(request, 'matchapp/matches.html', context)


# filter button on similarHobbies page which generates
# By gender or age or both !

@loggedin
def filter(request, user):
    if request.method == 'GET':
        exclude = Member.objects.exclude(username=user)
        common = exclude.filter(hobbies__in=user.hobbies.all())
        gender = request.GET.get('gender',False)
        yearMin = getYearBorn(request.GET.get('age-min', False))
        yearMax = getYearBorn(request.GET.get('age-max',False))

        if gender and yearMin and yearMax:
            sex = common.filter(profile__gender=gender)
            match = sex.filter(profile__dob__year__range=(yearMax,yearMin))

        elif gender:
            match = common.filter(profile__gender= gender)

        elif yearMin and yearMax:
            match= common.filter(profile__dob__year__range=(yearMax,yearMin))
        else:
            raise Http404("Please fill in the boxes")

        return HttpResponse(display_matches(match))

    else:
	    raise Http404("GET request was not used")


def getYearBorn(age):
    if age != '':
        return int((datetime.now().year - int(age)))
    else:
        return age

@loggedin
def displayProfile(request, user):
	# query users login
    if request.method == "GET":
        form = UserProfile()
        formM = MemberProfile()
        person = Member.objects.get(id=user.id)
        hobby = Hobby.objects.all()

        context = {
            'appname':appname,
            'form': form,
            'formM': formM,
            'user': person,
            'hobbies': hobby,
            'loggedIn': True
        }

        return render(request, 'matchapp/displayProfile.html', context)

#remove csrf_exempt
@loggedin
def editProfile(request, user):
    if request.method == 'POST':
        form = UserProfile(request.POST,instance=user)
        formM = MemberProfile(request.POST,instance=user)
        if form.is_valid() and formM.is_valid():

            profile = Profile.objects.get(user=user.id)
            profile.email = form.cleaned_data.get('email')
            profile.dob = form.cleaned_data.get('dob')
            profile.gender = form.cleaned_data.get('gender')

            profile.save()

            member = Member.objects.get(id=user.id)
            allHobbies= formM.cleaned_data.get('hobbies')

            member.hobbies.set(allHobbies)
            member.save()

            context = {
                'appname':appname,
                'form': form,
                'formM': formM,
                'user': member,
                'hobbies': allHobbies,
                'loggedIn': True
            }

            return render(request, 'matchapp/displayProfile.html', context)
        else:
            print (form.errors)
            return HttpResponse("else")

@loggedin
def upload_image(request, user):
    member = Member.objects.get(id=user.id)
    profile = Profile.objects.get(user = member.id)
    if 'img_file' in request.FILES:
        image_file = request.FILES['img_file']
        profile.image = image_file
        profile.save()
        return HttpResponse(profile.image.url)
    else:
        return HttpResponse("Image not in request")

@loggedin
def contacts(request, user):
    # all the users matches that is logged in 
    # Get the requested user   
    exclude = Member.objects.exclude(id=user.id)    
    match = exclude.filter(hobbies__in=user.hobbies.all())
    
    friends = user.friends.all()

    context = {
        'u': user,
        'matches': match,
        'friends': friends,
        'loggedIn': True,
    }

    return render(request, 'matchapp/contact.html', context)
    
def send_request(request, id):
    if 'username' in request.session:
        username = request.session['username']
        from_member = Member.objects.get(username = username)
        to_member = Member.objects.get(id=id)
        NRequest, created = Number.objects.get_or_create(
        from_user=from_member,
        to_user=to_member)
        request.session['created'] = "created"
        return HttpResponseRedirect("/contact")

def cancel_request(request, id):
     if 'username' in request.session:
        username = request.session['username']
        to_member = Member.objects.get(username = username)
        from_member  = Member.objects.get(id=id)

        NRequest = Number.objects.filter(
        from_user=from_member,
        to_user=to_member).first()
        NRequest.delete()
        return HttpResponseRedirect("/contact")

def delete_request(request, id):
     if 'username' in request.session:
        username = request.session['username']
        from_member = Member.objects.get(username = username)
        to_member  = Member.objects.get(id=id)
        NRequest = Number.objects.filter(
        from_user=from_member,
        to_user=to_member).first()
        NRequest.delete()
        return HttpResponseRedirect("/contact")

def accept_request(request, id):
     if 'username' in request.session:
        username = request.session['username']
        to_member = Member.objects.get(username = username)
        from_member  = Member.objects.get(id=id)
        NRequest = Number.objects.filter(
        from_user=from_member,
        to_user=to_member).first()
             
        # Make these users friends of each other
        to_member.friends.add(from_member)
        from_member.friends.add(to_member)

        acceptedUser = Profile.objects.get(user=from_member).number
        currentUser  = Profile.objects.get(user=NRequest.to_user).number
       
        NRequest.delete()
        return HttpResponseRedirect("/contact")






