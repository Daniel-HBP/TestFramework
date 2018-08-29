# -*- coding:utf-8 -*-
# !/usr/bin/env python

__author__ = 'daniel hong'
import os
import time
import shutil
import json


class BaseQueue:
    def __init__(self, l_queue_name):
        l_current_path = os.path.abspath(__file__)
        l_queue_root = self.__create_path(os.path.join(os.path.dirname(l_current_path), "Queue"))
        self.__queue_root = l_queue_root
        self.__queue_id = time.strftime("%Y%m%d%H%M%S")
        # self.__queue_id = ""
        self.queue_name = l_queue_name
        self.__queue = self.__create_path(os.path.join(l_queue_root, l_queue_name))
        self.__queue_temp = self.__create_path(os.path.join(l_queue_root, l_queue_name + "Temp"))
        self.__queue_error = self.__create_path(os.path.join(l_queue_root, l_queue_name + "Error"))

    def __create_path(self, l_path):
        if not os.path.exists(l_path):
            os.makedirs(l_path)
        return l_path

    def get_queue_keys(self):
        l_queue_org_keys = os.listdir(self.__queue)
        l_queue_keys = []
        for l_obj in l_queue_org_keys:
            l_obj.replace(self.__queue_id, "")
            l_queue_keys.append(l_obj)
        return l_queue_keys

    def remove_queue_obj(self, l_key_name):
        l_obj = os.path.join(self.__queue, l_key_name + self.__queue_id)
        if os.path.exists(l_obj):
            try:
                os.remove(l_obj)
            except Exception, e:
                return False
        return True

    def get_obj_by_key(self, l_key_name):
        l_key_name = l_key_name + self.__queue_id
        l_obj = os.path.join(self.__queue, l_key_name)
        if os.path.exists(l_obj):
            try:
                with open(l_obj, "r") as fd:
                    l_dict_str = fd.read()
                l_obj_dict = json.loads(l_dict_str)
                return l_obj_dict
            except Exception as e:
                self.__move_obj_to_error_queue(l_key_name, e.message)
        return None

    def pop_obj_by_key(self, l_key_name):
        l_key_name = l_key_name + self.__queue_id
        l_obj = os.path.join(self.__queue, l_key_name)
        if os.path.exists(l_obj):
            try:
                with open(l_obj, "r") as fd:
                    l_dict_str = fd.read()
                l_obj_dict = json.loads(l_dict_str)
                os.remove(l_obj)
                return l_obj_dict
            except Exception as e:
                self.__move_obj_to_error_queue(l_key_name, e.message)
        return None

    def append_new_obj(self, l_key_name, l_queue_obj):
        l_key_name = l_key_name + self.__queue_id
        l_src_obj = os.path.join(self.__queue_temp, l_key_name)
        l_dst_obj = os.path.join(self.__queue, l_key_name)
        with open(l_src_obj, "w") as fd:
            if isinstance(l_queue_obj, str):
                fd.write(l_queue_obj)
            else:
                fd.write(json.dumps(l_queue_obj))
        shutil.move(l_src_obj, l_dst_obj)

    def __move_obj_to_error_queue(self, l_key_name, error_message):
        l_src_obj = os.path.join(self.__queue, l_key_name)
        l_dst_obj = os.path.join(self.__queue_error, l_key_name)
        shutil.move(l_src_obj, l_dst_obj)
        l_error_file = os.path.join(self.__queue_error, l_key_name + "_error")
        with open(l_error_file, "w") as fd:
            fd.write(error_message)


