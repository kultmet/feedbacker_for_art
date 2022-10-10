from rest_framework import permissions


class IsAuthorOrModeratorOrAdminOrReadOnly(permissions.BasePermission):
    message = 'Изменение чужого контента запрещено!'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # return (request.method in permissions.SAFE_METHODS
        #         or obj.author == request.user
        #         or request.user.role == 'moderator'
        #         or request.user.role == 'admin'
        #         )
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user)



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
