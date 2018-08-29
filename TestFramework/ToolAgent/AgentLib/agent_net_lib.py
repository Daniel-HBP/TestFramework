# -*- coding:utf-8 -*-
# !/usr/bin/env python

__author__ = 'daniel hong'
from ToolAgent.BaseLib.base_data_lib import *
from ToolAgent.BaseLib.base_object_lib import NetMessagePackage
from ToolAgent.BaseLib.base_log_lib import agent_log
from ToolAgent.BaseLib.base_queue_lib import BaseQueue
import socket
import threading
import json
import time


class BaseNetModule:
    def __init__(self, l_listen_ip, l_listen_port):
        self.__listening_ip = l_listen_ip
        self.__listening_port = l_listen_port
        self.__net_receive_queue = BaseQueue(QueueType.PACKAGE_RECEIVE)
        self.__net_send_queue = BaseQueue(QueueType.PACKAGE_SEND)
        self._server_hd = None
        self._client_hd = None

    def start(self):
        self._server_hd = threading.Thread(target=BaseNetModule.__start_server, args=(self,))
        self._server_hd.setDaemon(True)
        self._server_hd.start()

    def __start_server(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as e:
            agent_log.error(e)
            raise e
        try:
            s.bind((self.__listening_ip, self.__listening_port))
        except Exception as e:
            agent_log.error(e)
            raise e
        s.listen(NetConf.MAX_CONNECTIONS)
        while True:
            try:
                conn, addr = s.accept()
            except socket.error as e:
                agent_log.error("error code: %s, message: %s" % (str(e.errno), e.message))
                raise e
            hd = threading.Thread(target=BaseNetModule.__do_receive, args=(self, conn, str(addr[0]), str(addr[1])))
            hd.setDaemon(True)
            hd.start()

    def __do_receive(self, conn, src_ip, src_port):
        buff = ""
        while True:
            try:
                data = conn.recv(NetConf.BUFFER_SIZE)
            except socket.error as e:
                error_msg = "receive data from %s:%d error. error code: %s, message: %s"
                agent_log.error(error_msg % (src_ip, int(src_port), str(e.errno), e.message))
                conn.close()
                raise e
            buff += data
            if buff.endswith(NetConf.MSG_END_FLG):
                if buff.strip() == NetConf.MSG_ACK:
                    buff = ""
                    continue
                buff.replace(NetConf.MSG_END_FLG, "")
                try:
                    l_package_dict = json.loads(buff)
                    l_package_obj = NetMessagePackage()
                    l_package_obj.set_object_by_dict(l_package_dict)
                    l_package_obj.src_ip = src_ip
                    l_package_obj.src_port = src_port
                    self.__net_receive_queue.append_new_obj(l_package_obj.id, l_package_obj.get_object_str())
                except Exception as e:
                    error_msg = "receive data from %s:%d error. message format error. error:%s,  message: %s"
                    agent_log.error(error_msg % (src_ip, int(src_port), e.message, buff))
                buff = ""
                conn.sendall(NetConf.MSG_ACK)

    def __do_send(self, l_package_obj):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as e:
            agent_log.error(e)
            raise e
        try:
            s.connect((l_package_obj.dst_ip, l_package_obj.dst_port))
        except socket.error as e:
            agent_log.error("error code: %s, message: %s" % (str(e.errno), e.message))
            raise e
        try:
            l_package_str = l_package_obj.get_object_str() + NetConf.MSG_END_FLG
            s.sendall(l_package_str)
        except socket.error as e:
            agent_log.error("error code: %s, message: %s" % (str(e.errno), e.message))
            raise e
        buff = ""
        while True:
            try:
                data = s.recv(NetConf.BUFFER_SIZE)
            except socket.error as e:
                agent_log.error("error code: %s, message: %s" % (str(e.errno), e.message))
                s.close()
                raise e
            buff += data
            if buff.strip() == NetConf.MSG_ACK:
                s.close()
                break

    def put_send_package(self, l_dst_ip, l_dst_port, l_package):
        l_package_obj = NetMessagePackage()
        l_package_obj.src_ip = self.__listening_ip
        l_package_obj.src_port = self.__listening_port
        l_package_obj.dst_ip = l_dst_ip
        l_package_obj.dst_port = l_dst_port
        l_package_obj.message = l_package
        self.__do_send(l_package_obj)
        return l_package_obj.id

    def get_receive_package(self, l_package_id):
        return self.__net_receive_queue.get_obj_by_key(l_package_id)

    def get_receive_package_list(self):
        return self.__net_receive_queue.get_queue_keys()

