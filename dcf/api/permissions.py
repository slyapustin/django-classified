from rest_framework import permissions


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow staff to edit objects.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # TODO: rewrite this permission for work with all methods
        # now this is work with GET, HEAD and OPTIONS only
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to staff.
        return request.user.is_staff
