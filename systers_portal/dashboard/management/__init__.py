from django.db.models.signals import post_syncdb
from django.contrib.auth.models import Group, Permission

from dashboard import models


permissions = [
    "add_tag",
    "change_tag",
    "add_resourcetype",
    "change_resourcetype",
    # djangocms_text_ckeditor permissions
    "add_text",
    "change_text",
    "delete_text",
]


def create_generic_group(sender, **kwargs):
    """Create a user group with generic permissions. Every user that is member
    of any other custom group, should become a member of this group too.

    :param sender: models module that was just installed
    """
    verbosity = kwargs.get("verbosity")
    if verbosity > 0:
        print "Initializing data post_syncdb"
    name = "Generic permissions"
    role, created = Group.objects.get_or_create(name=name)
    if verbosity > 1 and created:
        print "Creating group {0}".format(name)
    for perm in permissions:
        role.permissions.add(Permission.objects.get(codename=perm))
        if verbosity > 1:
            print "Permitting {0} to {1}".format(name, perm)
    role.save()


post_syncdb.connect(create_generic_group, sender=models)
