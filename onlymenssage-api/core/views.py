from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .paginator import Paginator
from django.http import Http404
from .permissions import *
from .serializers import *
from .models import *

User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ProfileListView(Paginator, APIView):

    pagination_class = PageNumberPagination
    
    def get(self, request, format=None):
        profiles = Profile.objects.get_queryset().order_by('id')
        page = self.paginate_queryset(profiles)
        context = {'request': request}
        profile_serializer = ProfileListViewSerializer(profiles, context=context, many=True)
        return self.get_paginated_response(profile_serializer.data)

    def post(self, request, format=None):
        profile_serializer = ProfileSerializer(data=request.data)
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(profile_serializer.data, status=status.HTTP_201_CREATED)
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileDetailView(APIView):
    
    permission_classes = [IsAuthenticated, ProfileOwnerReadOnly]

    def get_object(self, obj, pk):
        try:
            return obj.objects.get(pk=pk)
        except obj.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        profile = self.get_object(Profile, pk)
        context = {'request': request}
        profile_serializer = ProfileDetailViewSerializer(profile, context=context, many=False)
        return Response(profile_serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk, format=None):
        profile = self.get_object(Profile, pk)
        self.check_object_permissions(request, profile)
        profile_serializer = ProfileDetailViewSerializer(profile, data=request.data, partial=True)
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(profile_serializer.data, status=status.HTTP_200_OK)
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        profile = self.get_object(Profile, pk)
        self.check_object_permissions(request, profile)
        profile.delete()
        return Response(status=status.HTTP_200_OK)


