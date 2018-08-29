# -*- coding:utf-8 -*-
# !/usr/bin/env python

__author__ = 'daniel hong'
import os

g_server_root_path = os.path.dirname(os.path.dirname(__file__))
g_server_conf_path = os.path.join(g_server_root_path, "ServerConf")
g_server_temp_path = os.path.join(g_server_root_path, "ServerTemp")
g_server_agent_list = os.path.join(g_server_conf_path, "agent_list")
g_agent_list_queue = "AgentStatus"
g_agent_zip_file = os.path.join(g_server_temp_path, "ToolAgent.zip")