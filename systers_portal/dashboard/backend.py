from __future__ import unicode_literals
from django.contrib.auth.backends import ModelBackend

from dashboard.models import CommunityPage, SysterUser


class CustomBackend(ModelBackend):
    """Overrides the ModelBackend's has_perm method
    to grant all rights to editors of Community Page
    model instance"""

    def has_perm(self, user_obj, perm, obj=None):
        """If obj is a Community page model instance and if user is
        in editors list of this object,grants all rights to the user
        else use the default behaviour of ModelBackend's has_perm method

        :param user_obj: user object for which the permission is checked
        :param perm: permission
        :obj: a model instance
        """
        if not user_obj.is_active:
            return False
        if isinstance(obj, CommunityPage):
            editors = SysterUser.objects.filter(editor_of_page=obj)
            if user_obj.systeruser in editors:
                return True
            else:
                return False
        return perm in self.get_all_permissions(user_obj, obj)
