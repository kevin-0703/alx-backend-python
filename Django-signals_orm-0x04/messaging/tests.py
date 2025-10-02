from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from messaging.models import Message, Notification

u1 = User.objects.create_user("alice", password="test123")
u2 = User.objects.create_user("bob", password="test123")

msg = Message.objects.create(sender=u1, receiver=u2, content="Hello Bob!")
