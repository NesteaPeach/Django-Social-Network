from django.shortcuts import render, redirect
from .models import Profile, Group, Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from itertools import chain

# Create your views here.
@login_required(login_url='login')
def home(request):
    postlist = []
    user = request.user
    posts = Post.objects.all()
    friends = Profile.objects.filter(friends=user)
    for friend in friends:
        postss = Post.objects.filter(user=friend.user)
        for post in postss:
            postlist.append(post)
    groups = Group.objects.filter(
        Q(users = user.profile)|
        Q(owner = user)
    ).distinct()
    for group in groups:
        posta = Post.objects.filter(group = group)
        for po in posta:
            postlist.append(po)
    new1 = set(postlist)    
     #like       
    if request.method == 'POST':
        postid = request.POST['postid']
        mypost = Post.objects.get(id = postid)
        if request.user.profile in mypost.likes.all():
            mypost.likes.remove(request.user.profile)
        else:
            mypost.likes.add(request.user.profile)
    
    return render(request,'mainapp/home.html',{"posts": new1})

@login_required(login_url='login')
def allgroup(request):
    groups = Group.objects.all()
    return render(request, 'mainapp/allgroup.html',{"groups":groups})

def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            try:
                user = User.objects.get(username=username)
            except:
                return render(request,'mainapp/login.html',{"error":"Username Not Found"})

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                return render(request,'mainapp/login.html',{"error":"Username or Password incorrect"}) 

    return render(request,'mainapp/login.html',{})

