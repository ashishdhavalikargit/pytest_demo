import paramiko
import json
import logging
import warnings
from os.path import basename


# Temporary solution until paramiko release 2.4.3
warnings.filterwarnings(action='ignore', module='.*paramiko.*')

logger = logging.getLogger(__name__)


class SSHClient(object):

    def __init__(self, host, username, password=None, cloud=None, private_key=None):
        """
        Initializes the SSH Client
        Parameters:
                host: Host IP address
                username: username to connect with the host
                password: Password to connect with the host
                cloud: instance cloud type by default is None Ex: aws, azure,
                private_key: private key to connect with SSH along the path
        """
        logger.info("Initializing SSH client ...")
        self.host = host
        self.username = username
        self.password = password
        self.cloud = cloud
        self.private_key = private_key
        self.sessions = {}
        self.platform = None
        logger.info(f"Username and password for instance: {self.username}:{self.password}")
        if self.private_key:
            self.use_key = True
        else:
            self.use_key = False

    def connect(self):
        """
        Connect to the SSH for the client, and save session.
        :return:
        """
        logger.info(f"host ip is : {self.host}")
        logger.info(f"Private ksy is : {self.private_key}")
        if self.sessions.get(self.host):
            self.disconnect(self.host)

        try:
            ssh = paramiko.SSHClient()
            # ssh.set_keepalive(60)
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            if not self.use_key:
                ssh.connect(self.host, username=self.username, password=self.password)
                self.sessions[self.host] = ssh
            elif self.use_key:
                ssh.connect(self.host, username=self.username, key_filename=self.private_key)
                self.sessions[self.host] = ssh
            else:
                logger.info('Not connected to SSH.')
        except Exception as e:
            logger.exception(f'SSH connection failed: {e}')

    def is_connected(self):
        transport = self.sessions[self.host].get_transport() if self.sessions[self.host] else None
        return transport and transport.is_active()

    def disconnect(self, host):
        self.sessions[host].close()

    def execute(self, command, fmt='json', debug=False):
        """
        Execute sh command over SSH connection/session.
        Parameters:
                command: sh command to execute.
                fmt (str): format the output
                debug (bool):
        Returns: STDOUT as a string.
        """
        try:
            self.is_connected()
            session = self.sessions[self.host]
        except:
            logger.info(f"Retrying again, SSH connection failed on {self.host}")
            self.connect()
            session = self.sessions[self.host]

        # session.set_combine_stderr(True)
        stdin, stdout, stderr = session.exec_command(command)
        output = stdout.read() + stderr.read()

        if debug:
            logger.info("Command: {0}".format(command))
            logger.info("Output: {0}".format(output))

        if fmt == 'raw':
            return output.decode('utf-8')
        elif fmt == 'json':
            return json.loads(output.decode('utf-8'))
        else:
            return output.decode('utf-8')

    def execute_without_output(self, command):
        """
        Execute sh command over SSH connection/session.
        Parameters:
            command: sh command to execute.
        Returns: STDOUT as a string.
        """
        try:
            self.is_connected()
            session = self.sessions[self.host]
        except:
            logger.info(f"Retrying again, SSH connection failed on {self.host}")
            self.connect()
            session = self.sessions[self.host]

        session.exec_command(command)

    def execute_long_running(self, command, fmt='json'):
        """
        Execute long running command and wait untill it finishes.
        Parameters:
            command: sh command to execute
            fmt: formats the output
        Returns: None
        """
        try:
            self.is_connected()
            session = self.sessions[self.host]
        except:
            logger.info(f"Retrying again, SSH connection failed on {self.host}")
            self.connect()
            session = self.sessions[self.host]

        stdin, stdout, stderr = session.exec_command(command)
        while not stdout.channel.exit_status_ready():
            # Print data when available
            if stdout.channel.recv_ready():
                alldata = stdout.channel.recv(1024)
                prevdata = b"1"
                while prevdata:
                    prevdata = stdout.channel.recv(1024)
                    alldata += prevdata

                logger.info(str(alldata))

    def execute_sudo(self, path="/", command=None, debug=False):
        """
        Executes sh command with SUDO/ROOT permissions over SSH connection/session.
        Parameters:
                path: Which folder to cd to.
                command: sh command to execute.
                debug (bool): prints output if True
        Returns: STDOUT as a string.
        """

        try:
            self.is_connected()
            session = self.sessions[self.host]
        except:
            logger.info(f"Retrying again, SSH connection failed on {self.host}")
            self.connect()
            session = self.sessions[self.host]

        logger.info(f"command to be executed: {command}")
        logger.info(f"Path from which command to be executed: {path}")
        stdin, stdout, stderr = session.exec_command('cd {0}; sudo -S {1}'.format(path, command), get_pty=True)
        stdin.write('{}\n'.format(self.password))
        stdin.flush()

        output = stdout.read() + stderr.read()

        if debug:
            logger.info("Command: {0}".format(command))
            logger.info("Output: {0}".format(output))

        try:
            return json.loads(output.decode('utf-8'))
        except:
            return output.decode('utf-8')

    def create_directory(self, dir_name, fmt='raw'):
        """
        Creates directory in a given path.
        Parameters:
                dir_name: Name of the directory
                fmt: formats output
        Returns: None
        """
        try:
            self.is_connected()
        except:
            logger.info(f"Retrying again, SSH connection failed on {self.host}")
            self.connect()
        command = 'mkdir -p {}'.format(dir_name)
        self.execute(command, fmt=fmt)

    def create_directory_sudo(self, dir_name):
        """
        Creates directory in a given path.
        Parameters:
                dir_name: new directory name
        Returns: None
        """
        try:
            self.is_connected()
        except:
            logger.info(f"Retrying again, SSH connection failed on {self.host}")
            self.connect()
        command = 'mkdir -p {}'.format(dir_name)
        self.execute_sudo("/", command, debug=True)