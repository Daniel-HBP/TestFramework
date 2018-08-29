# -*- coding:utf-8 -*-
# !/usr/bin/env python

__author__ = 'daniel hong'







def get_service_import_module(l_message_obj):
    """

    :type l_message_obj: TaskMessageObject
    """
    if l_message_obj.import_package is None:
        l_module_to_import = "ToolAgent.AgentLib"
    else:
        l_module_to_import = l_message_obj.import_package
    if l_message_obj.import_file is not None:
        l_module_to_import = l_module_to_import + "." + l_message_obj.import_file
    else:
        l_module_to_import = l_module_to_import + "." + "service_cmd_lib"
    return l_module_to_import


def import_need_module(l_message_obj):
    """

    :type l_message_obj: TaskMessageObject
    """
    try:
        l_module_name = get_service_import_module(l_message_obj)
        if l_module_name not in sys.modules.keys():
            l_module = importlib.import_module(l_module_name)
        else:
            l_module = sys.modules[l_module_name]
    except Exception as e:
        agent_log.error(e)
        raise e
    try:
        if l_message_obj.import_class is not None:
            l_temp_class = getattr(l_module, l_message_obj.import_class)
            l_temp_obj = l_temp_class()
            l_cmd_func = getattr(l_temp_obj, l_message_obj.func_name)
        else:
            l_cmd_func = getattr(l_module, l_message_obj.func_name)
        return l_cmd_func
    except Exception as e:
        raise e


def run_cmd(l_temp_task):
    """

    :type l_temp_task: TaskObject
    """
    try:
        l_func_cmd = import_need_module(l_temp_task.task_info)
    except Exception as e:
        raise e
    try:
        l_result = l_func_cmd(l_temp_task.task_info.func_argvs)
    except Exception as e:
        l_temp_task.set_task_result(G_CONSTANT_RESULT_ERROR, {"result": False, "body": e.message})
        raise e
    l_temp_task.set_task_result(G_CONSTANT_RESULT_NORMAL, l_result)


def run_manage(l_temp_task):
    """

    :type l_temp_task: TaskObject
    """
    pass


def run_report_process(l_temp_task):
    """

    :type l_temp_task: TaskObject
    """
    pass