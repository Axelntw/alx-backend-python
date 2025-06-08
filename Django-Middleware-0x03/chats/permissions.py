from rest_framework import permissions
from .models import Conversation


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    Allows GET, POST, PUT, PATCH, DELETE methods for participants.
    """

    def has_permission(self, request, view):
        # Check if user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check if user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Allow all HTTP methods (GET, POST, PUT, PATCH, DELETE) for participants
        allowed_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
        
        if request.method not in allowed_methods:
            return False
        
        # If obj is a Conversation, check if user is a participant
        if isinstance(obj, Conversation):
            return obj.participants.filter(id=request.user.id).exists()
        
        # If obj is a Message, check if user is a participant of the conversation
        if hasattr(obj, 'conversation'):
            return obj.conversation.participants.filter(id=request.user.id).exists()
        
        return False


class IsOwnerOrParticipant(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or conversation participants to access it.
    Supports PUT, PATCH, DELETE operations.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Allow all methods including PUT, PATCH, DELETE
        allowed_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
        
        if request.method not in allowed_methods:
            return False
        
        # For PUT, PATCH, DELETE operations, check ownership or participation
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            # Check if user is the owner
            if hasattr(obj, 'sender') and obj.sender == request.user:
                return True
            
            # For DELETE, only allow sender to delete their own messages
            if request.method == 'DELETE' and hasattr(obj, 'sender'):
                return obj.sender == request.user
        
        # Check if user is a participant of the conversation
        if hasattr(obj, 'conversation'):
            return obj.conversation.participants.filter(id=request.user.id).exists()
        
        return False