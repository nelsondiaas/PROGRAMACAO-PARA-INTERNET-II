from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile")
    status = models.CharField(max_length=120, default="Bem vindo ao meu perfil")
    
    class Meta:
        ordering = ['user']


class Contact(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="contacts")
    friend = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_contacts(self):
        return "http://localhost:8000/api/v1/profiles/{}/".format(self.friend.user.pk)
    
    class Meta:
        ordering = ['date_added']


class Chat(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)


class SingleChat(Chat):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)


class GroupChat(Chat):
    title = models.CharField(max_length=64)


class GroupMember(models.Model):
    chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE, related_name="members")
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sent_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)