from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

# Create your views here.

class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing conversations"""
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter conversations to only those user participates in"""
        return self.queryset.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        """Create a new conversation with participants"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()
        
        # Add current user to participants if not included
        if request.user not in conversation.participants.all():
            conversation.participants.add(request.user)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for managing messages"""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter messages by conversation"""
        conversation_id = self.kwargs.get('conversation_pk')
        return self.queryset.filter(conversation_id=conversation_id)

    def create(self, request, *args, **kwargs):
        """Create a new message in the conversation"""
        conversation_id = self.kwargs.get('conversation_pk')
        if not conversation_id:
            return Response(
                {"error": "Conversation ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Add conversation and sender to message data
        data = request.data.copy()
        data['conversation'] = conversation_id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=request.user)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
