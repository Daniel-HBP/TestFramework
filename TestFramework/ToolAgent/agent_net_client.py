# -*- coding:utf-8 -*-
# !/usr/bin/env python

__author__ = 'daniel hong'
from ToolAgent.AgentLib.agent_net_lib import *


def do_send(l_package_obj):
    """

    :type l_package_obj: NetMessagePackage
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except Exception as e:
        agent_log.error(e)
        raise e
    try:
        s.connect((l_package_obj.__dst_ip, l_package_obj.__dst_port))
    except socket.error as e:
        agent_log.error("error code: %s, message: %s" % (str(e.errno), e.message))
        raise e
    try:
        l_package_str = l_package_obj.get_object_str() + G_CONSTANT_MSG_END_FLG
        s.sendall(l_package_str)
    except socket.error as e:
        agent_log.error("error code: %s, message: %s" % (str(e.errno), e.message))
        raise e
    buff = ""
    while True:
        try:
            data = s.recv(G_CONSTANT_BUFFER_SIZE)
        except socket.error as e:
            agent_log.error("error code: %s, message: %s" % (str(e.errno), e.message))
            s.close()
            raise e
        buff += data
        if buff.strip() == G_CONSTANT_MSG_ACK:
            s.close()
            break


def agent_client():
    l_func_name = sys._getframe().f_code.co_name
    agent_log.info("%s start" % l_func_name)
    while True:
        l_send_package_list = get_send_package_list_from_queue()
        for item in l_send_package_list:
            thread.start_new_thread(do_send, (item,))
        if get_process_stop_flg(l_func_name):
            break
        time.sleep(G_CONSTANT_THREAD_SLEEP)
    agent_log.info("%s stopped" % l_func_name)


if __name__ == "__main__":
    agent_client()
