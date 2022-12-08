from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST'] and \
                not view.kwargs.get('username', None):
            return True
        elif request.user.is_authenticated and \
                view.kwargs.get('username', None) == request.user.username:
            return True
        return False
