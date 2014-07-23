import mock

from django.db.models.signals import post_save, post_delete, m2m_changed
from django.contrib.auth.models import User, Group
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import Http404
from django.test import TestCase, Client, RequestFactory
from allauth.account import signals
from guardian.shortcuts import get_perms
from south.signals import post_migrate

from dashboard.decorators import (membership_required, admin_required,
                                  authorship_required)
from dashboard.forms import UserForm, CommunityForm
from dashboard.management import create_generic_group, permissions
from dashboard.models import (SysterUser, Community, News, Resource, Tag,
                              ResourceType, CommunityPage)
from dashboard.signals import *
from dashboard.views import edit_userprofile


class DashboardModelsTestCase(TestCase):
    def setUp(self):
        self.auth_user = User.objects.create(username='foo', password='foobar')
        self.tag = Tag.objects.create(name='dummy_tag')
        self.resource_type = ResourceType.objects.create(
            name='dummy_resource_type')

    def test_user_and_syster_user(self):
        self.assertQuerysetEqual(SysterUser.objects.all(), [])
        systeruser = SysterUser.objects.create(
            user=self.auth_user,
            blog_url='http://blog_url.com',
            homepage_url='http://homepage_url.com')
        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(len(SysterUser.objects.all()), 1)
        self.assertEqual(unicode(systeruser), self.auth_user.username)
        self.assertEqual(systeruser.blog_url,
                         self.auth_user.systeruser.blog_url)
        self.assertEqual(systeruser.blog_url, 'http://blog_url.com')
        self.assertEqual(systeruser.homepage_url, 'http://homepage_url.com')
        second_user = User.objects.create(username='user2', password='user2')
        second_systeruser = SysterUser.objects.create(user=second_user)  # NOQA
        self.assertEqual(len(User.objects.all()), 2)
        self.assertEqual(len(SysterUser.objects.all()), 2)
        second_user.delete()
        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(len(SysterUser.objects.all()), 1)

    def test_community_model(self):
        self.assertQuerysetEqual(Community.objects.all(), [])
        self.assertQuerysetEqual(SysterUser.objects.all(), [])
        systeruser = SysterUser.objects.create(user=self.auth_user)
        community = Community.objects.create(name='dummy_community',
                                             community_admin=systeruser)
        community.members.add(systeruser)
        second_user = User.objects.create(username='user2', password='user2')
        second_systeruser = SysterUser.objects.create(
            user=second_user)
        community.members.add(second_systeruser)
        community_members = SysterUser.objects.filter(
            member_of_community=community)
        community_admin = SysterUser.objects.get(community=community)
        self.assertEqual(len(Community.objects.all()), 1)
        self.assertEqual(len(community_members), 2)
        self.assertEqual(unicode(community), 'dummy_community')
        self.assertEqual(community.community_admin, systeruser)
        self.assertEqual(community_admin, systeruser)
        self.assertEqual(systeruser in community_members, True)
        self.assertEqual(second_systeruser in community_members, True)

    def test_tag_model(self):
        self.assertEqual(len(Tag.objects.all()), 1)
        tag = Tag.objects.create(name='dummy_tag1')
        self.assertEqual(len(Tag.objects.all()), 2)
        self.assertEqual(unicode(tag), 'dummy_tag1')

    def test_resourcetype_model(self):
        self.assertEqual(len(ResourceType.objects.all()), 1)
        resource = ResourceType.objects.create(name='dummy_resource1')
        self.assertEqual(len(ResourceType.objects.all()), 2)
        self.assertEqual(unicode(resource), 'dummy_resource1')

    def test_news_model(self):
        self.assertQuerysetEqual(News.objects.all(), [])
        self.assertQuerysetEqual(Community.objects.all(), [])
        self.assertQuerysetEqual(SysterUser.objects.all(), [])
        systeruser = SysterUser.objects.create(user=self.auth_user)
        community = Community.objects.create(name='dummy_community',
                                             community_admin=systeruser)
        news_article = News.objects.create(title='dummy_article',
                                           community=community,
                                           author=systeruser,
                                           content='dummy news article')
        news_article.tags.add(self.tag)
        news_article_tags = Tag.objects.filter(news=news_article)
        self.assertEqual(len(Community.objects.all()), 1)
        self.assertEqual(len(SysterUser.objects.all()), 1)
        self.assertEqual(len(News.objects.all()), 1)
        self.assertEqual(unicode(news_article),
                         'dummy_article of dummy_community Community')
        self.assertEqual(news_article.community,
                         community)
        self.assertEqual(news_article.author, systeruser)
        self.assertEqual(news_article.community.community_admin,
                         systeruser)
        self.assertEqual(news_article.author.user, self.auth_user)
        self.assertEqual(news_article_tags[0], self.tag)
        self.assertEqual(news_article.is_public, True)
        self.assertEqual(news_article.community,
                         Community.objects.get(news=news_article))

    def test_resource_model(self):
        self.assertQuerysetEqual(Resource.objects.all(), [])
        self.assertQuerysetEqual(Community.objects.all(), [])
        self.assertQuerysetEqual(SysterUser.objects.all(), [])
        systeruser = SysterUser.objects.create(user=self.auth_user)
        community = Community.objects.create(name='dummy_community',
                                             community_admin=systeruser)
        resource = Resource.objects.create(title='dummy_resource',
                                           community=community,
                                           author=systeruser,
                                           content='dummy resource',
                                           resource_type=self.resource_type)
        resource.tags.add(self.tag)
        resource_tags = Tag.objects.filter(resource=resource)
        self.assertEqual(len(Community.objects.all()), 1)
        self.assertEqual(len(SysterUser.objects.all()), 1)
        self.assertEqual(len(Resource.objects.all()), 1)
        self.assertEqual(unicode(resource),
                         'dummy_resource of dummy_community Community')
        self.assertEqual(resource.community, community)
        self.assertEqual(resource.author, systeruser)
        self.assertEqual(resource.community.community_admin, systeruser)
        self.assertEqual(resource.author.user, self.auth_user)
        self.assertEqual(resource_tags[0], self.tag)
        self.assertEqual(resource.resource_type, self.resource_type)
        self.assertEqual(resource.is_public, True)
        self.assertEqual(resource.community,
                         Community.objects.get(resource=resource))
        resource.is_public = False
        self.assertEqual(resource.is_public, False)

    def test_CommunityPage_model(self):
        self.assertQuerysetEqual(CommunityPage.objects.all(), [])
        self.assertQuerysetEqual(Community.objects.all(), [])
        self.assertQuerysetEqual(SysterUser.objects.all(), [])
        systeruser = SysterUser.objects.create(user=self.auth_user)
        community = Community.objects.create(name='dummy_community',
                                             community_admin=systeruser)
        about_dummy_community = CommunityPage.objects.create(
            title='About',
            community=community,
            slug='about')
        self.assertEqual(len(Community.objects.all()), 1)
        self.assertEqual(len(SysterUser.objects.all()), 1)
        self.assertEqual(len(CommunityPage.objects.all()), 1)
        self.assertEqual(unicode(about_dummy_community),
                         'About of dummy_community Community')
        self.assertEqual(about_dummy_community.community, community)
        about_dummy_community.delete()
        self.assertEqual(len(CommunityPage.objects.all()), 0)

    def test_signal_registry(self):
        """Test if functions were registered as signal receivers"""
        signed_up_registered_funcs = [r[1]() for r in
                                      signals.user_signed_up.receivers]
        post_save_registered_funcs = [r[1]() for r in post_save.receivers]
        post_delete_registered_funcs = [r[1]() for r in post_delete.receivers]
        post_migrate_registered_funcs = [r[1]() for r in
                                         post_migrate.receivers]
        m2m_changed_registered_funcs = [r[1]() for r in m2m_changed.receivers]
        self.assertIn(create_syster_user, signed_up_registered_funcs)
        self.assertIn(create_community_groups, post_save_registered_funcs)
        self.assertIn(remove_community_groups, post_delete_registered_funcs)
        self.assertIn(create_generic_group, post_migrate_registered_funcs)
        self.assertIn(give_basic_access, m2m_changed_registered_funcs)

    def test_create_syster_user(self):
        """Test the creation of SysterUser object on user signup"""
        self.assertQuerysetEqual(SysterUser.objects.all(), [])
        request = {'user': self.auth_user}
        create_syster_user(self.test_create_syster_user, **request)
        users = User.objects.all()
        systerusers = SysterUser.objects.all()
        self.assertEqual(len(systerusers), len(users))
        self.assertEqual(len(users), 1)
        self.assertEqual(systerusers[0].user, users[0])

    def test_give_basic_access(self):
        """Test giving basic access to users"""
        self.assertEqual(list(self.auth_user.groups.all()), [])
        self.assertFalse(self.auth_user.is_staff)
        group = Group.objects.create(name="Foo group")
        self.auth_user.groups.add(group)
        self.auth_user.save()
        self.assertIn(group, self.auth_user.groups.all())
        self.assertTrue(self.auth_user.is_staff)
        self.auth_user.groups.remove(group)
        self.auth_user.save()
        self.assertEqual(list(self.auth_user.groups.all()), [])
        self.assertFalse(self.auth_user.is_staff)

    def test_create_community_groups(self):
        """Test creation of community specific groups"""
        systeruser = SysterUser.objects.create(user=self.auth_user)
        name = 'FooBar'
        for key, group_name in generic_groups.items():
            self.assertFalse(Group.objects.filter(
                name=group_name.format(name)).exists())
        community = Community.objects.create(name=name,
                                             community_admin=systeruser)
        for key, group_name in generic_groups.items():
            self.assertTrue(Group.objects.filter(
                name=group_name.format(community.name)).exists())
        self.assertIn(Group.objects.get(
            name=generic_groups["community_admin"].format(name)),
            systeruser.user.groups.all())
        community.name = "BarFoo"
        systeruser2 = SysterUser.objects.create(
            user=User.objects.create(username='bar', password='foobar'))
        community.community_admin = systeruser2
        community.save()
        self.assertNotIn(Group.objects.get(
            name=generic_groups["community_admin"].format(community.name)),
            systeruser.user.groups.all())
        self.assertIn(Group.objects.get(
            name=generic_groups["community_admin"].format(community.name)),
            systeruser2.user.groups.all())
        for key, group_name in generic_groups.items():
            self.assertFalse(Group.objects.filter(
                name=group_name.format(name)).exists())
            self.assertTrue(Group.objects.filter(
                name=group_name.format(community.name)).exists())

    def test_remove_community_groups(self):
        """Test removal of community specific groups"""
        systeruser = SysterUser.objects.create(user=self.auth_user)
        community = Community.objects.create(name="Foo",
                                             community_admin=systeruser)
        community.delete()
        for key, group_name in generic_groups.items():
            self.assertFalse(Group.objects.filter(
                name=group_name.format(community.name)).exists())

    def test_create_groups(self):
        name = "baz"
        for key, group_name in generic_groups.items():
            self.assertFalse(Group.objects.filter(
                name=group_name.format(name)).exists())
        create_groups(name)
        for key, group_name in generic_groups.items():
            self.assertTrue(Group.objects.filter(
                name=group_name.format(name)).exists())

    def test_delete_groups(self):
        name = "bar"
        for key, group_name in generic_groups.items():
            Group.objects.create(name=group_name.format(name))
        delede_groups(name)
        for key, group_name in generic_groups.items():
            self.assertFalse(Group.objects.filter(
                name=group_name.format(name)).exists())

    def test_assign_permissions(self):
        name = "Foo"
        systeruser = SysterUser.objects.create(user=self.auth_user)
        community = Community.objects.create(name=name,
                                             community_admin=systeruser)
        assign_permissions(community)
        for key, value in dashboard_group_permissions.items():
            group = Group.objects.get(name=generic_groups[key].format(name))
            group_permissions = [p.codename for p in
                                 list(group.permissions.all())]
            group_permissions += get_perms(group, community)
            self.assertItemsEqual(group_permissions, value)

    def test_grant_access_to_parent_community(self):
        systeruser1 = SysterUser.objects.create(user=self.auth_user)
        auth_user2 = User.objects.create(username='bar', password='foobar')
        systeruser2 = SysterUser.objects.create(user=auth_user2)
        community_a = Community.objects.create(name="A", slug='a',
                                               community_admin=systeruser1)
        community_b = Community.objects.create(name="B", slug='b',
                                               community_admin=systeruser2)
        group_a = Group.objects.get(name="Community Admin for A")
        group_a.user_set.add(self.auth_user)
        community_b.parent_community = community_a
        community_b.save()
        group_b = Group.objects.get(name="Community Admin for B")
        user_groups = self.auth_user.groups.all()
        self.assertIn(group_a, user_groups)
        self.assertIn(group_b, user_groups)

    def test_create_generic_group(self):
        self.assertTrue(Group.objects.filter(
            name="Generic permissions").exists())
        group = Group.objects.get(name="Generic permissions")
        group_permissions = [p.codename for p in
                             list(group.permissions.all())]
        self.assertItemsEqual(group_permissions, permissions)

    def test_join_leave_group(self):
        systeruser = SysterUser.objects.create(user=self.auth_user)
        community = Community.objects.create(name="Foo",
                                             community_admin=systeruser)
        self.assertRaises(Http404, join_group, systeruser, "No such group")
        self.assertRaises(Http404, leave_group, systeruser, "No such group")
        join_group(systeruser,
                   generic_groups["content_manager"].format(community.name))
        self.assertIn(Group.objects.get(
            name=generic_groups["content_manager"].format(community.name)),
            systeruser.user.groups.all())
        leave_group(systeruser,
                    generic_groups["content_manager"].format(community.name))
        self.assertNotIn(Group.objects.get(
            name=generic_groups["content_manager"].format(community.name)),
            systeruser.user.groups.all())


