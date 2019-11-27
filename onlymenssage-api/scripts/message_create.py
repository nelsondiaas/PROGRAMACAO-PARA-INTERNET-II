from core.models import *

def run():

    chat = Chat.objects.get(pk=1)
    profile = SingleChat.objects.get()