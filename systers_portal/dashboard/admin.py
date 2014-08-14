from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from dashboard.models import (
    SysterUser, Community, News, Resource, Tag, ResourceType,
    CommunityPage, NewsComment, ResourceComment, JoinRequest)
from cms.admin.placeholderadmin import PlaceholderAdminMixin


class CommunityPageAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    pass


class CommunityAdmin(GuardedModelAdmin):
    pass


admin.site.register(CommunityPage, CommunityPageAdmin)
admin.site.register(SysterUser)
admin.site.register(JoinRequest)
admin.site.register(NewsComment)
admin.site.register(ResourceComment)
admin.site.register(Community, CommunityAdmin)
admin.site.register(News)
admin.site.register(Resource)
admin.site.register(Tag)
admin.site.register(ResourceType)
