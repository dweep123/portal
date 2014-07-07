from django.contrib import admin
from dashboard.models import (
    SysterUser, Community, News, Resource, Tag, ResourceType,
    CommunityPage)
from cms.admin.placeholderadmin import PlaceholderAdminMixin
from cms.admin.placeholderadmin import FrontendEditableAdminMixin

class CommunityPageAdmin(PlaceholderAdminMixin,admin.ModelAdmin):
    pass
#    prepopulated_fields = {'slug': ('title',)}

admin.site.register(CommunityPage, CommunityPageAdmin)
admin.site.register(SysterUser)
admin.site.register(Community)
admin.site.register(News)
admin.site.register(Resource)
admin.site.register(Tag)
admin.site.register(ResourceType)
