from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        if hasattr(obj, "conversation_id"):
            conversation = obj.conversation_id
            if request.method in ["PUT", "PATCH", "DELETE"]:
                return request.user == conversation in conversation.participations.all()
            return request.user in conversation.participations.all()
        return False