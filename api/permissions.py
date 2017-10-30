from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.permissions import BasePermission

UserModel = get_user_model()


class IsStaffOrReadOnly(BasePermission):
    """
    The request is not POST or the request user is the staff.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        try:
            staff = UserModel.objects.filter(is_staff=True)
        except UserModel.DoesNotExist:
            # Reject any requests for an invalid user
            return False

        return request.user in staff