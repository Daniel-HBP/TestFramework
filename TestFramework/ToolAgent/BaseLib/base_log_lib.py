# -*- coding:utf-8 -*-
# !/usr/bin/env python

__author__ = 'daniel hong'
import datetime
import os
import sys
import thread
import threading
import inspect
import multiprocessing as mp


def log_cur_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')


def get_root_path():
    return os.path.dirname(os.path.dirname(__file__))


class AgentLog:
    def __init__(self):
        l_path, l_file = os.path.split(sys.argv[0])
        log_file = l_file[:-3] + ".log"
        l_root_path = get_root_path()
        temp_log_name = os.path.join(l_root_path, "AgentLog", log_file)
        self.log_file = temp_log_name
        self._g_log_lock = thread.allocate_lock()
        self._g_log_list = []
        if os.path.exists(self.log_file):
            self._log_file_fd = open(self.log_file, "a")
        else:
            self._log_file_fd = open(self.log_file, "w")
        # thread.start_new_thread(self._write_to_disk, ())

    def __del__(self):
        print "log instance exit"
        self._log_file_fd.close()

    def _write_log(self, log_message):
        print log_message
        self._g_log_lock.acquire()
        try:
            self._log_file_fd.write(log_message + "\n")
        except Exception as e:
            print e
        self._g_log_lock.release()

    def info(self, log_str):
        f = inspect.currentframe().f_back
        path, mod = os.path.split(f.f_code.co_filename)
        line_no = f.f_lineno
        func_name = f.f_code.co_name
        process_name = mp.current_process().name
        thread_name = threading.currentThread().getName()
        log_message = '%s INFO %s %s %s %s [Line:%s]: %s' % (log_cur_time(), process_name, thread_name, mod, func_name, line_no, log_str)
        self._write_log(log_message)

    def error(self, log_str):
        f = inspect.currentframe().f_back
        path, mod = os.path.split(f.f_code.co_filename)
        line_no = f.f_lineno
        func_name = f.f_code.co_name
        process_name = mp.current_process().name
        thread_name = threading.currentThread().getName()
        log_message = '%s ERROR %s %s %s %s [Line:%s]: %s' % (log_cur_time(), process_name, thread_name, mod, func_name, line_no, log_str)
        self._write_log(log_message)

    def debug(self, log_str):
        f = inspect.currentframe().f_back
        path, mod = os.path.split(f.f_code.co_filename)
        line_no = f.f_lineno
        func_name = f.f_code.co_name
        process_name = mp.current_process().name
        thread_name = threading.currentThread().getName()
        log_message = '%s DEBUG %s %s %s %s [Line:%s]: %s' % (log_cur_time(), process_name, thread_name, mod, func_name, line_no, log_str)
        self._write_log(log_message)

    def warning(self, log_str):
        f = inspect.currentframe().f_back
        path, mod = os.path.split(f.f_code.co_filename)
        line_no = f.f_lineno
        func_name = f.f_code.co_name
        process_name = mp.current_process().name
        thread_name = threading.currentThread().getName()
        log_message = '%s WARNING %s %s %s %s [Line:%s]: %s' % (log_cur_time(), process_name, thread_name, mod, func_name, line_no, log_str)
        self._write_log(log_message)


agent_log = AgentLog()

