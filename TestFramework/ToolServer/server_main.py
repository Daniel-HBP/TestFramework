# -*- coding:utf-8 -*-
# !/usr/bin/env python

__author__ = 'daniel hong'
from ToolAgent.agent_monitor import agent_monitor
from ToolAgent.AgentTemp.agent_queue_manage import *


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
    l_service_module_map = {"agent_server": {"path": "ToolAgent", "file": "agent_net_server"},
                            "agent_client": {"path": "ToolAgent", "file": "agent_net_client"},
                            "agent_monitor": {"path": "ToolAgent", "file": "agent_monitor"},
                            "message_processor": {"path": "ToolAgent", "file": "agent_message_process"},
                            "server_file_syn": {"path": "ToolAgent", "file": "server_file_syn"}
                            }
    for item in l_service_module_map.keys():
        l_reg_info = ModuleInfo(l_module_path=l_service_module_map[item]["path"], l_module_name=l_service_module_map[item]["file"], l_process_name=item, l_args=())
        registration_process(l_reg_info)
    for item in l_service_module_map.keys():
        set_process_start_flg(item)
    agent_monitor()


