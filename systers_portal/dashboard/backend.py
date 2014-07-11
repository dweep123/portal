from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.auth.backends import ModelBackend

from dashboard.models import CommunityPage
from dashboard.models import (
    SysterUser, Community, News, Resource, Tag, ResourceType,
    CommunityPage)


class MyCustomBackend(ModelBackend):
	
    def has_perm(self, user_obj, perm, obj=None):
        if not user_obj.is_active:
            return False
	if isinstance(obj, CommunityPage):
	    print perm
	    editors = SysterUser.objects.filter(editor_of_page=obj)
	    if user_obj.systeruser in editors:
	        return True 
	    else:
	        return False
        return perm in self.get_all_permissions(user_obj, obj)
