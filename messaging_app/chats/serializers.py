from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 
                 'last_name', 'phone_number', 'bio', 'avatar']
        read_only_fields = ['user_id']


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model"""
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 
                 'message_body', 'sent_at', 'is_read']
        read_only_fields = ['message_id', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation model with nested relationships"""
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'name', 'participants', 
                 'messages', 'created_at', 'updated_at']
        read_only_fields = ['conversation_id', 'created_at', 'updated_at']

    def create(self, validated_data):
        participants = self.context['request'].data.get('participants', [])
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participants)
        return conversation
