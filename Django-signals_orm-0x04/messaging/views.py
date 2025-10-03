from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .models import Message

# Create your views here.
@cache_page(60)  # cache for 60 seconds
def conversation_view(request, user_id):
    messages = Message.objects.filter(receiver_id=user_id).select_related("sender")
    return render(request, "conversation.html", {"messages": messages})
