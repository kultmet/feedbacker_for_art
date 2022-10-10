from rest_framework import permissions

# Пермишены для моделей юзера


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


# Пермишены для моделей Title, Category, Genre

class TitlePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.role == 'admin' or request.user.is_superuser:
            return True
        return False

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.role == 'admin' or request.user.is_superuser:
            return True
        return False
    """"
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                or request.user.role == 'admin'
                or request.user.is_superuser)

    def has_object_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                or request.user.role == 'admin'
                or request.user.is_superuser)
    """

# Пермишены для моделей Review, Comment


class ReviewPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role == 'admin'
                or request.user.role == 'moderator'
                or obj.author == request.user)
