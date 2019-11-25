from core.models import *

def run():

    group_member = GroupMember.objects.get(pk=1)
    
    chat = group_member.chat.chat_ptr_id

    profile = group_member.contact.friend

    message = Message.objects.create(chat=chat, sent_by=profile, content="minha primeira msg!", )

    print("\nSuccess: {}".format(message))