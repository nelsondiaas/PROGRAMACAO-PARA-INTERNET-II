from core.models import *

def run():

    group_member = GroupMember.objects.all()

    print("\nSuccess: {}".format(group_member[0].__dict__))