"""
Discover, parse and initialize a RemoteManager
using the configuration specified by the Django project.
"""
from django.conf import settings
from django.utils.importlib import import_module

from remotemonitor.remote import remote_manager, RemoteBox


def autodiscover():
    """
    Iterate over each app, look for any remote.py configuration
    files and.
    """
    for app in settings.INSTALLED_APPS:

        # Attempt to import the app's `moderators` module
        try:
            remote_config_file = import_module('%s.remotes' % app)
            inspected_elements = inspect.getmembers(mod)
            REMOTES = [i for i in inspected_elements if i[0] == 'REMOTES'][0]

            for configuration in REMOTES:
                remote_box = RemoteBox(
                    **configuration
                )
                remote_manager.register(remote_box)
        except ImportError:
            pass

autodiscover()
