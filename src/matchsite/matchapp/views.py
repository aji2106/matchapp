from django.shortcuts import render, redirect
from django.db.models import Count
from django.http import HttpResponse, Http404, HttpResponseRedirect
from matchapp.models import Member, Profile, Hobby, Number, Like
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

from django.forms.models import model_to_dict


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
    login_form = UserLogInForm()
    registration_form = UserRegForm()
    """if 'username' in request.session:
        return redirect('displayProfile')"""
    """else:"""
    return render(request, 'matchapp/index.html', {'login_form': login_form,'registration_form': registration_form, 'loggedIn': False})



# user logged in


def loggedin(view):
    def mod_view(request):
        login_form = UserLogInForm()
        if 'username' in request.session:
            username = request.session['username']
            try: user = Member.objects.get(username=username)
            except Member.DoesNotExist: raise Http404('Member does not exist')
            return view(request, user)
        else:
            return render(request, 'matchapp/index.html', {'login_form': login_form, 'loggedIn': False})
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
        registration_form = UserRegForm(request.POST)

        if registration_form.is_valid():
			# user = form.save(commit=False)
			# normalized data
            username = registration_form.cleaned_data['username']
            password = registration_form.cleaned_data['password']
            re_password = registration_form.cleaned_data['re_password']
            if password and re_password:
                if password != re_password:

                    errorPassword=("The two password fields do not match.")
                    login_form = UserLogInForm()
                    context = {
                        'appname':appname,
                        'registration_form': registration_form,
                        'login_form': login_form,
                        'errorPassword':errorPassword
                        }
                    return render(request, 'matchapp/index.html', context)

                else:
                    user = Member(username=username)
                    user.set_password(password)


                    try:
                        user.save()

                    except:
                        login_form = UserLogInForm()
                        registration_form = UserRegForm()

                        context = {
                            'appname':appname,
                            'login_form': login_form,
                            'registration_form': registration_form,
                            'errorM':'Username '+ str(user) +' is already taken. Usernames must be unique',
                            }

                        return render(request, 'matchapp/index.html', context)

                    login_form = UserLogInForm()
                    registration_form = UserRegForm()
                    return render(request, 'matchapp/index.html', {'login_form': login_form,'registration_form': registration_form, 'loggedIn': False})



     #else:
        #form = UserRegForm()
        #loginForm = UserLogInForm()

        #return render(request, 'matchapp/index.html', {'form': form,'loginForm': loginForm})

# this occurs when user presses login button from index


