from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from collections import defaultdict
import re


class RestrictAccessByTimeMiddleware:
    """Middleware that restricts access to chat during certain hours (outside 9AM-6PM)"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check if this is a chat-related request
        if request.path.startswith('/chats/') or 'chat' in request.path:
            current_time = timezone.now().time()
            
            # Define allowed hours: 9AM to 6PM (09:00 to 18:00)
            start_time = datetime.strptime('09:00', '%H:%M').time()
            end_time = datetime.strptime('18:00', '%H:%M').time()
            
            # Check if current time is outside allowed hours
            if not (start_time <= current_time <= end_time):
                return JsonResponse(
                    {'error': 'Chat access is restricted outside business hours (9AM-6PM)'},
                    status=403
                )
        
        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware:
    """Middleware that detects offensive language and implements rate limiting"""
    
    # Class-level storage for IP tracking (in production, use Redis or database)
    ip_message_count = defaultdict(list)
    
    # List of offensive words (expand as needed)
    OFFENSIVE_WORDS = [
        'spam', 'abuse', 'hate', 'offensive', 'inappropriate',
        'badword1', 'badword2', 'profanity'  # Add actual offensive words
    ]
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.max_messages = 5  # Maximum messages per time window
        self.time_window = 60  # Time window in seconds (1 minute)
    
    def __call__(self, request):
        # Only check POST requests to chat endpoints
        if request.method == 'POST' and (request.path.startswith('/chats/') or 'chat' in request.path):
            client_ip = self.get_client_ip(request)
            current_time = timezone.now()
            
            # Clean old entries for this IP
            self.clean_old_entries(client_ip, current_time)
            
            # Check rate limit
            if len(self.ip_message_count[client_ip]) >= self.max_messages:
                return JsonResponse(
                    {'error': f'Rate limit exceeded. Maximum {self.max_messages} messages per minute allowed.'},
                    status=429
                )
            
            # Check for offensive language in message content
            if hasattr(request, 'data') and 'message' in request.data:
                message_content = request.data.get('message', '')
            elif request.POST.get('message'):
                message_content = request.POST.get('message', '')
            else:
                # Try to get message from request body
                try:
                    import json
                    body = json.loads(request.body.decode('utf-8'))
                    message_content = body.get('message', '')
                except:
                    message_content = ''
            
            if self.contains_offensive_language(message_content):
                return JsonResponse(
                    {'error': 'Message contains inappropriate content and has been blocked.'},
                    status=400
                )
            
            # Add timestamp for this request
            self.ip_message_count[client_ip].append(current_time)
        
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        """Get the client's IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def clean_old_entries(self, ip, current_time):
        """Remove entries older than the time window"""
        cutoff_time = current_time - timedelta(seconds=self.time_window)
        self.ip_message_count[ip] = [
            timestamp for timestamp in self.ip_message_count[ip]
            if timestamp > cutoff_time
        ]
    
    def contains_offensive_language(self, message):
        """Check if message contains offensive language"""
        if not message:
            return False
        
        message_lower = message.lower()
        for word in self.OFFENSIVE_WORDS:
            if re.search(r'\b' + re.escape(word.lower()) + r'\b', message_lower):
                return True
        return False


class RolePermissionMiddleware:
    """Middleware that enforces role-based permissions for chat access"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check if this is a chat-related request that requires admin/moderator access
        if self.requires_role_check(request):
            # Check if user is authenticated
            if not request.user.is_authenticated:
                return JsonResponse(
                    {'error': 'Authentication required'},
                    status=401
                )
            
            # Check if user has required role
            if not self.has_required_role(request.user):
                return JsonResponse(
                    {'error': 'Access denied. Admin or moderator role required.'},
                    status=403
                )
        
        response = self.get_response(request)
        return response
    
    def requires_role_check(self, request):
        """Determine if the request requires role checking"""
        # Check for admin-only endpoints
        admin_paths = [
            '/chats/admin/',
            '/chats/moderate/',
            '/chats/delete/',
            '/chats/ban/',
        ]
        
        # Check if path requires admin access
        for path in admin_paths:
            if request.path.startswith(path):
                return True
        
        # Check for DELETE, PUT methods on chat endpoints (admin actions)
        if request.method in ['DELETE', 'PUT'] and request.path.startswith('/chats/'):
            return True
        
        return False
    
    def has_required_role(self, user):
        """Check if user has admin or moderator role"""
        # Check if user is superuser (admin)
        if user.is_superuser or user.is_staff:
            return True
        
        # Check for custom role fields (if you have them)
        # Assuming you might have a profile model with roles
        try:
            if hasattr(user, 'profile'):
                user_role = getattr(user.profile, 'role', None)
                if user_role in ['admin', 'moderator']:
                    return True
        except:
            pass
        
        # Check groups
        user_groups = user.groups.values_list('name', flat=True)
        allowed_groups = ['admin', 'moderator', 'administrators', 'moderators']
        
        if any(group.lower() in [g.lower() for g in allowed_groups] for group in user_groups):
            return True
        
        return False