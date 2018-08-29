# -*- coding: utf-8 -*-
__author__ = 'daniel hong'
from ToolServer.ServerLib.server_conf import *
from ToolAgent.AgentLib.agent_common import *
import wmi
import time


class WindowsClient:
    def __init__(self, win_ip, username, password):
        self.ip = win_ip
        self.username = username
        self.password = password
        self.conn = wmi.WMI(computer=win_ip, user=username, password=password)
        self.remote_sys_directory = self.__get_sys_directory()
        self.local_temp_dir = g_server_temp_path
        self.remote_windows_directory = os.path.dirname(self.remote_sys_directory)
        self.remote_system_partition = os.path.dirname(self.remote_windows_directory)
        self.remote_system_partition_char = self.remote_system_partition.split(":")[0]

    def __get_sys_directory(self):
        l_win_sys = self.conn.Win32_OperatingSystem()
        return l_win_sys[0].SystemDirectory

    def get_process_status(self, p_id):
        l_process_info = self.conn.ExecQuery('select * from Win32_Process where ProcessId="%d"' % p_id)
        if l_process_info is None or len(l_process_info) == 0:
            return None
        return l_process_info

    def kill_remote_process_by_pid(self, p_id):
        cmd_string = "cmd /c taskkill /pid %d /f" % p_id
        return self.execute_cmd_without_output(cmd_string)

    def __set_net_use_connect(self, l_remote_root):
        cmd_str = 'net use \\\\%s\\%s$ "%s" /USER:%s' % (self.ip, l_remote_root, self.password, self.username)
        l_result = execute_win_cmd(cmd_str)
        if l_result[0] != 0:
            return False
        return True

    def __del_net_use_connect(self, l_remote_root):
        cmd_str = 'net use \\\\%s\\%s$ /del' % (self.ip, l_remote_root)
        l_result = execute_win_cmd(cmd_str)
        if l_result[0] != 0:
            return False
        return True

    def __get_cmd_result(self, l_result_file):
        l_file_basename = os.path.basename(l_result_file)
        if self.__set_net_use_connect(self.remote_system_partition_char):
            l_remote_temp_file = "\\\\%s\\%s" % (self.ip, l_result_file.replace(":", "$"))
            l_result = execute_win_cmd('copy  %s %s' % (l_remote_temp_file, self.local_temp_dir))
            if l_result[0] == 0:
                execute_win_cmd('del %s' % l_remote_temp_file)
                self.__del_net_use_connect(self.remote_system_partition_char)
                l_cmd_result = execute_win_cmd('type %s\\%s' % (self.local_temp_dir, l_file_basename))
                if l_cmd_result[0] == 0:
                    execute_win_cmd('del %s\\%s' % (self.local_temp_dir, l_file_basename))
                    return l_cmd_result
            else:
                self.__del_net_use_connect(self.remote_system_partition_char)
        return None

    def execute_cmd_without_output(self, cmd_string, time_out=10):
        p_id, create_result = self.conn.Win32_Process.Create(CommandLine=cmd_string)
        if create_result == 0:
            l_time_out = time_out
            while self.get_process_status(p_id) is not None:
                if l_time_out < 0:
                    return -1
                else:
                    time.sleep(1)
                    l_time_out -= 1
        return create_result

    def execute_asyn_cmd(self, cmd_string):
        return self.conn.Win32_Process.Create(CommandLine=cmd_string)

    def execute_cmd(self, cmd_string, time_out=10):
        l_result_file = os.path.join(self.remote_windows_directory, "win_client_%s" % (time.strftime("%Y%m%d%H%M%S")))
        cmd_string = 'cmd /c ( %s ) > %s' % (cmd_string, l_result_file)
        p_id, create_result = self.conn.Win32_Process.Create(CommandLine=cmd_string)
        if create_result == 0:
            l_time_out = time_out
            while self.get_process_status(p_id) is not None:
                if l_time_out < 0:
                    return None
                else:
                    time.sleep(1)
                    l_time_out -= 1
            l_result = self.__get_cmd_result(l_result_file)
            if l_result is not None:
                return l_result[1]
        return None

    def put_file_to_remote(self, l_src_file, l_remote_dir):
        self.execute_cmd_without_output('mkdir "%s"' % l_remote_dir)
        l_remote_root = l_remote_dir.split(":")[0]
        l_remote_dir = l_remote_dir.replace(":", "$")
        if self.__set_net_use_connect(l_remote_root):
            l_result = execute_win_cmd('copy "%s" "\\\\%s\\%s"' % (l_src_file, self.ip, l_remote_dir))
            self.__del_net_use_connect(l_remote_root)
            if l_result[0] == 0:
                return True
        return False

    def get_file_from_remote(self, l_remote_file, l_local_dir=None):
        if l_local_dir is None:
            l_local_dir = g_server_temp_path
        l_remote_root = l_remote_file.split(":")[0]
        l_file_basename = os.path.basename(l_remote_file)
        l_remote_file = l_remote_file.replace(":", "$")
        if not os.path.exists(l_local_dir):
            os.makedirs(l_local_dir)
        if self.__set_net_use_connect(l_remote_root):
            l_result = execute_win_cmd('copy "\\\\%s\\%s" "%s"' % (self.ip, l_remote_file, l_local_dir))
            self.__del_net_use_connect(l_remote_root)
            if l_result[0] == 0:
                return os.path.join(l_local_dir, l_file_basename)
        return None
