from django.contrib import admin
from dashboard.models import (
    SysterUser, Community, News, Resource, Tag, Resource_Type,
    CommunityPage)

admin.site.register(SysterUser)
admin.site.register(Community)
admin.site.register(News)
admin.site.register(Resource)
admin.site.register(Tag)
admin.site.register(Resource_Type)
admin.site.register(CommunityPage)
