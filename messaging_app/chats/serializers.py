from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    conversation_count = serializers.SerializerMethodField()

    def get_conversation_count(self, obj):
        return obj.conversations.count()

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 
                 'last_name', 'phone_number', 'bio', 'avatar', 'conversation_count']
        read_only_fields = ['user_id']


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model"""
    sender_name = serializers.CharField(source='sender.get_full_name', read_only=True)
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'sender_name', 
                 'message_body', 'sent_at', 'is_read']
        read_only_fields = ['message_id', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation model with nested relationships"""
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    def get_message_count(self, obj):
        return obj.messages.count()

    def get_last_message(self, obj):
        last_message = obj.messages.last()
        return MessageSerializer(last_message).data if last_message else None

    def validate_participants(self, value):
        if len(value) < 2:
            raise serializers.ValidationError(
                "Conversation must have at least 2 participants"
            )
        return value

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'name', 'participants', 
                 'messages', 'message_count', 'last_message', 'created_at', 'updated_at']
        read_only_fields = ['conversation_id', 'created_at', 'updated_at']

    def create(self, validated_data):
        participants = self.context['request'].data.get('participants', [])
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participants)
        return conversation
