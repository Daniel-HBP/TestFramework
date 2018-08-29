# -*- coding:utf-8 -*-
# !/usr/bin/env python

__author__ = 'daniel hong'
from ToolAgent.AgentTemp.agent_queue_manage import *


def start_process(l_process_obj):
    """

    :type l_process_obj: ModuleInfo
    """
    try:
        l_module_name = "%s.%s" % (l_process_obj.module_path, l_process_obj.module_name)
        if l_module_name not in sys.modules.keys():
            importlib.import_module(l_module_name)
        l_func = getattr(sys.modules[l_module_name], l_process_obj.process_name)
        hd = threading.Thread(target=l_func, args=l_process_obj.module_args)
        hd.start()
        return hd
    except Exception as e:
        agent_log.error(e.message)
        return None


def stop_process(l_process_name, hd):
    set_process_stop_flg(l_process_name)
    count = 3
    while True:
        if hd.is_alive() or count < 0:
            count -= 1
            time.sleep(G_CONSTANT_THREAD_SLEEP)
        else:
            break
    del_process_stop_flg(l_process_name)
    return l_process_name


def delete_all_stop_flg():
    l_process_list = get_registration_process()
    for item in l_process_list:
        del_process_stop_flg(item.process_name)


def del_process_stop_flg(l_process_name):
    l_stop_flg = l_process_name + "_stop"
    remove_obj_from_queue(g_process_status_queue, l_stop_flg)


def del_process_start_flg(l_process_name):
    l_start_flg = l_process_name + "_start"
    remove_obj_from_queue(g_process_status_queue, l_start_flg)


def del_process_restart_flg(l_process_name):
    l_start_flg = l_process_name + "_restart"
    remove_obj_from_queue(g_process_status_queue, l_start_flg)