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
    
    class Meta:
        ordering = ['date_added']


class Chat(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)


class SingleChat(Chat):
    status = models.BooleanField(default=False)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    
    @property
    def add_status(self):
        self.status = True
        instance = self
        instance.save()

    def __str__(self):
        return "Author: {}, Friend: {}".format(
            self.contact.profile.user.username, 
            self.contact.friend.user.username)
    

class GroupChat(Chat):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)


class GroupMember(models.Model):
    chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE, related_name="members")
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)


class Message(models.Model):
    '''
    Para saber a quem essa menssagem foi enviado, temos o Chat, que passaremos no caso
    seja a conversa entre dois Profile, a referencia do Chat que é criada quando SingleChat é criado
    e no mesmo tem contact, onde tem a referencia tanto do do friend que é o alvo dá menssagem.

    No caso de um grupo, pegaremos a referencia criada do Chat do GroupChat que cria uma assim que o 
    mesmo é criado, porem pegaremos o chat limpo de referencia de contact, portanto a menssagem sera destinada a
    todos que participam do grupo.
    '''
    
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sent_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)