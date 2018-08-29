# -*- coding:utf-8 -*-
# !/usr/bin/env python

__author__ = 'daniel hong'
from ToolAgent.AgentTemp.agent_task_lib import *


g_task_list = {}
g_task_list_lock = thread.allocate_lock()


def execute_func(task_id):
    l_temp_task = g_task_list[task_id]  # type: TaskObject
    l_temp_task.task_status = G_CONSTANT_TASK_RUNNING
    if l_temp_task.task_type == G_CONSTANT_MSG_TYPE_CMD:
        run_cmd(l_temp_task)
    if l_temp_task.task_type == G_CONSTANT_MSG_TYPE_MANAGE:
        run_manage(l_temp_task)
    if l_temp_task.task_type == G_CONSTANT_MSG_TYPE_RESULT:
        run_report_process(l_temp_task)
    l_temp_task.task_status = G_CONSTANT_TASK_FINISHED


def wait_task_finished(hd):
    """

    :type hd: threading.Thread
    """
    while hd.is_alive():
        time.sleep(1)


def add_new_task(l_task_obj):
    global g_task_list
    g_task_list_lock.acquire()
    try:
        l_task_id = l_task_obj.task_id
        g_task_list.update({l_task_obj.task_id: l_task_obj})
    except Exception as e:
        g_task_list_lock.release()
        raise e
    g_task_list_lock.release()
    return l_task_id


def remove_task(l_task_id):
    g_task_list_lock.acquire()
    try:
        l_task_obj = g_task_list.pop(l_task_id)  # type: TaskObject
    except Exception as e:
        g_task_list_lock.release()
        raise e
    g_task_list_lock.release()
    return l_task_obj


def do_task(l_task_obj):
    """

    :type l_task_obj: TaskObject
    """
    l_task_id = add_new_task(l_task_obj)
    hd = threading.Thread(target=execute_func, args=(l_task_id,))
    hd.join(l_task_obj.task_timeout)
    hd.start()
    wait_task_finished(hd)
    l_task_obj = remove_task(l_task_id)
    if l_task_obj.task_status == G_CONSTANT_TASK_RUNNING:
        error_msg = "timeout=%d" % l_task_obj.task_timeout
        l_task_obj.set_task_result(G_CONSTANT_RESULT_TIMEOUT, {"result": False, "body": error_msg})
    send_result(l_task_obj)


def task_manager():
    l_func_name = sys._getframe().f_code.co_name
    agent_log.info("%s start" % l_func_name)
    while True:
        l_message_file_list = g_message_receive_queue.get_queue_keys()
        for item in l_message_file_list:
            l_message_obj = g_message_receive_queue.get_obj_by_key(item)
            l_temp_task_obj = TaskObject(l_message_obj)
            thread.start_new_thread(do_task, (l_temp_task_obj,))
        if get_process_stop_flg(l_func_name):
            break
        time.sleep(G_CONSTANT_THREAD_SLEEP)
    agent_log.info("%s stopped" % l_func_name)


if __name__ == "__main__":
    task_manager()