"""
Permission classes for Campaign operations.
"""

from rest_framework import permissions
from apps.core.permissions import HasRole


class CampaignPermission(permissions.BasePermission):
    """
    Campaign-level permissions.
    - campaign_manager+ can create/edit campaigns
    - viewer can read only
    - owner can edit their own campaigns
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # Safe methods (GET) allowed for authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True

        # Dangerous methods (POST, PUT, DELETE, PATCH)
        # Require campaign_manager role or higher
        user_groups = request.user.groups.values_list("name", flat=True)
        required_roles = ["campaign_manager", "admin"]
        return request.user.is_staff or any(role in user_groups for role in required_roles)

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        # Read access for authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write access: owner or admin or campaign_manager
        user_groups = request.user.groups.values_list("name", flat=True)
        is_manager = request.user.is_staff or any(
            role in user_groups for role in ["campaign_manager", "admin"]
        )
        is_owner = obj.owner == request.user

        return is_manager or is_owner


class CanApproveCampaigns(permissions.BasePermission):
    """
    Permission to approve/reject campaigns.
    Only admin and approver roles can approve campaigns.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        user_groups = request.user.groups.values_list("name", flat=True)
        required_roles = ["approver", "admin"]
        return request.user.is_staff or any(role in user_groups for role in required_roles)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class CanManageCampaign(permissions.BasePermission):
    """
    Permission to pause, resume, or delete campaigns.
    Owner, campaign_manager, or admin can manage.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        user_groups = request.user.groups.values_list("name", flat=True)
        is_manager = request.user.is_staff or any(
            role in user_groups for role in ["campaign_manager", "admin"]
        )
        is_owner = obj.owner == request.user

        return is_manager or is_owner
