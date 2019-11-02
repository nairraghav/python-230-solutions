from django.urls import path
from blogging.views import list_view, details_view

urlpatterns = [
    path('', list_view, name='post_index'),
    path('posts/<int:poll_id>/', details_view, name='post_details'),

]