from django.shortcuts import render
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from rest_framework import filters
from .permissions import IsParticipantOfConversation
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
User = get_user_model()
# Create your views here.
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    seralizer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["participants__username"]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user) 

    def create (self, request, *args, **kwargs):
        participants_id = request.data.get('participants', [])
        if not participants_id or len(participants_id) < 2:
            return Response({'error': 'At least two participants are required to create a conversation.'}, status=status.HTTP_400_BAD_REQUEST)
        
        participants = User.objects.filter(id_in=participants_id)
        if participants.count() <2:
            return Response({'error': 'Some participants do not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class MessageFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        conversation_id = request.query_params.get('conversation_id')
        if conversation_id:
            queryset = queryset.filter(conversation__id=conversation_id)
        return queryset

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [MessageFilterBackend, filters.OrderingFilter]
    
    def get_queryset(self):
        return Message.objects.filter(conversation_participants=self.request.user)
    def create (self, request, *args, **kwargs):
        sender_id = request.data.get('sender_id')
        message_body = request.data.get('message_body')
        conversation_id = request.data.get('conversation_id')
        conversation = serializer.validated_data.get('conversation_id')

        if self.request.user not in conversation.participants.all():
            return Response (
                {"detail": "You do not have permission to send messages in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save(sender_id=self.request.user)

        if not sender_id or message_body is None or not conversation_id:
            return Response({'error': 'sender_id, message_body and conversation_id are required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        message = Message.objects.create(sender_id=sender_id, message_body=message_body, conversation=conversation)
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)