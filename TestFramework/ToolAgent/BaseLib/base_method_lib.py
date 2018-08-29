# -*- coding:utf-8 -*-
# !/usr/bin/env python

__author__ = 'daniel hong'
import os
import sys
import commands
import time
import random
import threading
import traceback
import datetime
import multiprocessing


class WinCmdProcess:
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
        return string.decode(enc) if enc else string

    def _process_output(self, stdout):
        stdout = stdout.replace('\r\n', '\n')
        if stdout.endswith('\n'):
            stdout = stdout[:-1]
        return stdout


def execute_win_cmd(cmd_string):
    ps = WinCmdProcess(cmd_string)
    l_output = ps.read()
    l_result_code = ps.close()
    return l_result_code, l_output


def execute_cmd(cmd_str):
    if sys.platform.find("win") != -1:
        ps = WinCmdProcess(cmd_str)
        l_result = ps.read()
        l_status = ps.close()
    else:
        l_status, l_result = commands.getstatusoutput(cmd_str)
    return l_status, l_result


def calc_exec_time(func):
    def wrapper(*args, **kwargs):
        l_start = datetime.datetime.now()
        try:
            func(*args, **kwargs)
        except Exception, e:
            print("%s exception. exception info: %s" % (func.__name__, e.message))
            exec_type, exec_value, exec_traceback = sys.exc_info()
            print(''.join(traceback.format_exception(exec_type, exec_value, exec_traceback)))
        l_end = datetime.datetime.now()
        print("function: %s, executed time: %d.%d ms" % (func.__name__, (l_end-l_start).total_seconds(), (l_end-l_start).microseconds))
    return wrapper


class ThreadParallelTask(object):
    def __init__(self):
        self._func_info_list = {}
        self._func_info_list_lock = threading.Lock()
        self._max_thread_num = 1024
        self._current_thread_num = 0
        self._wait_thread_num = 0
        self._wait_thread_num_lock = threading.Lock()
        self._THREAD_RUN = 1
        self._THREAD_READY = 0
        self._THREAD_ERROR = -1
        self._THREAD_FINISHED = 2

    def _add_wait_thread(self):
        self._wait_thread_num_lock.acquire()
        self._wait_thread_num += 1
        self._wait_thread_num_lock.release()

    def _sub_wait_thread(self):
        self._wait_thread_num_lock.acquire()
        self._wait_thread_num -= 1
        self._wait_thread_num_lock.release()

    def _update_func_info_list(self, l_key, l_value):
        self._func_info_list_lock.acquire()
        self._func_info_list.update({l_key: l_value})
        self._func_info_list_lock.release()

    def _update_func_info(self, l_handler, l_key, l_value):
        self._func_info_list_lock.acquire()
        self._func_info_list[l_handler][l_key] = l_value
        self._func_info_list_lock.release()

    def _pop_func_info_list(self, l_key):
        self._func_info_list_lock.acquire()
        if l_key in self._func_info_list.keys():
            self._func_info_list.pop(l_key)
        self._func_info_list_lock.release()

    def register(self, func, *args, **kwargs):
        if self._current_thread_num > self._max_thread_num:
            return None
        self._current_thread_num += 1
        l_handler = str(int(time.time())) + str(random.randint(1000, 9999))
        l_func_info = {"name": func, "args": args, "kwargs": kwargs, "result": None, "thread_hd": None, "status": self._THREAD_READY, "error": None}
        self._update_func_info_list(l_handler, l_func_info)
        return l_handler

    def unregister(self, func_handler, force_flag=True):
        if force_flag:
            self._pop_func_info_list(func_handler)
        else:
            if func_handler in self._func_info_list.keys():
                while self._func_info_list[func_handler]["status"] == self._THREAD_RUN:
                    time.sleep(1)
                self._pop_func_info_list(func_handler)
        self._current_thread_num -= 1
        return True

    def reset(self, force_flag=True):
        if force_flag:
            self._func_info_list = {}
        else:
            for l_handler in self._func_info_list.keys():
                while self._func_info_list[l_handler]["status"] == self._THREAD_RUN:
                    time.sleep(1)
                self._pop_func_info_list(l_handler)
        self._current_thread_num = 0
        return True

    def _wrapper_func(self, l_handler):
        func = self._func_info_list[l_handler]["name"]
        args = self._func_info_list[l_handler]["args"]
        kwargs = self._func_info_list[l_handler]["kwargs"]
        try:
            self._update_func_info(l_handler, "status", self._THREAD_RUN)
            l_result = func(*args, **kwargs)
            self._update_func_info(l_handler, "result", l_result)
            self._update_func_info(l_handler, "status", self._THREAD_FINISHED)
        except Exception, e:
            self._update_func_info(l_handler, "status", self._THREAD_ERROR)
            self._update_func_info(l_handler, "error", e.message)

    @calc_exec_time
    def start(self):
        for l_handler in self._func_info_list.keys():
            hd = threading.Thread(target=ThreadParallelTask._wrapper_func, args=(self, l_handler))
            hd.setDaemon(True)
            hd.start()
            self._update_func_info(l_handler, "thread_hd", hd)

    def _join_thread(self, l_hd, time_out):
        if time_out is not None:
            l_hd.join(time_out)
        else:
            l_hd.join()
        self._sub_wait_thread()

    def wait_end(self, time_out=None):
        for l_handler in self._func_info_list.keys():
            l_hd = self._func_info_list[l_handler]["thread_hd"]
            l_temp_hd = threading.Thread(target=ThreadParallelTask._join_thread, args=(self, l_hd, time_out))
            l_temp_hd.setDaemon(True)
            self._add_wait_thread()
            l_temp_hd.start()
        while self._wait_thread_num != 0:
            time.sleep(1)

    def get_result(self, func_handler):
        l_result = None
        self._func_info_list_lock.acquire()
        if func_handler in self._func_info_list.keys():
            l_result = self._func_info_list[func_handler]["result"]
        self._func_info_list_lock.release()
        return l_result


class ProcessParallelTask(object):
    def __init__(self):
        pass

