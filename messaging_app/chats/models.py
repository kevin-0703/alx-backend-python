from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
  ROLES = (
    ('admin', 'Admin'),
    ('user', 'User'),
    ('guest', 'Guest'),
  )

  user_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
  first_name = models.CharField(max_length=30, null=False)
  last_name = models.CharField(max_length=30, null=False)
  email = models.EmailField(unique=True, null=False, db_index=True)
  phone_number = models.CharField(max_length=128, null=False)
  role = models.CharField(max_length=10, choices=ROLES, default='guest')
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.first_name + ' ' + self.last_name

class conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Conversation {self.conversation_id}'

class message(models.Model):
    message_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE)
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender_id} at {self.sent_at}'