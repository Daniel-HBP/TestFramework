# -*- coding:utf-8 -*-
# !/usr/bin/env python

__author__ = 'daniel hong'
from ToolAgent.BaseLib.base_data_lib import *
import uuid
import datetime
import json


class MyBaseObject:
    def __init__(self):
        self.object_dict = None
        self.__gen_object_dict()

    def set_object_by_dict(self, l_object_dict):
        pass

    def __gen_object_dict(self):
        pass

    def resolve_object_by_str(self, l_object_str):
        l_object_dict = json.loads(l_object_str)
        self.set_object_by_dict(l_object_dict)

    def get_object_dict(self):
        self.__gen_object_dict()
        return self.object_dict

    def get_object_str(self):
        self.__gen_object_dict()
        return json.dumps(self.object_dict)


class NetMessagePackage(MyBaseObject):
    def __init__(self):
        self.__src_ip = None
        self.__src_port = None
        self.__dst_ip = None
        self.__dst_port = None
        self.__id = uuid.uuid1()
        self.__message = None
        MyBaseObject.__init__(self)

    def set_object_by_dict(self, l_object_dict):
        self.__src_ip = l_object_dict["src_ip"]
        self.__src_port = l_object_dict["src_port"]
        self.__dst_ip = l_object_dict["dst_ip"]
        self.__dst_port = l_object_dict["dst_port"]
        self.__id = l_object_dict["id"]
        self.__message = l_object_dict["message"]
        self.__gen_object_dict()

    def __gen_object_dict(self):
        self.object_dict = {"id": self.__id,
                            "src_ip": self.__src_ip,
                            "src_port": self.__src_port,
                            "dst_ip": self.__dst_ip,
                            "dst_port": self.__dst_port,
                            "message": self.__message
                            }

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, l_value):
        self.__id = l_value
        self.get_object_dict()

    @property
    def src_ip(self):
        return self.__src_ip

    @src_ip.setter
    def src_ip(self, l_value):
        self.__src_ip = l_value
        self.__gen_object_dict()

    @property
    def src_port(self):
        return self.__src_port

    @src_port.setter
    def src_port(self, l_value):
        self.__src_port = l_value
        self.__gen_object_dict()

    @property
    def dst_ip(self):
        return self.__dst_ip

    @dst_ip.setter
    def dst_ip(self, l_value):
        self.__dst_ip = l_value
        self.__gen_object_dict()

    @property
    def dst_port(self):
        return self.__dst_port

    @dst_port.setter
    def dst_port(self, l_value):
        self.__dst_port = l_value
        self.__gen_object_dict()

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, l_value):
        self.__message = l_value
        self.__gen_object_dict()



class TaskMessageObject(MyBaseObject):
    def __init__(self):
        self.message_type = None
        self.message_id = uuid.uuid1()
        self.dst_ip = None
        self.dst_port = None
        self.src_ip = None
        self.src_port = None
        self.message_body = None

        self.import_info = None
        self.import_package = None
        self.import_file = None
        self.import_class = None

        self.func_info = None
        self.func_name = None
        self.func_argvs = None
        self.func_timeout = 1800

        self.result_info = None
        self.result_id = None
        self.result_code = None
        self.result_body = None
        MyBaseObject.__init__(self)

    def set_object_by_dict(self, l_object_dict):
        self.message_type = l_object_dict["message_type"]
        self.message_id = l_object_dict["message_id"]
        self.dst_ip = l_object_dict["dst_ip"]
        self.dst_port = l_object_dict["dst_port"]
        self.src_port = l_object_dict["src_port"]
        self.src_ip = l_object_dict["src_ip"]
        self.message_body = l_object_dict["message_body"]
        if "import_info" not in self.message_body.keys():
            self.import_package = None
            self.import_file = None
            self.import_class = None
        else:
            l_import_info = self.message_body["import_info"]
            if "import_package" in l_import_info.keys():
                self.import_package = l_import_info["import_package"]
            if "import_file" in l_import_info.keys():
                self.import_file = l_import_info["import_file"]
            if "import_class" in l_import_info.keys():
                self.import_class = l_import_info["import_class"]
        if "func_info" not in self.message_body.keys():
            self.func_name = None
            self.func_argvs = None
        else:
            l_func_info = self.message_body["func_info"]
            if "func_name" in l_func_info.keys():
                self.func_name = l_func_info["func_name"]
            if "func_argvs" in l_func_info.keys():
                self.func_argvs = l_func_info["func_argvs"]
            if "func_timeout" in l_func_info["func_timeout"]:
                self.func_timeout = l_func_info["func_timeout"]
        if "result_info" not in self.message_body.keys():
            self.result_id = None
            self.result_code = None
            self.result_body = None
        else:
            l_func_result = self.message_body["result_info"]
            if "result_id" in l_func_result.keys():
                self.result_id = l_func_result["result_id"]
            if "result_code" in l_func_result.keys():
                self.result_code = l_func_result["result_code"]
            if "result_body" in l_func_result.keys():
                self.result_body = l_func_result["result_body"]
        self.__gen_object_dict()

    def __gen_object_dict(self):
        self.result_info = {"result_code": self.result_code,
                            "result_body": self.result_body,
                            "result_id": self.result_id}
        self.import_info = {"import_package": self.import_package,
                            "import_file": self.import_file,
                            "import_class": self.import_class,
                            }
        self.func_info = {"func_name": self.func_name,
                          "func_argvs": self.func_argvs,
                          "func_timeout": self.func_timeout}
        self.message_body = {"import_info": self.import_info,
                             "func_info": self.func_info,
                             "result_info": self.result_info
                             }
        self.object_dict = {"message_type": self.message_type,
                            "message_id": self.message_id,
                            "dst_ip": self.dst_ip,
                            "dst_port": self.dst_port,
                            "src_ip": self.src_ip,
                            "src_port": self.src_port,
                            "message_body": self.message_body
                            }


