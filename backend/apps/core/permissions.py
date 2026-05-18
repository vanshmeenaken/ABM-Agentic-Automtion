"""
Permission classes for Ken ABM Platform.
Implements role-based access control (RBAC) for the platform.
"""

from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Allow access only to admin users."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class IsAuthenticated(permissions.IsAuthenticated):
    """Ensure user is authenticated."""

    pass


class HasRole(permissions.BasePermission):
    """
    Base permission class for role-based access.
    Subclasses should define required_roles.
    """

    required_roles = []

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # Check if user has admin or required groups
        if request.user.is_staff:
            return True

        user_groups = request.user.groups.values_list("name", flat=True)
        return any(role in user_groups for role in self.required_roles)


class IsCampaignManager(HasRole):
    """Allow access to campaign_manager role and above."""

    required_roles = ["campaign_manager", "admin"]


class IsApprover(HasRole):
    """Allow access to approver role and above."""

    required_roles = ["approver", "admin"]


class IsViewer(HasRole):
    """Allow read-only access to viewer role and above."""

    required_roles = ["viewer", "campaign_manager", "approver", "admin"]

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return super().has_permission(request, view)
