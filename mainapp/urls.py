from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.login_user, name = "login"),
    path('signup/', views.signup_user, name = "signup"),
    path('', views.home, name = "home"),
    path('profile/<str:username>', views.profile, name = "profile"),
    path('profile/<str:username>/edit/',views.editProfile, name="editprofile"),
    path('profile/<str:username>/remove/', views.removeProfile, name="removeprofile"),
    path('group/new', views.newgroup, name="newgroup"),
    path('group/all/', views.allgroup, name='allgroup'),
    path('group/<str:id>/edit/', views.editgroup, name="editgroup"),
    path('group/<str:id>/remove/', views.removegroup, name="removegroup"),
    path('group/<str:id>/', views.group, name = "group"),
    path('post/add', views.newpost, name="newpost"),
    path('post/<str:id>/', views.user_post, name="post"),
    path('post/<str:id>/edit/', views.editpost, name="editpost"),
    path('post/<str:id>/remove/', views.removepost, name="removepost"),
    path('logout/', views.logoutUser, name = "logout"),
    path('post/<str:id>/comment', views.addcomment, name="addcomment"),
    path('comment/<str:id>/remove', views.removecomment, name="removecomment"),
    path('addfriend/<str:username>', views.addfriend, name="addfriend"),
    path('group/<str:id>/join/', views.joingroup,name='joingroup'),
    path('group/<str:id>/post/', views.postToGroup, name="grouppost"),
    path('search/', views.search, name="search")


    
]