class DashboardDecoratorsTestCase(TestCase):
    def setUp(self):
        self.auth_user_foo = User.objects.create_user(username="foo",
                                                      password="foobar")
        self.user_foo = SysterUser(user=self.auth_user_foo)
        self.user_foo.save()
        self.auth_user_bar = User.objects.create_user(username="bar",
                                                      password="foobar")
        self.user_bar = SysterUser(user=self.auth_user_bar)
        self.user_bar.save()
        self.community = Community(community_admin=self.user_foo)
        self.community.save()
        self.community.members.add(self.user_foo)
        self.community.save()
        self.resource = Resource(community=self.community,
                                 author=self.user_foo)
        self.resource.save()

    def test_decorators(self):
        request = mock.MagicMock()
        view = mock.MagicMock(return_value='foo response')

        test_objects = [self.community, self.resource, ]
        mockup_tests = [
            {"user": self.auth_user_foo, "success": True},
            {"user": self.auth_user_bar, "success": False},
        ]
        tests = []
        for obj in test_objects:
            for mockup_test in mockup_tests:
                tests.append(mockup_test)
                tests[-1]["model"] = type(obj)
                tests[-1]["object"] = obj
        decorators = [membership_required, admin_required, authorship_required]
        for decorator in decorators:
            for test in tests:
                request.user = test["user"]
                request_kwargs = {"id": test["object"].id}
                decorated = decorator(test["model"], "id__exact", "id")
                wrapped = decorated(view)

                if test["success"]:
                    response = wrapped(request, **request_kwargs)
                    self.assertEqual(response, view.return_value)
                else:
                    self.assertRaises(PermissionDenied, wrapped, request,
                                      **request_kwargs)


