from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet

# Create a router instance routers.DefaultRouter()
router = routers.DefaultRouter()
router.register('conversations', ConversationViewSet, basename='conversation')
router.register(
    r'conversations/(?P<conversation_pk>[^/.]+)/messages',
    MessageViewSet,
    basename='message'
)

urlpatterns = [
    path('', include(router.urls)),
]
