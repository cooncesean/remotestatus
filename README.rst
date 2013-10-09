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
