from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.core.urlresolvers import reverse
from django.db import models
from cms.models.fields import PlaceholderField


class SysterUser(models.Model):

    """Profile model to store additional information about a user"""
    user = models.OneToOneField(User)
    country = CountryField(blank=True, null=True, verbose_name="Country")
    blog_url = models.URLField(max_length=255, blank=True, verbose_name="Blog")
    homepage_url = models.URLField(max_length=255, blank=True,
                                   verbose_name="Homepage")
    profile_picture = models.ImageField(upload_to='photos/',
                                        blank=True,
                                        null=True,
                                        verbose_name="Photo")

    def __unicode__(self):
        firstname = self.user.first_name
        lastname = self.user.last_name
        if firstname and lastname:
            return "{0} {1}".format(self.user.first_name, self.user.last_name)
        else:
            return self.user.username

    def get_absolute_url(self):
        return reverse('view_user_profile', args=[self.user.username])

    def get_user_fields(self):
        """Set verbose name for User fields and Get model fields of a User object

        :return: list of tuples (fieldname, fieldvalue)
        """
        User._meta.get_field('first_name').verbose_name = 'First Name'
        User._meta.get_field('last_name').verbose_name = 'Last Name'
        User._meta.get_field('email').verbose_name = 'Email'
        return [(field.name, getattr(self.user, field.name)) for field in
                User._meta.fields]

    def get_fields(self):
        """Get model fields of a SysterUser object

        :return: list of tuples (fieldname, fieldvalue)
        """
        return [(field.name, getattr(self, field.name)) for field in
                SysterUser._meta.fields]


def user_unicode(self):
    if self.first_name and self.last_name:
        return "{0} {1}".format(self.first_name, self.last_name)
    else:
        return self.username

User.__unicode__ = user_unicode


class Community(models.Model):

    """Model to represent a Syster Community"""
    name = models.CharField(max_length=255, verbose_name="Name")
    slug = models.SlugField(max_length=150, unique=True, verbose_name="Slug")
    email = models.EmailField(max_length=255, blank=True, verbose_name="Email")
    mailing_list = models.EmailField(max_length=255, blank=True,
                                     verbose_name="Mailing List")
    resource_area = models.URLField(max_length=255, blank=True,
                                    verbose_name="Resource area")
    members = models.ManyToManyField(SysterUser, blank=True, null=True,
                                     related_name='member_of_community',
                                     verbose_name="Members")
    community_admin = models.ForeignKey(SysterUser, related_name='community',
                                        verbose_name="Admin")
    parent_community = models.ForeignKey('self', blank=True, null=True,
                                         verbose_name="Parent Community")
    website = models.URLField(max_length=255, blank=True,
                              verbose_name="Website")
    facebook = models.URLField(max_length=255, blank=True,
                               verbose_name="Facebook")
    googleplus = models.URLField(max_length=255, blank=True,
                                 verbose_name="Google+")
    twitter = models.URLField(max_length=255, blank=True,
                              verbose_name="Twitter")
    __original_name = None
    __original_community_admin = None

    class Meta:
        permissions = (
            ('add_community_systeruser', 'Add community Systeruser'),
            ('change_community_systeruser', 'Change community Systeruser'),
            ('delete_community_systeruser', 'Delete community Systeruser'),
            ('add_community_news', 'Add community news'),
            ('change_community_news', 'Change community news'),
            ('delete_community_news', 'Delete community news'),
            ('add_community_resource', 'Add community resource'),
            ('change_community_resource', 'Change community resource'),
            ('delete_community_resource', 'Delete community resource'),
            ('add_community_page', 'Add community page'),
            ('change_community_page', 'Change community page'),
            ('delete_community_page', 'Delete community page'),
        )

    def __init__(self, *args, **kwargs):
        super(Community, self).__init__(*args, **kwargs)
        self.__original_name = self.name
        if self.community_admin_id is not None:
            self.__original_community_admin = self.community_admin

    def __unicode__(self):
        return self.name

    @property
    def original_name(self):
        return self.__original_name

    @property
    def original_community_admin(self):
        return self.__original_community_admin

    def save(self, *args, **kwargs):
        super(Community, self).save(*args, **kwargs)
        self.__original_name = self.name
        self.__original_community_admin = self.community_admin

    def get_fields(self):
        """Get model fields of a community object

        :return: list of tuples (fieldname, fieldvalue)
        """
        return [(field.name, getattr(self, field.name)) for field in
                Community._meta.fields]

    def get_absolute_url(self):
        return reverse('community_main_page', args=[self.slug])


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
    title = models.CharField(max_length=255, verbose_name='Title')
    slug = models.SlugField(max_length=150, unique=True, verbose_name='Slug')
    community = models.ForeignKey(Community, verbose_name='Community')
    author = models.ForeignKey(SysterUser, verbose_name='Author')
    date_created = models.DateField(auto_now=False, auto_now_add=True,
                                    verbose_name='Publish date')
    date_modified = models.DateField(auto_now=True, auto_now_add=False,
                                     verbose_name='Last Modified date')
    is_public = models.BooleanField(default=True, verbose_name='Is public')
    tags = models.ManyToManyField(Tag, blank=True, null=True,
                                  verbose_name='Tags')
    content = models.TextField(verbose_name='Content')
    is_monitor = models.BooleanField(default=False,
                                     verbose_name='Is monitored')

    def __unicode__(self):
        return "{0} of {1} Community".format(self.title, self.community.name)

    def get_absolute_url(self):
        """Absoulte URL for News object"""
        return reverse('view_news',
                       kwargs={'community_slug': self.community.slug,
                               'news_slug': self.slug})

    def get_fields(self):
        """Get model fields of a News object

        :return: list of tuples (fieldname, fieldvalue)
        """
        return [(field.name, getattr(self, field.name)) for field in
                News._meta.fields]


