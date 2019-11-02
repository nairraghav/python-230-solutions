from django.shortcuts import render
from django.http import Http404
from polling.models import Poll


def list_view(request):
    context = {'polls': Poll.objects.all()}
    return render(request, 'polling/list.html', context)


def details_view(request, poll_id):
    try:
        poll = Poll.objects.get(pk=poll_id)
    except Poll.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        if request.POST.get("vote") == "Yes":
            poll.score += 1
        else:
            poll.score -= 1
        poll.save()

    # we want to return this view in both POST and GET
    context = {'poll': poll}
    return render(request, 'polling/details.html', context)
