from core.models import *

def run():

    profile = Profile.objects.get(pk=1)
    group_chat = group_chat = GroupChat.objects.create(owner=profile, title="Engenharia da safadesa")

    print("\nSucess: {}".format(group_chat))