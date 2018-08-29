# -*- coding:utf-8 -*-
# !/usr/bin/env python

__author__ = 'daniel hong'
from ToolServer.ServerLib.shell_client import ShellClient
from ToolServer.ServerLib.server_conf import *
from ToolAgent.AgentTemp.agent_queue_manage import *


def get_all_agent_config_info_from_config():
    l_all_agent_config_list = {}
    with open(g_server_agent_list, "r") as fd:
        all_agent_config_str = fd.read()
    for item in all_agent_config_str.splitlines():
        l_agent_config_dict = json.loads(item)
        l_all_agent_config_list.update({l_agent_config_dict["ip"]: l_agent_config_dict})
    return l_all_agent_config_list


def push_agent(l_agent_config_dict):
    l_ssh_client = ShellClient(l_agent_config_dict["ip"], l_agent_config_dict["username"], l_agent_config_dict["user_password"], l_agent_config_dict["root_password"], l_agent_config_dict["key_auth_file"], l_agent_config_dict["key_password"])
    l_ssh_client.put_file(g_agent_zip_file, "/tmp/")
    result = l_ssh_client.execute_root_cmd("unzip /tmp/ToolAgent.zip")
    result = l_ssh_client.execute_root_cmd("nohup python /tmp/ToolAgent/agent_main.py %s %d &" % (l_agent_config_dict["ip"], l_agent_config_dict["port"]))


def get_agent_status(target_ip):
    pass


def set_agent_config_info_to_conf(target_ip, username, user_password, root_password, target_port=12345, ssh_port=22, key_auth_file=None, key_password=None):
    l_agent_info_dict = {"ip": target_ip,
                         "port": target_port,
                         "ssh_port": ssh_port,
                         "username": username,
                         "user_password": user_password,
                         "root_password": root_password,
                         "key_auth_file": key_auth_file,
                         "key_password": key_password
                         }
    with open(g_server_agent_list, "r") as fd:
        l_org_list = fd.read().splitlines()
    l_org_list.append(json.dumps(l_agent_info_dict))
    with open(g_server_agent_list, "w") as fd:
        fd.write("\n".join(l_org_list))


if __name__ == "__main__":
    set_agent_config_info_to_conf("192.168.40.11", "wood", "test123", "huawei")
    set_agent_config_info_to_conf("192.168.40.12", "wood", "test123", "huawei")
    set_agent_config_info_to_conf("192.168.40.13", "wood", "test123", "huawei")


