from rest_framework import permissions


class UpdateDetailPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "PATCH":
            if request.parser_context['kwargs']['id'] == request.user.id:
                return True
            return False
        return True
