from django.urls import path
from polling.views import list_view, details_view

urlpatterns = [
    path('', list_view, name='poll_index'),
    path('polls/<int:poll_id>/', details_view, name='poll_details'),

]