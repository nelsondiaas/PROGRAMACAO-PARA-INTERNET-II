from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Address(models.Model):
    street = models.CharField(max_length=255)
    suite = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.OneToOneField(Address, models.CASCADE, related_name='address')

class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    userId = models.ForeignKey(Profile, models.CASCADE, related_name='posts')

class Comment(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    body = models.TextField()
    postId = models.ForeignKey(Post, models.CASCADE, related_name='comments')
    
