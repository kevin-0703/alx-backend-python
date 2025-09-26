from rest_framework import permissions

class IsParticipantorReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        if hasattr(obj, "sender_id"):
            return request.user in obj.sender_id.participants.all()
        return False