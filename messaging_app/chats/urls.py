from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Create a router instance routers.DefaultRouter()
router = DefaultRouter()

# Register viewsets with the router
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(
    r'conversations/(?P<conversation_pk>[^/.]+)/messages',
    MessageViewSet,
    basename='conversation-messages'
)

# Wire up our API using automatic URL routing
urlpatterns = [
    path('', include(router.urls)),
]
