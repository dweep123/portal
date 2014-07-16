from django.contrib.auth.models import Group, Permission, User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from guardian.shortcuts import assign_perm

from dashboard.models import Community, SysterUser


generic_groups = {"content_contributor": "Content Contributor for {0}",
                  "content_manager": "Content Manager for {0}",
                  "user_content_manager": "User and Content Manager for {0}",
                  "community_admin": "Community Admin for {0}"}

content_contributor_permissions = [
    "add_community_resource",
    "change_community_resource",
    "change_community_page",
    "add_community_news",
    "change_community_news",
]

content_manager_permissions = content_contributor_permissions + [
    "delete_community_resource",
    "add_community_page",
    "delete_community_page",
    "delete_community_news",
    "delete_tag",
    "delete_resourcetype",
]

user_content_manager_permissions = content_manager_permissions + [
    "add_community_systeruser",
    "change_community_systeruser",
    "delete_community_systeruser",
]

community_admin_permissions = user_content_manager_permissions + [
    "change_community",
]

dashboard_group_permissions = {
    "content_contributor": content_contributor_permissions,
    "content_manager": content_manager_permissions,
    "user_content_manager": user_content_manager_permissions,
    "community_admin": community_admin_permissions
}


@receiver(post_save, sender=Community, dispatch_uid="create_groups")
def create_community_groups(sender, instance, created, **kwargs):
    """Create user groups for a particular Community instance and assign
    permissions to each group"""
    if created:
        create_groups(instance.name)
        assign_permissions(instance)
    else:
        if instance.name != instance.original_name:
            delede_groups(instance.original_name)
            create_groups(instance.name)
            assign_permissions(instance)
    grant_access_to_parent_community(instance)


@receiver(post_delete, sender=Community, dispatch_uid="remove_groups")
def remove_community_groups(sender, instance, **kwargs):
    """Remove user groups for this particular Community instance"""
    delede_groups(instance.name)


@receiver(user_signed_up)
def create_syster_user(sender, **kwargs):
    """Keep User and SysterUser synchronized. Create a SystersUser instance on
    receiving a signal about new user signup.
    """
    user = kwargs.get('user')
    if user is not None:
        syster_user = SysterUser(user=user)
        syster_user.save()


def create_groups(community_name):
    """Create groups for a particular Community instance using its name

    :param community_name: string name of community
    """
    for key, group_name in generic_groups.items():
        Group.objects.get_or_create(name=group_name.format(community_name))


def delede_groups(community_name):
    """Delete groups that were created using community name

    :param community_name: string name of community
    """
    for key, group_name in generic_groups.items():
        Group.objects.get(name=group_name.format(community_name)).delete()


def assign_permissions(community):
    """Assign specific permissions for each group

    :param community: Community object
    """
    for key, group_name in generic_groups.items():
        group = Group.objects.get(name=group_name.format(community.name))
        for perm in dashboard_group_permissions[key]:
            if perm.endswith('tag') or perm.endswith('resourcetype'):
                group.permissions.add(Permission.objects.get(codename=perm))
                group.save()
            else:
                assign_perm(perm, group, community)


def grant_access_to_parent_community(community):
    """Make members of parent community "Community Admin" group, also members
    of subcommunity's "Community Admin" group.

    :param community: Community object
    """
    if community.parent_community is not None:
        community_admin_group = Group.objects.get(
            name="Community Admin for {0}".format(
                community.name))
        parent_community_admin_users = User.objects.filter(
            groups__name='Community Admin for {0}'.format(
                community.parent_community.name))
        for user in parent_community_admin_users:
            community_admin_group.user_set.add(user)
