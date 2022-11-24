from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, related_name="friends")
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    dob = models.DateField()
    imageUrl = models.TextField()
    relationship = models.BooleanField(default=False)

    def __str__(self):
        return self.firstname

class Group(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    users = models.ManyToManyField(Profile)
    imageUrl = models.TextField(blank=True)
    def __str__(self):
        return self.name

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, blank=True,null=True, on_delete=models.CASCADE)
    body = models.TextField()
    imageUrl = models.TextField(blank=True)
    likes = models.ManyToManyField(Profile, blank=True)
    created = models.DateTimeField(auto_now_add=True)        
    def __str__(self):
        return self.body

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.body





