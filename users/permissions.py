from rest_framework import permissions


class UpdateDetailPermission(permissions.BasePermission):
    
    """Checks if the user wants to update data then the same should be the owner of profile"""
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method == "PATCH":
                if request.parser_context['kwargs']['id'] == request.user.id:
                    return True
                return False
            return True

        return False
