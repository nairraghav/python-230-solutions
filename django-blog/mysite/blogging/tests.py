from django.test import TestCase
from django.contrib.auth.models import User
from blogging.models import Post, Category
from datetime import datetime, timedelta
from django.db.utils import IntegrityError
from django.utils.timezone import utc


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


class CategoryTestCase(TestCase):

    def test_string_representation(self):
        expected = "A Category"
        c1 = Category(name=expected)
        actual = str(c1)
        self.assertEqual(expected, actual)


class FrontEndTestCase(TestCase):
    """test views provided in the front-end"""
    fixtures = ['blogging_test_fixture.json', ]

    def setUp(self):
        self.now = datetime.utcnow().replace(tzinfo=utc)
        self.timedelta = timedelta(15)
        author = User.objects.get(pk=1)
        for count in range(1, 11):
            post = Post(title="Post %d Title" % count,
                        text="foo",
                        author=author)
            if count < 6:
                # publish the first five posts
                pubdate = self.now - self.timedelta * count
                post.published_date = pubdate
            post.save()

    def test_list_only_published(self):
        resp = self.client.get('/')
        # the content of the rendered response is always a bytestring
        resp_text = resp.content.decode(resp.charset)
        self.assertTrue("Recent Posts" in resp_text)
        for count in range(1, 11):
            title = "Post %d Title" % count
            if count < 6:
                self.assertContains(resp, title, count=1)
            else:
                self.assertNotContains(resp, title)

    def test_details_only_published(self):
        for count in range(1, 11):
            title = "Post %d Title" % count
            post = Post.objects.get(title=title)
            resp = self.client.get('/posts/%d/' % post.pk)
            if count < 6:
                self.assertEqual(resp.status_code, 200)
                self.assertContains(resp, title)
            else:
                self.assertEqual(resp.status_code, 404)
