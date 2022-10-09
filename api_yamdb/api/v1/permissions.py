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


# class IsadminForMePagePermission(permissions.BasePermission):

#     def has_object_permission(self, request, view, obj):
#         # Read permissions are allowed to any request,
#         # so we'll always allow GET, HEAD or OPTIONS requests.
#         if request.method in permissions.SAFE_METHODS:
#             return True

#         # Instance must have an attribute named `owner`.
#         if request.user.role == 'admin':

#             return 
#         return 
    


# class IsSuperuserPermission(permissions.BasePermission):

#     def has_permission(self, request, view):
#         if request.user.role == 'admin':
#             return True
#         return False