from django.urls import path, include
from rest_framework_nested import routers
from .views import ConversationViewSet, MessageViewSet

# Create a router instance routers.DefaultRouter()
router = routers.DefaultRouter()
router.register('conversations', ConversationViewSet, basename='conversation')

messages_router = routers.NestedDefaultRouter(router, 'conversations', lookup='conversation')
messages_router.register('messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(messages_router.urls)),
]
