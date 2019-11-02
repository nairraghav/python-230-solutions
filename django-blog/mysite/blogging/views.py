from django.shortcuts import render
from django.http import Http404
from blogging.models import Post


def list_view(request):
    context = {'posts': Post.objects.all()}
    return render(request, 'blogging/list.html', context)


def details_view(request, poll_id):
    try:
        post = Post.objects.get(pk=poll_id)
    except Post.DoesNotExist:
        raise Http404

    # we want to return this view in both POST and GET
    context = {'post': post}
    return render(request, 'blogging/details.html', context)
