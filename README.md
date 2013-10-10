# What Is This Package
`remotestatus` is a reusable Django app that checks the status (and the status of optional processes) of remote hosts and presents that status in an easy to use dashboard. It also notifies administrators in the case that a specific remote is unreachable or that a specified process is not running.

# Installation And Configuration
This package can be installed via pip:
```
> pip install remotestatus
```

### Settings

After the package has been installed, you will want to add it to your project's `INSTALLED_APPS`.

**your-project/settings.py:**
```python
INSTALLED_APPS = [
    ....
    'remotestatus',
    ....
]
```

You will also want to add a few new settings to configure the app. The app currently assumes your remote hosts are each behind a NAT router but have an ssh tunnel from each remote to a proxy host. This proxy information should be defined in your settings file.

    There should eventually be support for non-tunneled cases as well as different proxy information per remote host.

**your-project/settings.py:**
```python
RS_USERS_TO_NOTIFY = ['some_admin@email.com', ...]          # List of users to notify in case of an outtage
RS_KEY_FILE = 'path/to/ssh/key/file'                        # Path to the proxy's private key
RS_KNOWN_HOSTS_FILE = 'path/to/projects/known_hosts'        # Path to the proxy's known_hosts
RS_PROXY_HOSTNAME = 'proxy.hostname.com'                    # Proxy hostname
RS_PROXY_USERNAME = 'proxy-user'                            # Proxy username
RS_PROXY_PORT = 22                                          # Proxy SSH port
REMOTE_CHECK_FREQUENCY = 30                                 # Optional minutes you wish to check the remote boxes
```

### Urls
Add the app to your project's `urls.py` file.

**your-project/urls.py:**
```python

urlpatterns = patterns('',
    ...
    url(r'^remotestatus/', include('remotestatus.urls')),
    ...
)
```

### Remotes.py
Now its time to configure the remote hosts you want to have the app check the status of. In any of your project's installed apps, create a new `remotes.py` file. This file will then define the list of remote hosts you wish to check the status of.

**your-project/your-app/remotes.py:**
```python
REMOTES = [
    {
        'nickname': 'Video Capture Box',
        'description': 'This host is responsible for capturing videos.',
        'remote_username': 'remote_user',
        'remote_password': 'remote_pass',
        'remote_port': 8001,
        'forwarded_port': 1001,
        'processes': [
            'python manage.py capture_videos.py'
        ]
    },
    {
        'nickname': 'Video Upload Box',
        'description': 'This box is responsible for uploading videos.',
        'remote_username': 'remote_user',
        'remote_password': 'remote_pass',
        'remote_port': 8002,
        'forwarded_port': 1002,
        'processes': [
            'python manage.py upload_videos.py',
            'ssh'
        ]
    }
]
```

### SyncDB
You will now have to run `python manage.py syncdb` to add the `remotestatus` tables to your database. The status history for each of your boxes will be stored in the db.

# How Does It Work
Once the app is added to your `INSTALLED_APPS` and you have defined the necessary settings


### Autodiscover
3. Will use autodiscover to find all apps wishing to contribute with a `remote.py` file


### Tasks
4. Will set run a task every 10 minutes to check the status of boxes

### The Dashboard
The dashboard is available at:













Checking Status Of Recording Devices:

1. One page summary of all distributed recording devices.
Name    Location    Remote Port     Virtual Port    Status          Running Both Processes
                                            (reachable/unreachable)        (yes/no)

2. Means we need a mapping (either in DB or in a config file) for each box

3. Script to log into each box using the settings specified and grep to see if that box
   is running the scripts it should be.

4. Save the output of that data for each box in redis.

5. View/url/template to render the output.

6. Notifications (via sms?) to be sent to administrators if any of the boxes is either unreachable
   or is not running the scripts it should be.





Usage:
1. Add `remotestatus` to the list of your installed apps.
2. Create a config file in any app with the remote boxes you wish to check the status of.
CHECK_FREQUENCY = 10 * 60 * 60 # Runs every 10 minutes
SSH_TUNNELING = True

{
    "proxy_hostname": "some.proxy-hostname.com",        # Typically the same for all proxy hosts
    "proxy_username": "proxy-username"                  # Typically the same for all proxy hosts
    "remote_username": "stomp2",                        # The username for the remote box you wish to connect to
    "remote_password": "jordan23",                      # The password for the remote box
    "port": 8001,                                       # The tunnelled port
    "local_port": 1001,                                 # The local port mapping
},
....
3. Will use autodiscover to find all apps wishing to contribute with a `remote.py` file
4. Will set run a task every 10 minutes to check the status of boxes