class TaskObject:
    def __init__(self, l_message_obj):
        self.task_id = uuid.uuid1()
        self.task_status = TaskStatus.READY
        self.message_id = l_message_obj.message_id
        self.task_timeout = l_message_obj.func_timeout
        self.task_info = l_message_obj
        self.task_type = l_message_obj.message_type
        self.result_message = TaskMessageObject()
        self.result_message.message_id = self.message_id
        self.result_message.message_type = MessageType.CMD
        self.result_message.dst_ip = l_message_obj.src_ip
        self.result_message.dst_port = l_message_obj.src_port

    def set_task_result(self, result_code, result_body):
        self.result_message.result_code = result_code
        self.result_message.result_id = self.message_id
        self.result_message.result_body = result_body

    def get_task_result_message_obj(self):
        return self.result_message


class ModuleInfo(MyBaseObject):
    def __init__(self, l_module_path=None, l_module_name=None, l_process_name=None, l_args=None):
        self.module_path = l_module_path
        self.module_name = l_module_name
        self.process_name = l_process_name
        self.module_args = l_args
        self.registration_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        MyBaseObject.__init__(self)

    def __gen_object_dict(self):
        self.object_dict = {"module_path": self.module_path,
                            "module_name": self.module_name,
                            "process_name": self.process_name,
                            "module_args": self.module_args,
                            "registration_time": self.registration_time}

    def set_object_by_dict(self, l_object_dict):
        self.module_path = l_object_dict["module_path"]
        self.module_name = l_object_dict["module_name"]
        self.process_name = l_object_dict["process_name"]
        self.module_args = l_object_dict["module_args"]
        self.registration_time = l_object_dict["registration_time"]
        self.__gen_object_dict()


class ProcessStatus(MyBaseObject):
    def __init__(self, l_process_name=None, l_process_status=None):
        self.process_name = l_process_name
        self.process_status = l_process_status
        self.set_status_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        MyBaseObject.__init__(self)

    def __gen_object_dict(self):
        self.object_dict = {"process_name": self.process_name,
                            "process_status": self.process_status,
                            "set_status_time": self.set_status_time}

    def set_object_by_dict(self, l_object_dict):
        self.process_name = l_object_dict["process_name"]
        self.process_status = l_object_dict["process_status"]
        self.set_status_time = l_object_dict["set_status_time"]
        self.__gen_object_dict()


class AgentInfoObject(MyBaseObject):
    def __init__(self, l_agent_type, l_agent_ip=None, l_agent_port=12345, l_os_login_info=None):
        self.agent_type = l_agent_type
        self.agent_ip = l_agent_ip
        self.agent_port = l_agent_port
        self.agent_status = None
        self.login_ip = l_os_login_info["ip"]
        self.login_port = l_os_login_info["port"]
        self.login_user = l_os_login_info["user"]
        self.login_user_password = l_os_login_info["user_password"]
        self.admin_password = l_os_login_info["admin_password"]
        self.key_auth_file = l_os_login_info["key_auth_file"]
        self.key_file_password = l_os_login_info["key_file_password"]
        self.login_info = None
        MyBaseObject.__init__(self)

    def __gen_object_dict(self):
        self.login_info = {"login_ip": self.login_ip,
                           "login_port": self.login_port,
                           "login_user": self.login_user,
                           "login_user_password": self.login_user_password,
                           "admin_password": self.admin_password,
                           "key_auth_file": self.key_auth_file,
                           "key_file_password": self.key_file_password
                           }
        self.object_dict = {"agent_ip": self.agent_ip,
                            "agent_port": self.agent_port,
                            "agent_type": self.agent_type,
                            "agent_status": self.agent_status,
                            "login_info": self.login_info
                            }

    def set_object_by_dict(self, l_object_dict):
        self.agent_ip = l_object_dict["agent_ip"]
        self.agent_port = l_object_dict["agent_port"]
        self.agent_status = l_object_dict["agent_status"]
        self.agent_type = l_object_dict["agent_type"]
        if "login_info" in l_object_dict.keys():
            l_os_login_info = l_object_dict["login_info"]
            self.login_ip = l_os_login_info["ip"]
            self.login_port = l_os_login_info["port"]
            self.login_user = l_os_login_info["user"]
            self.login_user_password = l_os_login_info["user_password"]
            self.admin_password = l_os_login_info["admin_password"]
            self.key_auth_file = l_os_login_info["key_auth_file"]
            self.key_file_password = l_os_login_info["key_file_password"]
        self.__gen_object_dict()
