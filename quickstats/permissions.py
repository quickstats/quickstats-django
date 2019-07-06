from rest_framework import permissions


class IsOwnerOrPublic(permissions.IsAuthenticatedOrReadOnly):
    message = "Not object owner or public"

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        if request.method in permissions.SAFE_METHODS:
            return obj.public
        return False


class CanSubscribe(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        if obj.public:
            return True
        return False


class IsOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner
