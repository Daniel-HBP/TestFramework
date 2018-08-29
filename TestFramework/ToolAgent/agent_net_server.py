# -*- coding:utf-8 -*-
# !/usr/bin/env python

__author__ = 'daniel hong'
from ToolAgent.AgentLib.agent_net_lib import *


def do_recv(conn, src_ip, src_port):
    buff = ""
    while True:
        try:
            data = conn.recv(G_CONSTANT_BUFFER_SIZE)
        except socket.error as e:
            agent_log.error("receive data from %s:%d error. error code: %s, message: %s" % (src_ip, int(src_port), str(e.errno), e.message))
            conn.close()
            raise e
        buff += data
        if buff.endswith(G_CONSTANT_MSG_END_FLG):
            if buff.strip() == G_CONSTANT_MSG_ACK:
                buff = ""
                continue
            buff.replace(G_CONSTANT_MSG_END_FLG, "")
            try:
                l_package_dict = json.loads(buff)
                l_package_obj = NetMessagePackage()
                l_package_obj.set_object_by_dict(l_package_dict)
                put_receive_package_to_queue(l_package_obj)
            except Exception as e:
                agent_log.error("receive data from %s:%d error. message format error. error:%s,  message: %s" % (src_ip, int(src_port), e.message, buff))
            buff = ""
            conn.sendall(G_CONSTANT_MSG_ACK)


def start_server(server_ip, server_port):
    s_ip = server_ip
    s_port = server_port
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except Exception as e:
        agent_log.error(e)
        raise e
    try:
        s.bind((s_ip, s_port))
    except Exception as e:
        agent_log.error(e)
        raise e
    s.listen(G_CONSTANT_MAX_CONNECTIONS)
    while True:
        try:
            conn, addr = s.accept()
        except socket.error as e:
            agent_log.error("error code: %s, message: %s" % (str(e.errno), e.message))
            raise e
        hd = threading.Thread(target=do_recv, args=(conn, str(addr[0]), str(addr[1])))
        hd.setDaemon(True)
        hd.start()


def agent_server():
    s_ip = g_current_ip
    s_port = g_current_port
    hd = threading.Thread(target=start_server, args=(s_ip, s_port))
    hd.setDaemon(True)
    hd.start()
    l_func_name = sys._getframe().f_code.co_name
    agent_log.info("%s start" % l_func_name)
    while True:
        if not hd.is_alive():
            agent_log.error("agent_net_server has exited. now restart")
            hd = threading.Thread(target=start_server, args=(s_ip, s_port))
            hd.setDaemon(True)
            hd.start()
        time.sleep(G_CONSTANT_THREAD_SLEEP)
        if get_process_stop_flg(l_func_name):
            break
    agent_log.info("%s stopped" % l_func_name)


if __name__ == "__main__":
    agent_server()
