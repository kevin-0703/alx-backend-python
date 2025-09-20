from django.contrib.auth import get_user_model
from .models import Conversation, Message
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    email = serializers.EmailField(required=True)
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'password', 'created_at']
        extra_kwargs = {'password': {'write_only': True}}
    def validation_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    class Meta:
        model = Message
        fields = ['message_id', 'sender_id', 'message_body', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at']

    def get_messages(self, obj):
        messages = obj.messages.order_by('sent_at')
        return MessageSerializer(messages, many=True).data