def login(request):
    if "username" in request.session:
        return redirect('displayProfile')
    if request.method == "POST":
        form = UserLogInForm(request.POST)
        registration_form = UserRegForm()
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
                        member_form = MemberProfile()
                        profile = Profile.objects.get(user=user.id)
                        form = UserProfile(initial=model_to_dict(profile))

                        person = Member.objects.get(username=user)

                        member_form = MemberProfile(initial=model_to_dict(person))
                        person = Member.objects.get(id=user.id)
                        #hobby = Hobby.objects.all()

                        context = {
                            'appname':appname,
                            'form': form,
                            'member_form': member_form,
                            'registration_form':registration_form,
                            'user': person,
                            #'hobbies': hobby,
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
                        'login_form': form,
                        'registration_form':registration_form,
                        'error':'User or password entered is incorrect'
                    }
                    # login(request,user)
                    return render(request, 'matchapp/index.html', context)

    else:
        #return displayProfile(request,)
        form = UserLogInForm()
        registration_form = UserRegForm()
        context = {
        'appname':appname,
        'login_form': form,
        'registration_form':registration_form,
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

# Might have to get all users that have liked by the current logged in user
# So if they refresh the page the likes would be there

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

    # For the EXTRA FEATURE (get all the user that liked this user)
    # It will be the to_user field
    #print(str(user))

    like = Like.objects.filter(from_user=user)

    #print(str(like))

    context = {
        'appname': appname,
        'u': user,
        'matches': match,
        'numberOfhobbies': hobbies.count(),
        'likes' : like,
        'loggedIn': True
        }

    return render(request, 'matchapp/matches.html', context)


# filter button on similarHobbies page which generates
# By gender or age or both !

@loggedin
def filter(request, user):
    if request.method == 'GET':
        exclude = Member.objects.exclude(username=user)
        common = exclude.filter(hobbies__in=user.hobbies.all()).distinct()
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

        print(yearMax , yearMin)
        print(gender)
        print(str(match))
        return HttpResponse(display_matches(match,user))

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
        profile = Profile.objects.get(user=user.id)
        form = UserProfile(initial=model_to_dict(profile))

        person = Member.objects.get(username=user)

        member_form = MemberProfile(initial=model_to_dict(person))
        context = {
            'appname':appname,
            'form': form,
            'member_form': member_form,
            'user': person,
            'loggedIn': True
        }

        return render(request, 'matchapp/displayProfile.html', context)

@loggedin
def editProfile(request, user):
    if request.method == 'POST':
        form = UserProfile(request.POST,instance=user)
        member_form = MemberProfile(request.POST,instance=user)
        if form.is_valid() and member_form.is_valid():

            profile = Profile.objects.get(user=user.id)
            profile.email = form.cleaned_data.get('email')

            if Profile.objects.filter(email = form.cleaned_data['email']).exists():
                member = Member.objects.get(id=user.id)
                allHobbies= member_form.cleaned_data.get('hobbies')
                email=profile.email
                context = {
                    'appname':appname,
                    'form': form,
                    'member_form': member_form,
                    'user': member,
                    'hobbies': allHobbies,
                    'error' : 'Email '+ email +' is already in use',
                    'loggedIn': True
                }

                return render(request, 'matchapp/displayProfile.html', context)
            else:
                profile.dob = form.cleaned_data.get('dob')
                profile.gender = form.cleaned_data.get('gender')
                profile.number = form.cleaned_data.get('number')

                profile.save()

                member = Member.objects.get(id=user.id)
                allHobbies= member_form.cleaned_data.get('hobbies')

                member.hobbies.set(allHobbies)
                member.save()

                context = {
                    'appname':appname,
                    'form': form,
                    'member_form': member_form,
                    'user': member,
                    'hobbies': allHobbies,
                    'loggedIn': True
                }

                return render(request, 'matchapp/displayProfile.html', context)
        else:

            member = Member.objects.get(id=user.id)
            errors=form.errors
            context = {
                'appname':appname,
                'form': form,
                'member_form': member_form,
                'user': member,
                'error': errors,
                'loggedIn': True
            }

            return render(request, 'matchapp/displayProfile.html', context)

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
    # display only if both users have liked each other
    like = Like.objects.filter(from_user=user)

    friends = user.friends.all()

    context = {
        'u': user,
        'friends': friends,
        'likes': like,
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

        NRequest.delete()
        return HttpResponseRedirect("/contact")

# Ajax to update the likes
def liked(request, match_id):

    if request.method == 'PUT':
        if 'username' in request.session:
            u = request.session['username']
            to_mem = Member.objects.get(id=match_id)
            from_mem = Member.objects.get(username=u)
            like = False

            liked = Like.objects.filter(
                from_user = from_mem,
                to_user = to_mem
            )

            # They have never liked this user before so like them
            if not liked.exists():
                liked = Like(to_user = to_mem, from_user=from_mem, liked=True)
                like = True
                liked.save()

            # They have liked the user before but now unliked them so remove the like
            # Remove the like
            else:
                # Check if the numbers request has been sent if so delete it
                numberR = Number.objects.filter(to_user=to_mem).filter(from_user=from_mem)
                if numberR.exists():
                    numberR.delete()
                liked.delete()

        response = {
            "from_user" : from_mem.username,
            "to_user": to_mem.username,
            "liked": like
        }
        return JsonResponse(response)
    else:
        raise Http404("PUT request was not used")
