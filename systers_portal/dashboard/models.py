from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from cms.models.pagemodel import Page


class SysterUser(models.Model):
    """Profile model to store additional information about a user"""
    user = models.OneToOneField(User)
    country = CountryField(blank=True, null=True)
    blog_url = models.URLField(max_length=255, blank=True)
    homepage_url = models.URLField(max_length=255, blank=True)
    profile_picture = models.ImageField(upload_to='photos/',
                                        default='photos/dummy.jpeg',
                                        blank=True,
                                        null=True)

    def __unicode__(self):
        firstname = self.user.first_name
        lastname = self.user.last_name
        if firstname and lastname:
            return "{0} {1}".format(self.user.first_name, self.user.last_name)
        else:
            return self.user.username


class Community(models.Model):
    """Model to represent a Syster Community"""
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, blank=True)
    mailing_list = models.EmailField(max_length=255, blank=True)
    resource_area = models.URLField(max_length=255, blank=True)
    members = models.ManyToManyField(SysterUser, blank=True, null=True,
                                     related_name='member_of_community')
    community_admin = models.ForeignKey(SysterUser, related_name='community')
    parent_community = models.ForeignKey('self', blank=True, null=True)
    website = models.URLField(max_length=30, blank=True)
    facebook = models.URLField(max_length=30, blank=True)
    googleplus = models.URLField(max_length=30, blank=True)
    twitter = models.URLField(max_length=30, blank=True)

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    """Model to represent the tags a resource can have"""
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class ResourceType(models.Model):
    """Model to represent the types a resource can have"""
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class News(models.Model):
    """Model to represent a News section on Community resource area"""
    title = models.CharField(max_length=255)
    community = models.ForeignKey(Community)
    author = models.ForeignKey(SysterUser)
    date_created = models.DateField(auto_now=False, auto_now_add=True)
    date_modified = models.DateField(auto_now=True, auto_now_add=False)
    is_public = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    content = models.TextField()

    def __unicode__(self):
        return "{0} of {1} Community".format(self.title, self.community.name)


class CommunityPage(models.Model):
    """Model to represent community pages"""
    title = models.CharField(max_length=255)
    page = models.OneToOneField(Page)
    community = models.ForeignKey(Community)

    def __unicode__(self):
        return "{0} of {1} Community".format(self.page, self.community.name)


class Resource(models.Model):
    """Model to represent a Resources section on Community resource area"""
    title = models.CharField(max_length=255)
    community = models.ForeignKey(Community)
    author = models.ForeignKey(SysterUser)
    date_created = models.DateField(auto_now=False, auto_now_add=True)
    date_modified = models.DateField(auto_now=True, auto_now_add=False)
    is_public = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    resource_type = models.ForeignKey(ResourceType, blank=True, null=True)
    content = models.TextField()

    def __unicode__(self):
        return "{0} of {1} Community".format(self.title, self.community.name)
