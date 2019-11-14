from core.serializers import *
import json

data = open('db.json', 'r')
json = json.load(data)

profiles = json['users']
posts = json['posts']
comments = json['comments']

def run():

    for profile in profiles :
        profile_serializer = ProfileSerializer(data=profile)
        if profile_serializer.is_valid():
            profile_serializer.save()

    for post in posts:
        post_serializer = PostSerializer(data=post)
        if post_serializer.is_valid():
            post_serializer.save()

    for comment in comments:
        comment_serializer = CommentSerializer(data=comment)
        if comment_serializer.is_valid():
            comment_serializer.save()

    print("\nPopulated database!")





