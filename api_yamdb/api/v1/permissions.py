from rest_framework import permissions


# class AuthorOrModeratorOrAdminOrReadOnly(permissions.BasePermission):
#     message = 'Изменение чужого контента запрещено!'

#     def has_permission(self, request, view):
#         return (request.method in permissions.SAFE_METHODS
#                 or request.user.is_authenticated)

#     def has_object_permission(self, request, view, obj):
#         return (request.method in permissions.SAFE_METHODS
#                 or obj.author == request.user
#                 or obj.moderator == request.user
#                 or obj.admin == request.user
#                 )

class IsAdminOrSuperuserPermission(permissions.BasePermission):
    message = 'Ваши полномочия здесь все...'

    def has_permission(self, request, view):
        if request.user.role == 'admin' or request.user.is_superuser:
            return True
        return False

class IsModeratorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'moderator':
            return True
        return False
