from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .models import Message
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
# Create your views here.
@login_required
def inbox(request):
    unread_messages = Message.unread.unread_for_user(request.user)
    return render(request, "inbox.html", {"messages": unread_messages})

@cache_page(60)  # cache for 60 seconds
def conversation_view(request, user_id):
    thread = (
       Message.objects.filter(receiver_id=user_id, sender=request.user)
       .select_related("sender", "receiver")
       .prefetch_related("replies")
    )
    return render(request, "conversation.html", {"messages": thread})

@login_required
def delete_user(request):
    user = request.user
    user.delete()  
    return redirect("/") 