from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=128, unique=True)
    text = models.TextField(blank=True)
    # The extra cascade means that if the User is ever deleted, all posts
    # will follow and be deleted as well
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # auto_now_add sets the DateTime when the Post is added
    created_date = models.DateTimeField(auto_now_add=True)
    # auto_now sets the DateTime whenever the Post is saved
    modified_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True)

    @property
    def is_modified_date_significant(self):
        """This function will return a boolean depending on whether or not the
        modified_date is worth showing. This is used to show the modified_date
        if it is atleast one minute more than the created date"""
        return (self.modified_date - self.created_date).seconds > 60