class DashboardFormsTestCase(TestCase):

    def setUp(self):
        auth_user = User.objects.create_user(username="foo", password="foobar")
        self.user = SysterUser(user=auth_user)
        self.user.save()
        self.community = Community(name='bar', community_admin=self.user)
        self.community.save()

    def test_userform(self):
        """Test userform"""
        user = User.objects.create_user(
            'john',
            'lennon@thebeatles.com',
            'johnpassword')
        systeruser = SysterUser.objects.create(user=user)
        form_data = {
            'first_name': 'FOO',
            'last_name': 'BAR',
            'country': 'FO',
            "blog_url": "http://anitaborg.org/",
            "homepage_url": "http://anitaborg.org/",
        }
        form = UserForm(data=form_data, instance=user)
        self.assert_(form.is_valid())
        self.assertEqual(form.instance.first_name, 'FOO')
        form.save()
        self.assertEqual(systeruser.blog_url, "http://anitaborg.org/")
        self.assertEqual(systeruser.homepage_url, "http://anitaborg.org/")
        self.assertEqual(
            User.objects.get(id=form.instance.id).first_name,
            'FOO'
        )
        form_data = [
            {},
            {'first_name': 'foo'},
            {'last_name': 'bar'},
            {'country': 'FO'},
            {"blog_url": "http://anitaborg.org/"},
            {"homepage_url": "http://anitaborg.org/"},
            {"blog_url": "anitaborg"},
            {"homepage_url": "foorbaranitaborg"},
        ]
        result = [True] * 6 + [False] * 2
        for i, data in enumerate(form_data):
            form = UserForm(data=data, instance=user)
            self.assertEqual(form.is_valid(), result[i])

    def test_community_form(self):
        form_data = [
            {},
            {'name': 'foo'},
            {'community_admin': self.user.id},
            {'slug': 'foo'},
            {'email': 'invalid_email'},
            {'website': 'just website'},
            {'name': 'foo', 'community_admin': self.user.id, 'slug': 'foo'},
            {'name': 'foo',
             'slug': 'foo',
             'community_admin': self.user.id,
             'parent_community': self.community.id},
            {'name': 'foo',
             'slug': 'foo',
             'email': 'foo@mail.org',
             'mailing_list': 'foo@mailing.org',
             'resource_area': 'http://foo.com/foo',
             'community_admin': self.user.id,
             'parent_community': self.community.id,
             'website': 'http://foo.com',
             'facebook': 'http://foo.com',
             'googleplus': 'http://foo.com',
             'twitter': 'http://foo.com'},
        ]
        result = [False] * 6 + [True] * 3
        for i, data in enumerate(form_data):
            form = CommunityForm(data=data)
            self.assertEqual(form.is_valid(), result[i])


class DashboardViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        auth_user = User.objects.create_user(username="foo", password="foobar")
        self.user = SysterUser(user=auth_user)
        self.user.save()
        self.community = Community(name='bar',
                                   community_admin=self.user,
                                   slug="bar-1")
        self.community.save()

    def _test_response_status(self, method, url, status_code, **kwargs):
        """Helper function to test if a request returns expected status code

        :param method: string name of the method to be called with test client
                       object, e.g. "get", "post", "put"
        :param url: string URL used in request
        :param status_code: int expected status code of the response
        :returns: HttpResponse object
        """
        response = getattr(self.client, method)(url, kwargs)
        self.assertEqual(response.status_code, status_code)
        return response

    def test_view_user_profile(self):
        """Test User Profile view """
        nonexistent_url = reverse('view_userprofile',
                                  kwargs={'username': "non-existent"})
        self._test_response_status('get', nonexistent_url, 404)
        url = reverse('view_userprofile',
                      kwargs={'username': self.user.user.username})
        self._test_response_status('get', url, 200)

    def test_edituserprofile(self):
        """Test the edit_userprofile function"""
        user = User.objects.create_user(
            'john',
            'lennon@thebeatles.com',
            'johnpassword')
        systeruser = SysterUser.objects.create(
            user=user,
            blog_url="http://anitaborg.org/",
            homepage_url="http://anitaborg.org/")
        self.assertEqual(systeruser.user.first_name, '')
        self.assertEqual(systeruser.user.last_name, '')
        self.assertEqual(systeruser.blog_url, "http://anitaborg.org/")
        self.assertEqual(unicode(systeruser), user.username)
        factory = RequestFactory()
        form_data = {
            'first_name': 'ullu',
            'last_name': 'bar',
            "blog_url": "http://systers.org/",
            "homepage_url": "http://borg.org/",
        }
        request = factory.post(
            reverse('edit_userprofile', args=(systeruser.user.username,)),
            form_data)
        request.user = user
        edit_userprofile(request, user.username)
        self.assertEqual(systeruser.user.first_name, "ullu")
        self.assertEqual(systeruser.user.last_name, "bar")
        self.assertEqual(systeruser.blog_url, "http://systers.org/")
        self.assertNotEqual(systeruser.homepage_url, "http://anitaborg.org/")
        self.assertEqual(unicode(systeruser), "ullu bar")

    def test_view_community_profile(self):
        """Test community profile view """
        nonexistent_url = reverse('view_community_profile',
                                  kwargs={'community_slug': "non-existent"})
        self._test_response_status('get', nonexistent_url, 404)
        url = reverse('view_community_profile',
                      kwargs={'community_slug': self.community.slug})
        self._test_response_status('get', url, 200)
