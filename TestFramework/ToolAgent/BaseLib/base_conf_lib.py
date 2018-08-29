# -*- coding:utf-8 -*-
# !/usr/bin/env python

__author__ = 'daniel hong'
import os


class BaseConf:
    def __init__(self, l_configuration_file):
        l_config_path = os.path.dirname(l_configuration_file)
        if not os.path.exists(l_config_path):
            os.makedirs(l_config_path)
        if not os.path.exists(l_configuration_file):
            fd = open(l_configuration_file, "w")
            fd.close()
        self._configuration_file = l_configuration_file
        self._configuration_dict = {}
        self.__get_conf_from_file()

    def __get_conf_from_file(self):
        with open(self._configuration_file, "r") as l_fd:
            l_conf_str = l_fd.read()
        for l_line in l_conf_str.splitlines():
            l_kv = l_line.split("$=$")
            l_key = l_kv[0]
            if len(l_kv) < 2:
                l_value = ""
            else:
                l_value = l_kv[1]

            self._configuration_dict.update({l_key: l_value})

    def __refresh_conf(self):
        self.__get_conf_from_file()

    def __update_conf(self):
        with open(self._configuration_file, "w") as l_fd:
            for l_key in self._configuration_dict.keys():
                l_fd.write("%s$=$%s" % (str(l_key), str(self._configuration_dict[l_key])))

    def get_conf_by_key(self, l_key_name):
        if l_key_name in self._configuration_dict.keys():
            return self._configuration_dict[l_key_name]
        return None

    def set_conf_by_key_value(self, l_key_name, l_value):
        self._configuration_dict.update({l_key_name: l_value})
        self.__update_conf()
