import urllib
from django.contrib.auth.models import Group
from django.core import mail
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.test import TestCase

from myjobs.models import *
from myjobs.tests.views import TestClient
from myjobs.tests.factories import UserFactory


class UserManagerTests(TestCase):
    user_info = {'password1': 'complicated_password',
                 'email': 'alice@example.com'}

    def test_inactive_user_creation(self):
        new_user, created = User.objects.create_inactive_user(**self.user_info)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(new_user.is_active, False)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(new_user.email, 'alice@example.com')
        self.failUnless(new_user.check_password('complicated_password'))
        self.failUnless(new_user.groups.filter(name='Job Seeker').count() == 1)

    def test_active_user_creation(self):
        new_user = User.objects.create_user(**self.user_info)

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(new_user.is_active, True)
        self.assertEqual(new_user.email, 'alice@example.com')
        self.failUnless(new_user.check_password('complicated_password'))
        self.failUnless(new_user.groups.filter(name='Job Seeker').count() == 1)

    def test_superuser_creation(self):
        new_user = User.objects.create_superuser(
            **{'password': 'complicated_password',
               'email': 'alice@example.com'})
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(new_user.is_superuser, True)
        self.assertEqual(new_user.is_staff, True)
        self.assertEqual(new_user.email, 'alice@example.com')
        self.failUnless(new_user.check_password('complicated_password'))
        self.failUnless(new_user.groups.filter(name='Job Seeker').count() == 1)

    def test_gravatar_url(self):
        """
        Test that email is hashed correctly and returns a 200 response
        """
        user = UserFactory()
        static_gravatar_url = "http://www.gravatar.com/avatar/c160f8cc69a4f0b" \
                              "f2b0362752353d060?s=20&d=mm"
        generated_gravatar_url = user.get_gravatar_url()
        self.assertEqual(static_gravatar_url, generated_gravatar_url)
        status_code = urllib.urlopen(static_gravatar_url).getcode()
        self.assertEqual(status_code, 200)

    def test_not_disabled(self):
        """
        An anonymous user or user with is_disabled set to True should be
        redirected to the home page, while a user with is_active set to False
        should proceed to their destination.
        """
        client = TestClient()
        user = UserFactory()

        quoted_email = urllib.quote(user.email)

        #Anonymous user
        resp = client.get(reverse('view_profile',
                                  args=[user.email]))
        self.assertRedirects(resp, "http://testserver/?next=/%s/profile/"
                             % (quoted_email,))

        # Active user
        client.login_user(user)
        resp = client.get(reverse('view_profile',
                                  args=[user.email]))
        self.assertTrue(resp.status_code, 200)

        #Disabled user
        user.is_disabled = True
        user.save()
        resp = client.get(reverse('view_profile',
                                  args=[user.email]))
        self.assertRedirects(resp, "http://testserver/?next=/%s/profile/"
                             % (quoted_email,))

    def test_is_active(self):
        """
        An anonymous user or user with is_active set to False should be
        redirected to the home page, while a user with is_active set to True
        should proceed to their destination.
        """
        client = TestClient()
        user = UserFactory()
        quoted_email = urllib.quote(user.email)

        #Anonymous user
        resp = client.get(reverse('saved_search_main', args=[user.email]))
        self.assertRedirects(resp, "http://testserver/?next=/%s/saved-search/"
                             % (quoted_email,))

        # Active user
        client.login_user(user)
        resp = client.get(reverse('saved_search_main', args=[user.email]))
        self.assertTrue(resp.status_code, 200)

        # Inactive user
        user.is_active = False
        user.save()
        resp = client.get(reverse('saved_search_main', args=[user.email]))
        self.assertRedirects(resp, "http://testserver/?next=/%s/saved-search/"
                             % (quoted_email,))

    def test_group_status(self):
        """
        Should return True if user.groups contains the group specified and
        False if it does not.
        """
        client = TestClient()
        user = UserFactory()

        user.groups.all().delete()

        for group in Group.objects.all():
            # Makes a list of all group names, excluding the one that the
            # user will be a member of
            names = map(lambda group: group.name,
                        Group.objects.filter(~Q(name=group.name)))

            user.groups.add(group.pk)
            user.save()

            for name in names:
                self.assertFalse(User.objects.is_group_member(user, name))
            self.assertTrue(User.objects.is_group_member(user, group.name))

            user.groups.all().delete()
