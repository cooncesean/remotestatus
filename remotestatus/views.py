from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404

from remotestatus.models import CallRound, StatusHistory, RemoteBoxModel


@staff_member_required
def remote_box_detail(request, remote_box_id):
    remote_box = get_object_or_404(RemoteBoxModel, id=remote_box_id)
    return render(request, 'remotestatus/remote_box_detail.html', {
        'remote_box': remote_box,
        'status_histories': StatusHistory.objects.filter(remote_box=remote_box).order_by('-id')
    })

@staff_member_required
def dashboard(request):
    " Show the most recent status update. "
    call_round = CallRound.objects.latest('id')
    call_rounds = CallRound.objects.all().order_by('-id')
    return render(request, 'remotestatus/dashboard.html', {
        'call_round': call_round,
        'call_rounds': call_rounds,
        'status_histories': StatusHistory.objects.filter(call_round=call_round)
    })
