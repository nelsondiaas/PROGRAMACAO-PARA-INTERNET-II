from core.models import *

def run():

    group_chat = GroupChat.objects.get(pk=1)
    contact = Contact.objects.get(pk=1)

    group_member = GroupMember.objects.create(chat=group_chat, contact=contact)

    print("\nSucess: {}".format(group_member))