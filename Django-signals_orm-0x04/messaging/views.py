from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .models import Message
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
# Create your views here.
@cache_page(60)  # cache for 60 seconds
def conversation_view(request, user_id):
    messages = Message.objects.filter(receiver_id=user_id).select_related("sender")
    return render(request, "conversation.html", {"messages": messages})

@login_required
def delete_user(request):
    user = request.user
    user.delete()  
    return redirect("/") 