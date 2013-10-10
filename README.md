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
Once the app is added to your `INSTALLED_APPS`, you have defined the necessary settings and have created your `remotes.py` file, a periodic task will be fired every `REMOTE_CHECK_FREQUENCY` (default 30) minutes that will ssh to each of these boxes to assert that it is reachable and that the optionally specified `processes` are actually running on it.

If any boxes are unreachable or are not running the specified processes, a notification email will be sent to `RS_USERS_TO_NOTIFY` with a rollup of what is wrong.

The history of each remote status check is logged in the `remotestatus.StatusHistory` table.


### The Dashboard
The dashboard is available at: `http://localhost:8000/remotestatus/` and shows the status of all defined boxes by the most recent call to check them. You can view each remote host's history by clicking on it's `nickname` and you can change the date via the dropdown.



