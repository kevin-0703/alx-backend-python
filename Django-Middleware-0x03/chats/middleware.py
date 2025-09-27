import logging
import time
from django.http import JsonResponse
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)
handler = logging.FileHandler('requests.log')
formatter = logging.Formatter("%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        respone = self.get_response(request)
        return respone
    
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        current_hour = datetime.now().hour
        if 9<= current_hour < 17:
            return self.get_response(request)
        else:
            
            return Response (
                {'error': 'Access is restricted to business hours (9 AM to 5 PM).'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if request.method == "POST" and "/messages" in request.path:
            ip = self.get_client_ip(request)
            current_time = time.time()

            if ip not in request.log:
                request.log[ip] = []

            request.log[ip] = [
                ts for ts in request.log[ip] if current_time - ts < 60
            ]
            if len(request.log[ip]) >= 5:
                return JsonResponse (
                    {'error': 'Rate limit exceeded. Max 5 messages per minute.'}, 
                    status=429
                )
            request.log[ip].append(current_time)
        return self.get_response(request)
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if request.user.is_authenticated:
            if request.user.role == 'admin' or 'modurator':
                return self.get_response(request)
            else:
                return JsonResponse (
                    {'error': 'You do not have permission to access this resource.'}, 
                    status=403
                )
        else:
            return JsonResponse (
                {'error': 'Authentication required.'}, 
                status=401
            )