class CommunityPage(models.Model):

    """Model to represent community pages"""
    title = models.CharField(max_length=255)
    editable_content = PlaceholderField('editable_content')
    community = models.ForeignKey(Community)
    slug = models.SlugField(max_length=150, unique=True)
    order = models.DecimalField(max_digits=2, decimal_places=0)

    def __unicode__(self):
        return "{0} of {1} Community".format(self.title, self.community.name)

    def get_absolute_url(self):
        return reverse('edit_page', args=[self.community.slug, self.slug])


class Resource(models.Model):

    """Model to represent a Resources section on Community resource area"""
    title = models.CharField(max_length=255, verbose_name='Title')
    slug = models.SlugField(max_length=150, unique=True, verbose_name='Slug')
    community = models.ForeignKey(Community, verbose_name='Community')
    author = models.ForeignKey(SysterUser, verbose_name='Author')
    date_created = models.DateField(auto_now=False, auto_now_add=True,
                                    verbose_name='Publish Date')
    date_modified = models.DateField(auto_now=True, auto_now_add=False,
                                     verbose_name='Last Modified date')
    is_public = models.BooleanField(default=True, verbose_name='Is public')
    tags = models.ManyToManyField(Tag, blank=True, null=True,
                                  verbose_name='Tags')
    resource_type = models.ForeignKey(ResourceType, blank=True, null=True,
                                      verbose_name='Resource Type')
    content = models.TextField(verbose_name='Content')
    is_monitor = models.BooleanField(
        default=False, verbose_name='Is monitored')

    def __unicode__(self):
        return "{0} of {1} Community".format(self.title, self.community.name)

    def get_absolute_url(self):
        """Absoulte URL for Resource object"""
        return reverse('view_resource',
                       kwargs={'community_slug': self.community.slug,
                               'resource_slug': self.slug})

    def get_fields(self):
        """Get model fields of a Resource object

        :return: list of tuples (fieldname, fieldvalue)
        """
        return [(field.name, getattr(self, field.name)) for field in
                Resource._meta.fields]


class NewsComment(models.Model):

    """Model to represent a comment to a News instance"""
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(SysterUser)
    body = models.TextField()
    news = models.ForeignKey(News)
    is_approved = models.BooleanField(default=True, verbose_name='Is approved')

    def __unicode__(self):
        return unicode("%s: %s" % (self.news, self.body))


class ResourceComment(models.Model):

    """Model to represent a comment to a Resource instance"""
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(SysterUser)
    body = models.TextField()
    resource = models.ForeignKey(Resource)
    is_approved = models.BooleanField(default=True, verbose_name='is_approved')

    def __unicode__(self):
        return unicode("%s: %s" % (self.resource, self.body))


class JoinRequest(models.Model):

    """Model to represent a request to join a community by a user"""
    user = models.ForeignKey(SysterUser, related_name='created_by')
    approved_by = models.ForeignKey(
        SysterUser, blank=True, null=True, related_name='approved_by')
    community = models.ForeignKey(Community, verbose_name='Community')
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True,
                                        verbose_name='Request Date')
    is_approved = models.BooleanField(
        default=False, verbose_name='Is approved')

    def __unicode__(self):
        if self.is_approved:
            return unicode("Join Request by {0} - approved".format(self.user))
        else:
            return unicode("Join Request by {0} - not approved".format(self.user))

    class Meta:
        get_latest_by = 'date_created'
