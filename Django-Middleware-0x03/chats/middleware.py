import logging
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