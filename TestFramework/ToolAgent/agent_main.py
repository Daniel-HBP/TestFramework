# -*- coding:utf-8 -*-
# !/usr/bin/env python

__author__ = 'daniel hong'
from ToolAgent.AgentLib.agent_conf import g_agent_conf
from ToolAgent.AgentLib.agent_net_lib import BaseNetModule, agent_log


class AgentMain:
    def __init__(self, l_agent_listen_ip, l_agent_listen_port):
        g_agent_conf.agent_ip = l_agent_listen_ip
        g_agent_conf.agent_port = l_agent_listen_port
        self._net_module = BaseNetModule(g_agent_conf.agent_ip, g_agent_conf.agent_port)


    def start(self):
        pass


if __name__ == '__main__':
    if len(sys.argv) == 4:
        l_role = sys.argv[1]
        l_server_ip = sys.argv[2]
        l_server_port = sys.argv[3]
        set_current_agent_info(l_server_ip, l_server_port, l_role)
    elif len(sys.argv) == 3:
        l_server_ip = sys.argv[1]
        l_server_port = sys.argv[2]
        set_current_agent_info(l_server_ip, l_server_port)
    elif len(sys.argv) == 2:
        l_server_ip = sys.argv[1]
        set_current_agent_info(l_server_ip)
    l_service_module_map = {"agent_server": "agent_net_server",
                            "agent_client": "agent_net_client",
                            "agent_monitor": "agent_monitor",
                            "message_processor": "agent_message_process",
                            "task_manager": "agent_task_manage"}
    for item in l_service_module_map.keys():
        l_reg_info = ModuleInfo(l_module_path="ToolAgent", l_module_name=l_service_module_map[item], l_process_name=item, l_args=())
        registration_process(l_reg_info)
    for item in l_service_module_map.keys():
        set_process_start_flg(item)
    agent_monitor()


