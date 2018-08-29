# -*- coding:utf-8 -*-
# !/usr/bin/env python

__author__ = 'daniel hong'
from ToolAgent.BaseLib.base_object_lib import *
from ToolAgent.BaseLib.base_log_lib import agent_log
from ToolAgent.BaseLib.base_queue_lib import BaseQueue


g_package_receive_queue = BaseQueue("PackageReceive")
g_package_send_queue = BaseQueue("PackageSend")
g_message_send_queue = BaseQueue("MessageSend")
g_message_receive_queue = BaseQueue("MessageReceive")
g_process_status_queue = BaseQueue("ProcessStatus")
g_process_registration_queue = BaseQueue("ProcessRegistration")


def put_send_message_to_queue(l_message_obj):
    l_message_id = l_message_obj.message_id
    l_message_obj.src_port = g_current_port
    l_message_obj.src_ip = g_current_ip
    put_obj_str_to_queue(g_message_send_queue, l_message_id, l_message_obj.get_object_str())


def send_result(l_task_obj):
    message = l_task_obj.get_task_result_message_obj()
    put_send_message_to_queue(message)


def registration_process(l_module_info_obj):
    """

    :type l_module_info_obj: ModuleInfo
    """
    put_obj_str_to_queue(g_process_registration_queue, l_module_info_obj.process_name, l_module_info_obj.get_object_str())


def cancel_registration_process(l_process_name):
    remove_obj_from_queue(g_process_registration_queue, l_process_name)


def get_registration_process_name_list():
    return get_list_from_queue(g_process_registration_queue)


def get_registration_process_info(l_process_name):
    l_process_dict = get_obj_dict_from_queue_without_delete(g_process_registration_queue, l_process_name)
    l_process_info_obj = ModuleInfo()
    l_process_info_obj.set_object_by_dict(l_process_dict)
    return l_process_info_obj


def set_process_status(process_status_obj):
    """

    :type process_status_obj: ProcessStatus
    """
    put_obj_str_to_queue(g_process_status_queue, process_status_obj.process_name, process_status_obj.get_object_str())


def get_process_stop_flg(l_module_name):
    # f = inspect.currentframe().f_back
    # l_path, l_module_name = os.path.split(f.f_code.co_filename)
    l_stop_flg = l_module_name + "_stop"
    l_status_list = get_list_from_queue(g_process_status_queue)
    print l_stop_flg
    if l_stop_flg in l_status_list:
        agent_log.info("%s has to stop" % l_module_name)
        return True
    return False


def set_process_stop_flg(l_process_name):
    l_message_dict = {"to_stop_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    put_obj_str_to_queue(g_process_status_queue, l_process_name + "_stop", json.dumps(l_message_dict))


def set_process_start_flg(l_process_name):
    l_message_dict = {"to_start_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    put_obj_str_to_queue(g_process_status_queue, l_process_name + "_start", json.dumps(l_message_dict))


def set_process_restart_flg(l_process_name):
    l_message_dict = {"to_restart_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    put_obj_str_to_queue(g_process_status_queue, l_process_name + "_restart", json.dumps(l_message_dict))


def get_process_stop_flg_list():
    l_to_stop_process_list = []
    l_process_list = get_registration_process_name_list()
    l_process_status_list = get_list_from_queue(g_process_status_queue)
    for item in l_process_list:
        l_stop_flg = item + "_stop"
        if l_stop_flg in l_process_status_list:
            l_to_stop_process_list.append(item)
    return l_to_stop_process_list


def get_process_start_flg_list():
    l_to_start_process_list = []
    l_process_list = get_registration_process_name_list()
    l_process_status_list = get_list_from_queue(g_process_status_queue)
    for item in l_process_list:
        l_start_flg = item + "_start"
        if l_start_flg in l_process_status_list:
            l_to_start_process_list.append(item)
    return l_to_start_process_list


def get_process_restart_flg_list():
    l_to_restart_process_list = []
    l_process_list = get_registration_process_name_list()
    l_process_status_list = get_list_from_queue(g_process_status_queue)
    for item in l_process_list:
        l_restart_flg = item + "_restart"
        if l_restart_flg in l_process_status_list:
            l_to_restart_process_list.append(item)
    return l_to_restart_process_list


def set_all_stop_flg():
    l_process_obj_list = get_registration_process()
    for item in l_process_obj_list:
        set_process_stop_flg(item.process_name)


def get_registration_process():
    l_process_dict_list = get_obj_dict_list_from_queue_without_delete(g_process_registration_queue)
    l_process_info_obj_list = []
    for item in l_process_dict_list:
        l_module_info_obj = ModuleInfo()
        l_module_info_obj.set_object_by_dict(item)
        l_process_info_obj_list.append(l_module_info_obj)
    return l_process_info_obj_list


def get_process_status(process_name):
    l_process_status_dict = get_obj_dict_from_queue(g_process_status_queue, process_name)
    l_process_obj = ProcessStatus()
    l_process_obj.set_object_by_dict(l_process_status_dict)
    return l_process_obj