def logoutUser(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('home')
    else:
        return redirect('login')


def signup_user(request):
    form = UserCreationForm()
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if request.POST['imageUrl'] != '' and request.POST['firstname'] != '' and request.POST['lastname'] != '' and request.POST['city'] != '' and request.POST['dob'] != '':
                if form.is_valid():
                    form.save()
                    username = request.POST['username']
                    password = request.POST['password1']
                    user = authenticate(username=username,password=password)
                    Profile.objects.create(
                        user=user,
                        firstname = request.POST['firstname'],
                        lastname = request.POST['lastname'],
                        city = request.POST['city'],
                        dob = request.POST['dob'],
                        imageUrl=request.POST['imageUrl'],
                        relationship = request.POST['relationship']
                    )
                    return redirect('home')
                else:
                    error = form.errors
                    return render(request,'mainapp/signup.html',{"form":form,"error":error})
            else:
                return render(request,'mainapp/signup.html',{"form":form,"error":"All fields are required"})

    return render(request,'mainapp/signup.html',{"form":form})

@login_required(login_url='login')
def profile(request, username):
     # for profile data
    user1 = User.objects.get(username=username)
    #posts data
    post_count = 0
    like_count = 0
    friend_count = 0
    posts = Post.objects.filter(Q(user = user1)).order_by('-created')
    for post in posts:
        post_count +=1
        likes = post.likes.all()
        for like in likes:
            like_count +=1
    
    if request.method == 'POST':
        postid = request.POST['postid']
        mypost = Post.objects.get(id = postid)
        if request.user.profile in mypost.likes.all():
            mypost.likes.remove(request.user.profile)
        else:
            mypost.likes.add(request.user.profile)

    #friends data
    friends = Profile.objects.filter(friends=user1)
    for friend in friends:
        friend_count +=1
    
    #group data
    groups = Group.objects.filter(
        Q(owner=user1)|
        Q(users = user1.profile)
    ).distinct()

    #likes

    return render(request,'mainapp/profile.html',{'user1':user1, 'posts':posts,'friends':friends,'groups':groups,'post_count':post_count,'like_count':like_count, 'friend_count':friend_count})


@login_required(login_url='login')
def editProfile(request,username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    if user != request.user:
        return redirect('profile', user.username)
    else:
        if request.method == 'POST':
            if request.POST['imageUrl'] != '' and request.POST['firstname'] != '' and request.POST['lastname'] != '' and request.POST['city'] != '':
                profile.user=user
                profile.firstname = request.POST['firstname']
                profile.lastname = request.POST['lastname']
                profile.city = request.POST['city']
                profile.imageUrl=request.POST['imageUrl']
                profile.relationship = request.POST['relationship']
                profile.save()
                return redirect('profile', user.username)
            else:
                return render(request,'mainapp/editprofile.html',{"profile":profile,"error":"All fields must be field"})
    return render(request,'mainapp/editprofile.html',{"profile":profile})

@login_required(login_url='login')
def user_post(request,id):
    post = Post.objects.get(id=id)
    p= request.GET.get('p') if request.GET.get('p') != None else None
    if request.method == 'POST':
        postid = request.POST['postid']
        mypost = Post.objects.get(id = postid)
        if request.user.profile in mypost.likes.all():
            mypost.likes.remove(request.user.profile)
        else:
            mypost.likes.add(request.user.profile)
    comments = Comment.objects.filter(post=post).order_by('-created')
    page_object = Paginator(comments,3)
    context = page_object.page(int(p)) if p != None else page_object.page(1)
    return render(request,'mainapp/post.html',{"post":post, "comments":context, "page_object":page_object})

@login_required(login_url='login')
def newpost(request):
    user = request.user
    if request.method == 'POST':
        Post.objects.create(
            user = user,
            body = request.POST['body'],
            imageUrl = request.POST['imageUrl']
        )
        return redirect('profile', user.username)
    return render(request,'mainapp/newpost.html',{})

@login_required(login_url='login')
def editpost(request,id):
    post = Post.objects.get(id=id)
    if post.user != request.user:
        return redirect('home')
    else:
        if request.method == 'POST':
            post.imageUrl = request.POST['imageUrl']
            post.body = request.POST['body']
            post.save()
            return redirect('profile', request.user.username)
        return render(request,'mainapp/editpost.html',{"post":post})

@login_required(login_url='login')
def removepost(request,id):
    post = Post.objects.get(id=id)
    if post.user != request.user and post.group.owner != request.user:
        return redirect('home')
    else:
        if request.method == 'POST':
            post.delete()
            return redirect('home')
        return render(request,'mainapp/removepost.html',{"post":post})

@login_required(login_url='login')
def group(request,id):
    group = Group.objects.get(id=id)
    posts = Post.objects.filter(group=group).order_by('-created')
    like_count = 0
    for post in posts:
        likes = post.likes.all()
        for like in likes:
            like_count+=1
    #likes
    if request.method == 'POST':
        postid = request.POST['postid']
        mypost = Post.objects.get(id=postid)
        if request.user.profile in mypost.likes.all():
            mypost.likes.remove(request.user.profile)
        else:
            mypost.likes.add(request.user.profile)
    
    return render(request,'mainapp/group.html',{"group":group, "posts":posts, "like_count":like_count})

def joingroup(request,id):
    group = Group.objects.get(id=id)
    user = request.user
    if user == group.owner:
        return redirect('group', group.id)
    else:
        if request.method == 'POST':
            if request.user.profile in group.users.all():
                group.users.remove(request.user.profile)
            else:
                group.users.add(request.user.profile)
            return redirect('group', group.id) 

    return redirect('group', group.id) 

@login_required(login_url='login')
def newgroup(request):
    if request.method == 'POST':
        Group.objects.create(
            owner = request.user,
            name = request.POST['name'],
            description = request.POST['body'],
            imageUrl = request.POST['imageUrl']
        )
        return redirect('allgroup')
    return render(request,'mainapp/newgroup.html',{})

@login_required(login_url='login')
def editgroup(request,id):
    group = Group.objects.get(id=id)
    if group.owner != request.user:
        return redirect('allgroup')
    else:
        if request.method == 'POST':
            group.imageUrl = request.POST['imageUrl']
            group.description = request.POST['body']
            group.name = request.POST['name']
            group.save()
            return redirect('group', group.id )
    return render(request,'mainapp/editgroup.html',{"group":group})

@login_required(login_url='login')
def removegroup(request,id):
    group = Group.objects.get(id=id)
    if group.owner != request.user:
        return redirect('allgroup')
    else:
        if request.method == 'POST':
            group.delete()
            return redirect('allgroup')
    return render(request,'mainapp/removegroup.html',{"group":group})

@login_required(login_url='login')
def removeProfile(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    friends = Profile.objects.filter(friends=user)
    groups = Group.objects.filter(owner = user)
    if user != request.user:
        return redirect('profile', user.username)
    else:
        if request.method == 'POST':
            # group check
            if friends.count() > 0 and groups.count() > 0:
                owner = User.objects.get(id = request.POST['owner'])
                for group in groups:
                    group.owner = owner
                    group.save()
            # end group check
            user.delete()
            return redirect('login')
        return render(request,'mainapp/removeprofile.html',{'profile':profile, "friends":friends})

def addcomment(request,id):
    if request.method == 'POST':
        user = request.user
        post = Post.objects.get(id=id)
        Comment.objects.create(
            user = user,
            post = post,
            body = request.POST['body']
        )
        return redirect('post',post.id)

    return render(request,'mainapp/post.html',{})

def removecomment(request,id):
    comment = Comment.objects.get(id=id)
    if comment.user != request.user:
        return redirect('post',comment.post.id)
    else:
        if request.method == 'POST':
            comment.delete()
            return redirect('post',comment.post.id)
        return render(request,'mainapp/removecomment.html',{"comment":comment})

def addfriend(request,username):
    friend = User.objects.get(username=username)  
    if request.user == friend:
        return redirect('profile',friend.username)
    else:
        if request.method == 'POST':
            user = request.user
            if request.user.profile in friend.friends.all():
                friend.friends.remove(request.user.profile)
                user.friends.remove(friend.profile)
            else:
                friend.friends.add(request.user.profile)
                user.friends.add(friend.profile)
            return redirect('profile',friend.username)
    return render(request,'home',{})

def postToGroup(request,id):
    group = Group.objects.get(id=id)
    user = request.user
    if not request.user.profile in group.users.all() and request.user != group.owner :
        return redirect('group', group.id)
    else:
        if request.method == 'POST':
            Post.objects.create(
                user = user,
                body = request.POST['body'],
                imageUrl = request.POST['imageUrl'],
                group = group
            )
            return redirect('group', group.id)
    return render(request, 'mainapp/grouppost.html',{})

def search(request):
    q = request.GET['q'] if request.GET.get('q') != None else ''
    users = Profile.objects.filter(
        Q(firstname__icontains = q) |
        Q(lastname__icontains = q)
    )
    posts = Post.objects.filter(body__icontains = q)
    groups = Group.objects.filter(
        Q(name__icontains = q) |
        Q(description__icontains = q)
    )
    
    return render(request,'mainapp/search.html', {"users":users, "posts":posts, "groups":groups})