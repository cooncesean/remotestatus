from django.conf import settings

STATUS_DOWN = 'down'
STATUS_UP = 'up'

# Frequency with which checks will be made to the remote boxes (default is 10 min.)
REMOTE_CHECK_FREQUENCY = getattr(settings, 'RS_REMOTE_CHECK_FREQUENCY', 10 * 60 * 60)
DEFAULT_KEY_FILE = getattr(settings, 'RS_KEY_FILE', None)
DEFAULT_KNOWN_HOSTS_FILE = getattr(settings, 'RS_KNOWN_HOSTS_FILE', None)

