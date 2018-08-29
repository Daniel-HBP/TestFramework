# -*- coding: utf-8 -*-
__author__ = 'daniel hong'
from ToolAgent.BaseLib.base_log_lib import *
import paramiko
import re


class ShellClient(object):
    def __init__(self, remote_ip, username, user_password=None, root_password=None, key_auth_file=None, key_auth_password=None, prompt=None, ssh_port=22):
        self._ssh_client = None
        self._sftp_client = None
        self._current_shell = None
        self._ssh_port = ssh_port
        self._remote_ip = remote_ip
        self._user = username
        self._password = user_password
        self._root_password = root_password
        self._default_prompt = ["$", ">"]
        if prompt is None:
            self._current_prompt = self._default_prompt
        else:
            self._current_prompt = prompt
        self._root_prompt = "#"
        self._key_auth_file = key_auth_file
        self._key_auth_password = key_auth_password
        self._auth_key = None
        self.__sudo_flg = True
        self._ssh_log = os.path.join(g_agent_log_path, "ssh.log")
        self._login()

    def _login(self):
        if self._user == 'root':
            self._current_prompt = self._root_prompt
        self._ssh_client = paramiko.SSHClient()
        paramiko.util.log_to_file(self._ssh_log)
        try:
            if self._key_auth_file is None:
                self._ssh_client.load_system_host_keys()
                self._ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
                self._ssh_client.connect(self._remote_ip, username=self._user, password=self._password,
                                         port=self._ssh_port)
            else:
                self._auth_key = paramiko.RSAKey.from_private_key(self._key_auth_file, self._key_auth_password)
                self._ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
                self._ssh_client.connect(self._remote_ip, username=self._user, password=self._password,
                                         pkey=self._auth_key, port=self._ssh_port)
        except Exception, e:
            agent_log.error("connect %s failed" % self._remote_ip)
            agent_log.error(e.message)
            raise e
        try:
            self._ssh_client.exec_command("TMOUT=0")
            self._current_shell = self._ssh_client.invoke_shell(width=1024, height=100)
            self._current_shell.settimeout(1800)
        except Exception, e:
            agent_log.error("create shell client failed")
            agent_log.error(e)
            raise e

    def __check_sudo_cmd(self):
        cmd_result = self.linux_command('echo "%s"|sudo ls -l' % self._root_password)


    def _sftp_login(self):
        try:
            if self._sftp_client is not None:
                self._sftp_client.close()
                self._sftp_client = None
            scp = paramiko.Transport((self._remote_ip, self._ssh_port))
        except Exception, e:
            agent_log.error("create scp channel failed")
            agent_log.error(e)
            raise e
        try:
            if self._key_auth_file is None:
                scp.connect(username=self._user, password=self._password)
            else:
                self._auth_key = paramiko.RSAKey.from_private_key(self._key_auth_file, self._key_auth_password)
                scp.connect(username=self._user, password=self._password, pkey=self._auth_key)
            self._sftp_client = paramiko.SFTPClient.from_transport(scp)
        except Exception, e:
            agent_log.error("sftp connect failed!")
            agent_log.error(e)
            raise e

    def linux_command(self, cmd_str):
        stdin, stdout, stderr = self._ssh_client.exec_command(cmd_str)
        out_str = stdout.read()
        err_str = stderr.read()
        if err_str:
            agent_log.warning(err_str)
        return out_str

    def __check_expected(self, buff, expected_list):
        for expected_str in expected_list:
            if buff.find(expected_str) != -1:
                return True
        return False

    def __su_root(self):
        self._current_shell.settimeout(30)
        time.sleep(0.1)
        self._current_shell.send("su - root\n")
        buff = ''
        while not buff.endswith('assword: '):
            resp = self._current_shell.recv(9999)
            buff += resp
        self._current_shell.send(self._root_password)
        self._current_shell.send("\n")
        buff = ''
        while buff.find(self._root_prompt) == -1:
            resp = self._current_shell.recv(9999)
            buff += resp
        self._current_shell.send("TMOUT=0")
        self._current_shell.send("\n")
        buff = ""
        while buff.find(self._root_prompt) == -1:
            resp = self._current_shell.recv(9999)
            buff += resp
        self._current_shell.settimeout(1800)

    def execute_root_cmd(self, cmd_str):
        if self._user == "root":
            return self.linux_command(cmd_str)
        else:
            pass

    def execute_shell(self, cmd_str, expected_str=None, time_out=1800):
        def deal_info(info):
            info = re.sub('\r', '', info)
            info = info.split('\n')[1:]
            return '\n'.join(info)
        if expected_str is None:
            expected_str = self._current_prompt
        try:
            self._current_shell.settimeout(time_out)
            time.sleep(0.1)
            self._current_shell.send(cmd_str)
            self._current_shell.send('\n')
        except Exception as e:
            agent_log.error(e)
            raise e
        buff = ''
        time.sleep(0.1)
        try:
            if isinstance(expected_str, list):
                while not self.__check_expected(buff, expected_str):
                    resp = self._current_shell.recv(9999)
                    buff += resp
            else:
                while not buff.find(expected_str) != -1:
                    resp = self._current_shell.recv(9999)
                    buff += resp
        except Exception as e:
            agent_log.error(e)
            raise e
        return deal_info(buff)

    def _check_sftp_login(self):
        if self._sftp_client is None:
            self._sftp_login()
        else:
            try:
                self._sftp_client.listdir()
            except Exception, e:
                agent_log.error(e.message)
                self._sftp_client.close()
                self._sftp_login()

    def put_file(self, local_file, remote_file="./"):
        self._check_sftp_login()
        if os.path.isfile(local_file):
            filename = os.path.basename(local_file)
            if remote_file.endswith("/"):
                remote_file += filename
            try:
                self._sftp_client.put(local_file, remote_file)
            except Exception, e:
                agent_log.error("put file %s to %s falied" % (local_file, remote_file))
                agent_log.error(e)
                raise e
        else:
            agent_log.error("local is a directory")
            raise None

    def put_dir(self, local_dir, remote_dir="./"):
        self._check_sftp_login()
        if os.path.isdir(local_dir):
            if not remote_dir.endswith("/"):
                agent_log.error("remote should be directory (end with '/'), current is %s" % remote_dir)
                raise None
            if remote_dir == "./":
                remote_dir = self.linux_command("pwd %s" % remote_dir)
                remote_dir = remote_dir.strip() + "/"
            local_dir_list = [os.path.abspath(local_dir)]
            while len(local_dir_list) != 0:
                cur_dir = local_dir_list.pop()
                cur_remote_dir = remote_dir + os.path.basename(cur_dir) + "/"
                cmd_str = "mkdir %s" % cur_remote_dir
                self.linux_command(cmd_str)
                file_list = os.listdir(cur_dir)
                for f in file_list:
                    if f[0] == '.':
                        continue
                    if os.path.isdir(os.path.join(cur_dir, f)):
                        local_dir_list.append(os.path.join(cur_dir, f))
                    else:
                        cur_file = os.path.join(cur_dir, f)
                        try:
                            self.put_file(cur_file, cur_remote_dir + f)
                        except Exception, e:
                            agent_log.error("put file %s to %s failed" % (cur_file, cur_remote_dir + f))
                            agent_log.error(e)
                            raise e

    def get_file(self, remote_file, local_file=None):
        self._check_sftp_login()
        if local_file is None:
            local_file = g_agent_temp_path
        if not remote_file.endswith("/"):
            filename = remote_file.split("/")[-1:]
            if os.path.exists(local_file) and os.path.isdir(local_file):
                local_file = os.path.join(local_file, filename)
        try:
            self._sftp_client.get(remote_file, local_file)
        except Exception, e:
            agent_log.error("get file %s to %s failed" % (remote_file, local_file))
            agent_log.error(e)
            raise e



    





