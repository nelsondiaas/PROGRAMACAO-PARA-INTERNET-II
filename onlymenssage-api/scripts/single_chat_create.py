from core.models import *

def run():

    #contact = Contact.objects.get(pk=1)
    #single_chat = SingleChat.objects.create(contact=contact)
    chats = Chat.objects.all()

    print("\nTESTS: ", chats[0].pk)
    #print("\nTESTS: ", single_chat.__dict__)
