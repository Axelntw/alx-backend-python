import django_filters
from django.contrib.auth.models import User
from .models import Message, Conversation


class MessageFilter(django_filters.FilterSet):
    conversation = django_filters.NumberFilter(field_name='conversation__id')
    sender = django_filters.CharFilter(field_name='sender__username', lookup_expr='icontains')
    content = django_filters.CharFilter(field_name='content', lookup_expr='icontains')
    timestamp_after = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte')
    timestamp_before = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')
    date_range = django_filters.DateFromToRangeFilter(field_name='timestamp')

    class Meta:
        model = Message
        fields = ['conversation', 'sender', 'content', 'timestamp_after', 'timestamp_before']


class ConversationFilter(django_filters.FilterSet):
    participant = django_filters.CharFilter(method='filter_by_participant')
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Conversation
        fields = ['participant', 'created_after', 'created_before']

    def filter_by_participant(self, queryset, name, value):
        try:
            user = User.objects.get(username__icontains=value)
            return queryset.filter(participants=user)
        except User.DoesNotExist:
            return queryset.none()