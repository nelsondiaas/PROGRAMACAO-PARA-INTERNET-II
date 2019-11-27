from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.reverse import reverse
from core.models import *

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    password = serializers.CharField(source='user.password')
    email = serializers.CharField(source='user.email')
    
    class Meta:
        model = Profile
        fields = ['pk', 'username', 'password', 'email', 'status']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data['user'])
        user.save()
        return Profile.objects.create(user=user)


class ProfileListViewSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(many=False, read_only=True, view_name="profile-detail-view")

    class Meta:
        model = Profile
        fields = ['url']


class ProfileDetailViewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    contacts = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name="contact-detail-view")
    singlechats = serializers.HyperlinkedIdentityField(many=False, read_only=True, view_name="profile-siglechat-list")
    create_groupchat = serializers.HyperlinkedIdentityField(many=False, read_only=True, view_name="groupchat-view")
    groupchats = serializers.HyperlinkedIdentityField(many=False, read_only=True, view_name="groupchat-list-view")
    
    class Meta:
        model = Profile
        fields = ['pk', 'username', 'email', 'status', 'singlechats', 'create_groupchat', 'groupchats', 'contacts']

    def patch(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        return instance.save()


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ['pk', 'profile', 'friend', 'date_added']


class ContactDetailSerializer(serializers.ModelSerializer):
    profile = serializers.HyperlinkedRelatedField(many=False, read_only=True, view_name="profile-detail-view")
    friend = serializers.HyperlinkedRelatedField(many=False, read_only=True, view_name="profile-detail-view")
    add_singlechat = serializers.HyperlinkedIdentityField(read_only=True, view_name="singlechat-view")
    
    class Meta:
        model = Contact
        fields = ['pk', 'profile', 'friend', 'add_singlechat', 'date_added']


class SingleChatViewSerializer(serializers.ModelSerializer):
    send_message = serializers.HyperlinkedIdentityField(many=False, read_only=True, view_name="message-view")
    messages = serializers.HyperlinkedIdentityField(many=False, read_only=True, view_name="message-list-view")

    class Meta:
        model = SingleChat
        fields = ['pk', 'chat_ptr_id', 'status', 'contact', 'send_message', 'messages', 'date_created']


class MessageViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['pk', 'chat', 'sent_by', 'content', 'timestamp']


class GroupChatHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    
    def get_url(self, obj, view_name, request, format):
        
        if obj.pk is None:
            return None
      
        url_kwargs = {
            'pk_profile': obj.owner_id,
            'pk_groupchat': obj.id
        }
        return self.reverse(view_name, kwargs=url_kwargs, request=request, format=format)


class GroupChatListViewSerializer(serializers.ModelSerializer):
    url = GroupChatHyperlinkedIdentityField(view_name="groupchat-detail-view")

    class Meta:
        model = GroupChat
        fields = ['url']


class GroupChatViewSerializer(serializers.ModelSerializer):
    add_member = serializers.HyperlinkedIdentityField(many=False, read_only=True, view_name="groupmember-view")
    members = serializers.HyperlinkedIdentityField(many=False, read_only=True, view_name="groupmember-list-view")

    class Meta:
        model = GroupChat
        fields = ['pk', 'chat_ptr_id', 'owner', 'title', 'add_member', 'members', 'date_created']


class GroupMemberViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupMember
        fields = ['pk',  'chat', 'contact']