from __future__ import unicode_literals
from django.contrib.auth.backends import ModelBackend

from dashboard.models import CommunityPage


class CustomBackend(ModelBackend):

    """Overrides the ModelBackend's has_perm method
    to grant all rights on Community Page to users who have
    change_community_page permissions on Community to which the page belongs"""

    def has_perm(self, user_obj, perm, obj=None):
        """If obj is a Community page model instance and if user is
        change_community_page for the community to which the page belongs ,
        grants all rights to the user on the page for editing
        else use the default behaviour of ModelBackend's has_perm method

        :param user_obj: user object for which the permission is checked
        :param perm: permission
        :obj: a model instance
        """
        if not user_obj.is_active:
            return False
        if isinstance(obj, CommunityPage):
            return user_obj.has_perm('change_community_page', obj.community)
        return perm in self.get_all_permissions(user_obj, obj)
