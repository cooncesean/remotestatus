from celery.decorators import periodic_task
from celery.task.schedules import crontab

from django.conf import settings
from django.utils.timezone import now

from remotestatus.conf import REMOTE_CHECK_FREQUENCY
from remotestatus.models import CallRound
from remotestatus.remote import remote_manager


@periodic_task(run_every=crontab(minute="*/%d" % REMOTE_CHECK_FREQUENCY))
def monitor_remote_status():
    """
    Iterate over each RemoteBox in the registry and:
        1. Check its status and the status of its optional procs.
        2. Save the status of each in the data store.
    """
    # Incr the `call_round` for this 'round' of remote calls
    call_round = CallRound.objects.create(date_checked=now())

    for remote_box in remote_manager.registry.values():
        # Get status of the box
        status = remote_box.check_remote_status()

        # If status is `down` contact necessary users
        if status[0] == False:
            remote_box.notify_user(settings.RS_NOTIFY_USERS)

        # Update the datastore with the status of the box
        remote_box.save_status_history(call_round, status)
