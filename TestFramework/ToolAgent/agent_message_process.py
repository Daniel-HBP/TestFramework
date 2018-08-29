# -*- coding:utf-8 -*-
# !/usr/bin/env python

__author__ = 'daniel hong'
from ToolAgent.AgentLib.agent_net_lib import *


def get_message_from_receive_package_queue():
    l_package_list = get_receive_package_list_from_queue()
    for l_package_obj in l_package_list:
        try:
            l_message_obj = TaskMessageObject()
            l_message_obj.set_object_by_dict(l_package_obj.message)
            put_obj_str_to_queue(g_message_receive_queue, l_message_obj.message_id, l_message_obj.get_object_str())
        except Exception as e:
            continue


def put_message_to_send_package_queue():
    l_message_list = get_obj_dict_list_from_queue(g_message_send_queue)
    for item in l_message_list:
        try:
            l_message_obj = TaskMessageObject()
            l_message_obj.set_object_by_dict(item)
            l_package_obj = NetMessagePackage()
            l_package_obj.__dst_ip = l_message_obj.dst_ip
            l_package_obj.__dst_port = l_message_obj.dst_port
            l_package_obj.__src_ip = l_message_obj.src_ip
            l_package_obj.__src_port = l_message_obj.src_port
            l_package_obj.__message = l_message_obj.get_object_dict()
            put_send_package_to_queue(l_package_obj)
        except Exception as e:
            continue


def message_processor():
    recv_hd = threading.Thread(target=get_message_from_receive_package_queue, args=())
    recv_hd.setDaemon(True)
    send_hd = threading.Thread(target=put_message_to_send_package_queue, args=())
    send_hd.setDaemon(True)
    recv_hd.start()
    send_hd.start()
    l_func_name = sys._getframe().f_code.co_name
    agent_log.info("%s start" % l_func_name)
    while True:
        if not recv_hd.is_alive():
            recv_hd = threading.Thread(target=get_message_from_receive_package_queue, args=())
            recv_hd.setDaemon(True)
            recv_hd.start()
        if not send_hd.is_alive():
            send_hd = threading.Thread(target=put_message_to_send_package_queue, args=())
            send_hd.setDaemon(True)
            send_hd.start()
        if get_process_stop_flg(l_func_name):
            break
        time.sleep(G_CONSTANT_BUFFER_SIZE)
    agent_log.info("%s stopped" % l_func_name)


if __name__ == "__main__":
    message_processor()