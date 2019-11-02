from django.test import TestCase
from django.contrib.auth.models import User
from blogging.models import Post
from datetime import datetime, timedelta
from django.db.utils import IntegrityError


class PostTestCase(TestCase):
    fixtures = ['blogging_test_fixture.json', ]

    def setUp(self):
        self.user = User.objects.get(pk=1)

    def test_string_representation(self):
        expected = "This is a title"
        p = Post(title=expected)
        actual = str(p)
        self.assertEqual(expected, actual)

    def test_post_has_default_empty_text(self):
        p = Post(title='some text')
        self.assertEqual(p.text, '')

    def test_cannot_save_post_with_null_author(self):
        p = Post(title='some text')
        with self.assertRaises(IntegrityError):
            p.save()

    def test_default_post_has_null_publish_date(self):
        p = Post(title='some text')
        self.assertIsNone(p.published_date)

    def test_default_post_has_no_significant_modified_date(self):
        a = User(username='user', email='email@email.com')
        a.save()
        p = Post(title='some text', author=a)
        p.save()
        self.assertFalse(p.is_modified_date_significant)
        a.delete()
        p.delete()

    def test_significant_modified_date_true(self):
        a = User(username='user', email='email@email.com')
        a.save()
        p = Post(title='some text', author=a)
        p.save()
        p.modified_date = datetime.now() + timedelta(minutes=1)

        # just to make sure we are not naive timezone
        p.created_date = p.created_date.replace(tzinfo=None)
        p.modified_date = p.modified_date.replace(tzinfo=None)
        self.assertFalse(p.is_modified_date_significant)
        a.delete()
        p.delete()



