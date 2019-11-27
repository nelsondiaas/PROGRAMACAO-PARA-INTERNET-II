from core.models import *

def run():

    group_chat = GroupChat.objects.all()

    print("\nSuccess: {}".format(group_chat[0].__dict__))