from django.conf import settings

from remotestatus.remote import remote_manager
from remotestatus.conf import REMOTE_CHECK_FREQUENCY, STATUS_DOWN, STATUS_UP


@periodic_task(seconds=REMOTE_CHECK_FREQUENCY)
def monitor_remote_status():
    """
    Iterate over each RemoteBox in the registry and:
        1. Check its status and the status of its optional procs.
        2. Save the status of each in the data store.
    """
    for remote_box in remote_manager.registry:
        # Get status of the box
        statuses = remote_box.check_remote_status()

        # If down contact necessary users
        if statuses[0] == STATUS_DOWN:
            remote_box.notify_user(settings.RS_NOTIFY_USERS)

        # Update the datastore with the status of the box and is procs
        remote_box.update_data()
