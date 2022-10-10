from rest_framework import permissions


class IsAuthorOrModeratorOrAdminOrReadOnly(permissions.BasePermission):
    """Предоставление прав доступа на изменение отзывов и комментариев
    для авторов, администратора и модератора"""

    message = 'Изменение чужого контента запрещено!'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role == 'admin'
                or request.user.role == 'moderator'
                or obj.author == request.user)


class TitleIsAdminOrReadOnly(permissions.BasePermission):
    # def has_object_permission(self, request, view, obj):
    #     if request.method in permissions.SAFE_METHODS:
    #         return True
    #     elif request.user.is_authenticated:
    #         return True
    #     elif request.user.role == 'admin' or request.user.is_superuser:
    #         return True

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
                request.user.role == 'admin' or request.user.is_superuser)
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        # if request.user.is_authenticated:
        #     return True
        # if request.user.role == 'admin' or request.user.is_superuser:
        #     return True
        # return False

class IsAdminOrSuperuserPermission(permissions.BasePermission):
    message = 'Ваши полномочия здесь все...'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated and request.user.role == 'admin':
            return True
        elif request.user.is_superuser:
            return True



class IsModeratorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'moderator':
            return True



class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS
            # or request.user.is_authenticated
            # or request.user.role == 'admin'
            # or request.user.is_staff
            # or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user == 'admin'
