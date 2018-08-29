# -*- coding:utf-8 -*-
# !/usr/bin/env python
from typing import Union

__author__ = 'daniel hong'
import os
from ToolAgent.BaseLib.base_conf_lib import BaseConf


class AgentConf(BaseConf):
    def __init__(self):
        self.__agent_root_path = os.path.dirname(os.path.dirname(__file__))
        self.__agent_log_path = self.__create_path(os.path.join(self.__agent_root_path, "AgentLog"))
        self.__agent_temp_path = self.__create_path(os.path.join(self.__agent_root_path, "AgentTemp"))
        self.__agent_conf_path = self.__create_path(os.path.join(self.__agent_root_path, "AgentConf"))
        self.__agent_config_file = os.path.join(self.__agent_conf_path, "config")
        BaseConf.__init__(self, self.__agent_config_file)

    def __create_path(self, l_path):
        if not os.path.exists(l_path):
            os.makedirs(l_path)
        return l_path

    @property
    def agent_root_path(self):
        return self.__agent_root_path

    @property
    def agent_log_path(self):
        return self.__agent_log_path

    @property
    def agent_temp_path(self):
        return self.__agent_temp_path

    @property
    def thread_sleep_time(self):
        return self.get_conf_by_key("thread_sleep_time")

    @thread_sleep_time.setter
    def thread_sleep_time(self, l_value):
        if isinstance(l_value, int) or isinstance(l_value, float):
            self.set_conf_by_key_value("thread_sleep_time", l_value)

    @property
    def agent_ip(self):
        return self.get_conf_by_key("ip")

    @agent_ip.setter
    def agent_ip(self, l_value):
        if isinstance(l_value, str):
            self.set_conf_by_key_value("ip", l_value)

    @property
    def agent_port(self):
        return self.get_conf_by_key("port")

    @agent_port.setter
    def agent_port(self, l_value):
        if isinstance(l_value, int) and 0 < l_value < 65536:
            self.set_conf_by_key_value("port", l_value)

    @property
    def agent_type(self):
        return self.get_conf_by_key("agent_type")

    @agent_type.setter
    def agent_type(self, l_value):
        self.set_conf_by_key_value("agent_type", l_value)


g_agent_conf = AgentConf()



