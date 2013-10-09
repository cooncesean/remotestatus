from paramiko import SSHClient

from django.settings import conf


class RemoteManager(object):
    """
    Responsible for parsing the remote boxes config file and
    instantiating the appropriate `RemoteBox` objects for each
    line in the config.
    """
    def __init__(self):
        self.registry = set()

    def register_remote_box(self, remote_box):
        self.registry.add(remote_box)

remote_manager = RemoteManager()

class RemoteBox(object):
    """
    An instance of remote connection, used to make calls to remote boxes
    to check their status and the status of any optional processes
    we expect them to be running.

    Assumes we're working with a PROXY host.
    """
    def __init__(self, nickname, description, remote_username,
        remote_password,
        remote_port, forwarded_port, processes=[]):
        self._client = None
        self.nickname = nickname
        self.description = description
        self.remote_username = remote_username
        self.remote_password = remote_password
        self.remote_port = remote_port
        self.remote_username = remote_username
        self.forwarded_port = forwarded_port
        self.processes = processes

    def get_client(self):
        " Return an instance of a connected and active `paramiko.SSHClient`. "
        # Use existing connection if active
        if self._client:
            return self._client

        # Create the client and connect to proxy server
        client = SSHClient()
        client.load_host_keys(hosts_file)
        client.connect(
            settings.PROXY_HOSTNAME,
            port=settings.PROXY_PORT,
            username=settings.PROXY_USERNAME,
            key_filename=key_filename
        )

        # Get the transport and find create a `direct-tcpip` channel
        transport = client.get_transport()
        dest_addr = ('0.0.0.0', dest_port)
        src_addr = ('127.0.0.1', local_port)
        channel = transport.open_channel("direct-tcpip", dest_addr, src_addr)

        self._client = SSHClient()
        target_client.load_host_keys(hosts_file)
        target_client.connect('localhost', port=local_port, username=dest_username, password=dest_password, sock=channel)
        return target_client

        # command = 'ps aux | grep %s' % cmd
        # # print 'command', command
        # x, stdout, e = target_client.exec_command(command)
        # print stdout.readlines()

    def check_remote_status(self):
        """
        Make a call to check the status of a box and to optionally
        check the status of any processes specified in the config
        for the particular box.

        It returns a tuple of status':
            (True/False, [{'proc1': True, 'proc2': False, etc...}])
            (Box (Up/Down), Process Statuses: (List of dictionaries [{'proc1': Up/Down}, etc...])
        """

    def notify_user(self, email_addresses):
        " Notify the necessary users when a box is not responsive. "

    def update_data(self):
        " Update the StatusHistory table with the table's findings. "
