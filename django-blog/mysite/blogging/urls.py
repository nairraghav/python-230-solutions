from django.urls import path
from blogging.views import details_view, list_view


urlpatterns = [
    path('', list_view, name="post_index"),
    path('posts/<int:post_id>/', details_view, name="post_details"),
]
