# -*- coding:utf-8 -*-
# !/usr/bin/env python

__author__ = 'daniel hong'
import os
import sys
import commands


class Process:
    def __init__(self, command):
        self._command = self._process_command(command)
        self._process = os.popen(self._command)

    def __str__(self):
        return self._command

    def read(self):
        return self._process_output(self._process.read())

    def close(self):
        try:
            rc = self._process.close()
        except IOError:
            return 255
        if rc is None:
            return 0
        if os.sep == '\\' or sys.platform.startswith('java'):
            return rc % 256
        return rc >> 8

    def _process_command(self, command):
        if '>' not in command:
            if command.endswith("&"):
                command = command[:-1] + ' 2>&1 &'
            else:
                command += ' 2>&1'
        return self._encode_to_file_system(command)

    def _encode_to_file_system(self, string):
        enc = sys.getfilesystemencoding()
        return string.encode(enc) if enc else string

    def _process_output(self, stdout):
        stdout = stdout.replace('\r\n', '\n')
        if stdout.endswith('\n'):
            stdout = stdout[:-1]
        return stdout


def execute_cmd(cmd_str):
    if sys.platform.find("win") != -1:
        ps = Process(cmd_str)
        l_result = ps.read()
        l_status = ps.close()
    else:
        l_status, l_result = commands.getstatusoutput(cmd_str)
    if l_status == 0:
        return {"result": True, "body": l_result}
    else:
        return {"result": False, "body": l_result}


def upload_file(argvs_dict):
    pass


def download_file(argvs_dict):
    pass


def search_keyword(argvs_dict):
    pass


if __name__ == "__main__":
    l_temp = os.path.join(os.path.dirname(os.path.dirname(__file__)), "AgentTemp", "temp.txt")
    result = execute_cmd("dir .")
    print result
    with open(l_temp, "w") as fd:
        fd.write(result["body"])
