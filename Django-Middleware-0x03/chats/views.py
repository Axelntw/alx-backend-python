from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation, IsOwnerOrParticipant
from .filters import MessageFilter, ConversationFilter
from .pagination import CustomPagination


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = ConversationFilter
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    search_fields = ['participants__username']

    def get_queryset(self):
        # Only return conversations where the current user is a participant
        queryset = Conversation.objects.filter(
            participants=self.request.user
        ).distinct()
        
        # Filter by conversation_id if provided
        conversation_id = self.request.query_params.get('conversation_id', None)
        if conversation_id is not None:
            queryset = queryset.filter(id=conversation_id)
        
        return queryset

    def perform_create(self, serializer):
        conversation = serializer.save()
        # Add the creator as a participant
        conversation.participants.add(self.request.user)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """Get all messages for a specific conversation"""
        conversation = self.get_object()
        messages = Message.objects.filter(
            conversation=conversation,
            conversation_id=conversation.id
        ).order_by('-timestamp')
        
        # Apply pagination
        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = MessageSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrParticipant]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = MessageFilter
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']
    search_fields = ['content', 'sender__username']

    def get_queryset(self):
        # Only return messages from conversations where the user is a participant
        queryset = Message.objects.filter(
            conversation__participants=self.request.user
        ).distinct()
        
        # Filter by conversation_id if provided
        conversation_id = self.request.query_params.get('conversation_id', None)
        if conversation_id is not None:
            queryset = queryset.filter(conversation_id=conversation_id)
        
        return queryset

    def perform_create(self, serializer):
        # Set the sender to the current user and ensure conversation_id is set
        conversation = serializer.validated_data.get('conversation')
        serializer.save(
            sender=self.request.user,
            conversation_id=conversation.id if conversation else None
        )

    def update(self, request, *args, **kwargs):
        # Only allow the sender to update their own messages (PUT/PATCH)
        message = self.get_object()
        if message.sender != request.user:
            return Response(
                {'error': 'You can only update your own messages'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Only allow the sender to delete their own messages (DELETE)
        message = self.get_object()
        if message.sender != request.user:
            return Response(
                {'error': 'You can only delete your own messages'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
