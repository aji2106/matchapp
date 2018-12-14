from django.urls import path, include
from matchapp import views
from django.conf.urls import url

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'profiles', views.ProfileViewSet)
router.register(r'members', views.MemberViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    # register
    path('tc/', views.tc, name='tc'),
    # register
    path('register/', views.register, name='register'),
    # user profile edit page
    path('editProfile/', views.editProfile, name='editProfile'),
    # displays profile
    path('displayProfile/', views.displayProfile, name='displayProfile'),
    # login page
    path('home/', views.login, name='login'),
    # logout page
    path('logout/', views.logout, name='logout'),
    # similar hobbies
    #url(r'^(?P<slug>[\w-]+)/$', views.similarHobbies, name='similarHobbies'),
    path('similarHobbies/', views.similarHobbies, name='similarHobbies'),
    #Ajax: filter
    path('filter/', views.filter, name='filter'),
    # upload image
    path('uploadimage/', views.upload_image, name='uploadimage'),
    # send request
    url(r'^send_request/(?P<id>\d+)/$', views.send_request, name='send_request'),
    # accept request
    url(r'^accept_request/(?P<id>\d+)/$', views.accept_request, name='accept_request'),
    # cancel request
    url(r'^cancel_request/(?P<id>\d+)/$', views.cancel_request, name='cancel_request'),
    # API
    path('api/', include(router.urls))
]
