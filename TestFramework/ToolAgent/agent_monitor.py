# -*- coding:utf-8 -*-
# !/usr/bin/env python

__author__ = 'daniel hong'
from ToolAgent.AgentTemp.agent_monitor_lib import *

g_thread_map_lock = thread.allocate_lock()
g_thread_map = {}
g_monitor_list = {}


def check_registration_and_stop_not_registration(l_cur_module):
    l_func_name = sys._getframe().f_code.co_name
    agent_log.info("%s start" % l_func_name)
    while True:
        l_process_name_list = get_registration_process_name_list()
        g_thread_map_lock.acquire()
        l_running_list = g_thread_map.keys()
        g_thread_map_lock.release()
        for l_module_name in l_running_list:
            if l_module_name == l_cur_module:
                continue
            if l_module_name not in l_process_name_list:
                g_thread_map_lock.acquire()
                hd = g_thread_map.pop(l_module_name)
                g_thread_map_lock.release()
                stop_process(l_module_name, hd)
        time.sleep(G_CONSTANT_THREAD_SLEEP)


def check_to_start(l_cur_module):
    l_func_name = sys._getframe().f_code.co_name
    agent_log.info("%s start" % l_func_name)
    while True:
        l_process_registration_name_list = get_registration_process_name_list()
        l_process_to_start_list = get_process_start_flg_list()
        g_thread_map_lock.acquire()
        l_running_list = g_thread_map.keys()
        g_thread_map_lock.release()
        for item in l_process_to_start_list:
            if item == l_cur_module:
                continue
            if item in l_process_registration_name_list and item not in l_running_list:
                l_process_info = get_registration_process_info(item)
                hd = start_process(l_process_info)
                g_thread_map_lock.acquire()
                g_thread_map.update({item: hd})
                g_thread_map_lock.release()
            del_process_start_flg(item)
        time.sleep(G_CONSTANT_THREAD_SLEEP)


def check_to_stop(l_cur_module):
    l_func_name = sys._getframe().f_code.co_name
    agent_log.info("%s start" % l_func_name)
    while True:
        l_process_registration_name_list = get_registration_process_name_list()
        l_process_to_stop_list = get_process_stop_flg_list()
        g_thread_map_lock.acquire()
        l_running_list = g_thread_map.keys()
        g_thread_map_lock.release()
        for item in l_process_to_stop_list:
            if item == l_cur_module:
                continue
            if item in l_process_registration_name_list and item in l_running_list:
                g_thread_map_lock.acquire()
                hd = g_thread_map.pop(item)
                g_thread_map_lock.release()
                while True:
                    if hd.is_alive():
                        time.sleep(G_CONSTANT_THREAD_SLEEP)
                    else:
                        break
            del_process_stop_flg(item)
        time.sleep(G_CONSTANT_THREAD_SLEEP)


def check_running(l_cur_module):
    l_func_name = sys._getframe().f_code.co_name
    agent_log.info("%s start" % l_func_name)
    while True:
        g_thread_map_lock.acquire()
        l_running_list = g_thread_map.keys()
        g_thread_map_lock.release()
        for item in l_running_list:
            if item == l_cur_module:
                continue
            g_thread_map_lock.acquire()
            if item in g_thread_map.keys():
                hd = g_thread_map[item]
                if hd is None or (not hd.is_alive()):
                    try:
                        l_process_info = get_registration_process_info(item)
                        hd = start_process(l_process_info)
                        g_thread_map.update({item: hd})
                    except Exception as e:
                        agent_log.error(e.message)
            g_thread_map_lock.release()
        time.sleep(G_CONSTANT_THREAD_SLEEP)


def check_to_restart(l_cur_module):
    l_func_name = sys._getframe().f_code.co_name
    agent_log.info("%s start" % l_func_name)
    while True:
        l_process_registration_name_list = get_registration_process_name_list()
        l_process_to_restart_list = get_process_restart_flg_list()
        g_thread_map_lock.acquire()
        l_running_list = g_thread_map.keys()
        g_thread_map_lock.release()
        for item in l_process_to_restart_list:
            if item == l_cur_module:
                continue
            if item in l_process_registration_name_list and item in l_running_list:
                g_thread_map_lock.acquire()
                hd = g_thread_map.pop(item)
                g_thread_map_lock.release()
                stop_process(item, hd)
                l_process_info = get_registration_process_info(item)
                hd = start_process(l_process_info)
                g_thread_map_lock.acquire()
                g_thread_map.update({item: hd})
                g_thread_map_lock.release()
            del_process_restart_flg(item)
        time.sleep(G_CONSTANT_THREAD_SLEEP)


def start_all_monitor(l_cur_module):
    l_monitor_name_list = ["check_registration_and_stop_not_registration",
                           "check_to_start", "check_to_stop", "check_running",
                           "check_to_restart"]
    for l_monitor in l_monitor_name_list:
        if l_monitor not in g_monitor_list.keys() or (not g_monitor_list[l_monitor].is_alive()):
            l_func = getattr(sys.modules[__name__], l_monitor)
            hd = threading.Thread(target=l_func, args=(l_cur_module, ))
            hd.setDaemon(True)
            hd.start()
            g_monitor_list.update({l_monitor: hd})


def agent_monitor():
    delete_all_stop_flg()
    l_cur_module_name = sys._getframe().f_code.co_name
    agent_log.info("%s start" % l_cur_module_name)
    g_thread_map.update({l_cur_module_name: None})
    while True:
        start_all_monitor(l_cur_module_name)
        time.sleep(G_CONSTANT_THREAD_SLEEP)
        if get_process_stop_flg(l_cur_module_name):
            break
    agent_log.info("%s stopped" % l_cur_module_name)


if __name__ == "__main__":
    agent_monitor()