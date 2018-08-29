# -*- coding:utf-8 -*-
# !/usr/bin/env python

__author__ = 'daniel hong'
from ToolServer.ServerLib.agent_management_lib import *


def api_cmd_base(l_message_obj):
    l_message_id = l_message_obj.message_id
    put_send_message_to_queue(l_message_obj)
    l_timeout = l_message_obj.func_timeout + 10
    while l_timeout > 0:
        l_file_list = g_message_receive_queue.get_queue_keys()
        if l_message_id in l_file_list:
            l_result_message = g_message_receive_queue.get_obj_by_key(l_message_id)
            return l_result_message.result_info
        l_timeout -= 1
    result_body = {"result": False, "body": "timeout"}
    return {"result_code": G_CONSTANT_RESULT_TIMEOUT, "result_id": l_message_id, "result_body": result_body}


def execute_root_cmd(target_ip, cmd_str, timeout=30):
    l_temp_message = TaskMessageObject()
    l_temp_message.func_timeout = timeout
    l_temp_message.func_name = "execute_root_cmd"
    l_temp_message.func_argvs = cmd_str
    l_agent_info = get_agent_info(target_ip)
    l_temp_message.dst_ip = l_agent_info["ip"]
    l_temp_message.dst_port = l_agent_info["port"]
    result = api_cmd_base(l_temp_message)
    return result["result_body"]


def upload_file(target_ip, src_file, dst_path, timeout=30):
    pass


def download_file(target_ip, src_file, dst_path, timout=30):
    pass


def search_keywords_in_path(target_ip, keyword_list, search_path, timeout=30):
    pass


if __name__ == "__main__":
    count = 30
    while count > 0:
        time.sleep(1)
        count -= 1
    set_all_stop_flg()