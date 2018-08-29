# -*- coding:utf-8 -*-
# !/usr/bin/env python

__author__ = 'daniel hong'
import sys
import datetime
import traceback
from ToolAgent.BaseLib.base_method_lib import execute_cmd, execute_win_cmd
from ToolAgent.BaseLib.base_log_lib import agent_log


def calc_func_exec_time(func):
    def wrapper(*args, **kwargs):
        l_start = datetime.datetime.now()
        try:
            func(*args, **kwargs)
        except Exception, e:
            agent_log.error("%s exception. exception info: %s" % (func.__name__, e.message))
            exec_type, exec_value, exec_traceback = sys.exc_info()
            agent_log.error(''.join(traceback.format_exception(exec_type, exec_value, exec_traceback)))
        l_end = datetime.datetime.now()
        agent_log.info("function %s, executed time: %d" % (func.__name__, (l_end-l_start).seconds))
    return wrapper


def upload_file(argvs_dict):
    pass


def download_file(argvs_dict):
    pass


def search_keyword(argvs_dict):
    pass