class ContactCreateView(APIView):

    def get_object(self, obj, pk):
        try:
            return obj.objects.get(pk=pk)
        except obj.DoesNotExist:
            raise Http404
    
    def post(self, request, pk_sender, pk_target, format=None):
        sender = self.get_object(Profile, pk_sender)
        target = self.get_object(Profile, pk_target)
        request.data['profile'] = sender.pk
        request.data['friend'] = target.pk
        contact_serializer = ContactSerializer(data=request.data)
        if contact_serializer.is_valid():
            contact_serializer.save()
            return Response(contact_serializer.data, status=status.HTTP_201_CREATED)
        return Response(contact_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContactView(Paginator, APIView):

    pagination_class = PageNumberPagination

    def get(self, request, format=None):
        contacts = Contact.objects.get_queryset().order_by('id')
        page = self.paginate_queryset(contacts)
        context = {'request': request}
        contact_serializer = ContactSerializer(contacts, context=context, many=True)
        return self.get_paginated_response(contact_serializer.data)


class ContactDetailView(APIView):
    
    def get_object(self, obj, pk):
        try:
            return obj.objects.get(pk=pk)
        except obj.DoesNotExist:
            raise Http404
            
    def get(self, request, pk, format=None):
        contact = self.get_object(Contact, pk)
        context = {'request': request}
        contact_serializer = ContactDetailSerializer(contact, context=context, many=False)
        return Response(contact_serializer.data, status=status.HTTP_200_OK)


class SingleChatView(APIView):

    def get_object(self, obj, pk):
        try:
            return obj.objects.get(pk=pk)
        except obj.DoesNotExist:
            raise Http404
    
    def post(self, request, pk, format=None):
        contact = self.get_object(Contact, pk)
        singlechat = SingleChat.objects.filter(contact=contact).exists()
        request.data['contact'] = contact.pk
        context = {'request': request}
        single_chat_serializer = SingleChatViewSerializer(data=request.data, context=context)

        owner = self.get_object(Profile, contact.profile.pk)
        friend = self.get_object(Profile, contact.friend.pk)

        contact_verify = Contact.objects.filter(profile=friend, friend=owner)

        single_verify = False

        if len(contact_verify):
            single_verify = SingleChat.objects.filter(contact=contact_verify[0]).exists()

        if not singlechat and not single_verify:
            if single_chat_serializer.is_valid():
                single_chat_serializer.save()
                return Response(single_chat_serializer.data, status=status.HTTP_201_CREATED)
            return Response(single_chat_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Singlechat already exists."}, status=status.HTTP_400_BAD_REQUEST)


class SingleChatList(APIView):

    def get_object(self, obj, pk):
        try:
            return obj.objects.get(pk=pk)
        except obj.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        single_chat = SingleChat.objects.all()
        singlechat = []
        for single in single_chat:
            if single.contact.pk == pk:
                singlechat.append(single)
        context = {'request': request}
        singlechat_serializer = SingleChatViewSerializer(singlechat, context=context, many=True)
        return Response(singlechat_serializer.data, status=status.HTTP_200_OK)


class MessageSingleChatView(APIView):

    def get_object(self, obj, pk):
        try:
            return obj.objects.get(pk=pk)
        except obj.DoesNotExist:
            raise Http404
    
    def post(self, request, pk, format=None):
        '''
        body: {
            "sent_by": 1,
            "content": "Oi tudo bem?"
        }
        '''
        
        single_chat = SingleChat.objects.get(pk=pk)
        contact = self.get_object(Contact, single_chat.contact.pk)
        chat = single_chat.chat_ptr_id
        request.data['chat'] = chat
        sent_by = request.data['sent_by']
        
        if contact.profile.pk == sent_by or contact.friend.pk == sent_by:
            if not single_chat.status:
                single_chat.add_status
            message_serializer = MessageViewSerializer(data=request.data)
            if message_serializer.is_valid():
                message_serializer.save()
                return Response(message_serializer.data, status=status.HTTP_201_CREATED)
            return Response(message_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "This profile on nonexistent contact"}, status=status.HTTP_400_BAD_REQUEST)


class MessageSingleChatList(APIView):

    def get_object(self, obj, pk):
        try:
            return obj.objects.get(pk=pk)
        except obj.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        messages = Message.objects.filter(chat=pk)
        context = {'request': request}
        messages_serializer = MessageListSerializer(messages, context=context, many=True)
        return Response(messages_serializer.data, status=status.HTTP_200_OK)


class ProfileSigleChatList(APIView):

    def get_object(self, obj, pk):
        try:
            return obj.objects.get(pk=pk)
        except obj.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        profile = Profile.objects.get(pk=pk)
        
        owner = Contact.objects.filter(profile=profile)
        friend = Contact.objects.filter(friend=profile)

        single_chat = SingleChat.objects.all()

        single_chat_list = []

        for single in single_chat:
            if single.contact in owner:
                single_chat_list.append(single)

            if single.contact in friend:
                if single.status:
                    single_chat_list.append(single)

        context = {'request': request}
        single_chat_serializer = SingleChatViewSerializer(single_chat_list, context=context, many=True)
        return Response(single_chat_serializer.data, status=status.HTTP_200_OK)


class GroupChatView(APIView):

    def post(self, request, pk, format=None):
        '''
        body: {
            "title": "name groupchat" 
        }
        '''

        request.data['owner'] = pk
        context = {'request': request}
        group_chat_serializer = GroupChatViewSerializer(data=request.data, context=context)
        if group_chat_serializer.is_valid():
            group_chat_serializer.save()
            return Response(group_chat_serializer.data, status=status.HTTP_201_CREATED)
        return Response(group_chat_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupChatList(APIView):

    def get_object(self, obj, pk):
        try:
            return obj.objects.get(pk=pk)
        except obj.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        profile = self.get_object(Profile, pk)

        group_chat = GroupChat.objects.filter(owner=profile)

        all_groupmember = GroupMember.objects.all()
        
        edit_groupchat = []

        for member in all_groupmember:
            if member.contact.friend == profile :
                find_groupchat = GroupChat.objects.get(chat_ptr_id=member.chat.id)
                edit_groupchat.append(find_groupchat)
        
        for groupchat in group_chat:
            edit_groupchat.append(groupchat)

        context = {'request': request}
        group_chat_serializer = GroupChatListViewSerializer(edit_groupchat, context=context, many=True)
        return Response(group_chat_serializer.data, status=status.HTTP_200_OK)


class GroupChatDetail(APIView):

    def get_object(self, obj, pk):
        try:
            return obj.objects.get(pk=pk)
        except obj.DoesNotExist:
            raise Http404
    
    def get(self, request, pk_profile, pk_groupchat, format=None):
        profile = self.get_object(Profile, pk_profile)
        group_chat = GroupChat.objects.get(owner=profile, pk=pk_groupchat)
        context = {'request': request}
        group_chat_serializer = GroupChatViewSerializer(group_chat, context=context, many=False)
        return Response(group_chat_serializer.data, status=status.HTTP_200_OK)


class GroupMemberView(APIView):

    def get_object(self, obj, pk):
        try:
            return obj.objects.get(pk=pk)
        except obj.DoesNotExist:
            raise Http404
    
    '''
    Fazer uma feature que verificar se esse profile é is_admin
    do grupo, caso ele seja, o mesmo podera adicionar seus contatos 
    ao groupchat, criado por outro profile.

    '''

    def post(self, request, pk, format=None):
        request.data['chat'] = pk

        contact = self.get_object(Contact, request.data['contact'])
        group_chat = self.get_object(GroupChat, pk)
        profile = self.get_object(Profile, group_chat.owner.pk)
        my_contacts = Contact.objects.filter(profile=profile)

        is_my_contact = False
        
        if contact in my_contacts:
            is_my_contact = True

        group_member_serializer = GroupMemberViewSerializer(data=request.data)
        
        if is_my_contact:
            if group_member_serializer.is_valid():
                group_member_serializer.save()
                return Response(group_member_serializer.data, status=status.HTTP_201_CREATED)
            return Response(group_member_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "This contact does not exist in my contact list"}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk, format=None):
        pass


class GroupMemberList(APIView):

    def get_object(self, obj, pk):
        try:
            return obj.objects.get(pk=pk)
        except obj.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        chat = self.get_object(GroupChat, pk)
        group_member = GroupMember.objects.filter(chat=chat)
        context = {'request': request}
        group_member_serializer = GroupMemberViewSerializer(group_member, context=context, many=True)
        return Response(group_member_serializer.data, status=status.HTTP_200_OK)


class MessageGroupChatView(APIView):

    def get_object(self, obj, pk):
        try:
            return obj.objects.get(pk=pk)
        except obj.DoesNotExist:
            raise Http404
    
    def post(self, request, pk, format=None):
        '''
        body: {
            "sent_by": 1,
            "content": "Oi tudo bem?"
        }
        '''
        
        group_chat = GroupChat.objects.get(pk=pk)

        request.data['chat'] = pk

        sent_by = request.data['sent_by']

        group_member = GroupMember.objects.filter(chat=pk)

        is_member = False

        for member in group_member:
            if (member.contact.profile.pk == sent_by or 
                member.contact.friend.pk == sent_by):
                is_member = True

        message_group_serializer = MessageViewSerializer(data=request.data)

        if is_member:
            if message_group_serializer.is_valid():
                message_group_serializer.save()
                return Response(message_group_serializer.data, status=status.HTTP_201_CREATED)
            return Response(message_group_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "This profile is not a member of this group"}, status=status.HTTP_400_BAD_REQUEST)
        

class MessageGroupChatList(APIView):

    def get_object(self, obj, pk):
        try:
            return obj.objects.get(pk=pk)
        except obj.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        messages = Message.objects.filter(chat=pk)
        context = {'request': request}
        messages_serializer = MessageListSerializer(messages, context=context, many=True)
        return Response(messages_serializer.data, status=status.HTTP_200_OK)


class ApiRoot(APIView):

    def get(self, request, *args, **kwargs):

        data = {
            
            'profiles': reverse('profile-list-view', request=request),
  
        }

        return Response(data, status=status.HTTP_200_OK)
