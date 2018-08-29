# -*- coding:utf-8 -*-
# !/usr/bin/env python

__author__ = 'daniel hong'
from enum import Enum


class ProcessStatus(Enum):
    ERROR = -1
    START = 0
    RUNNING = 1
    STOP = 99


class TaskStatus(Enum):
    READY = 0
    RUNNING = 1
    ERROR = -1
    FINISHED = 2
    REPORTED = 3
    TIMEOUT = 99


class TaskConf(Enum):
    MAX_TASK_LENGTH = 1024


class TaskResult(Enum):
    NORMAL = 0
    ERROR = -1
    TIMEOUT = -2


class MessageType(Enum):
    CMD = 0
    MANAGE = 1
    RESULT = -1


class NetConf(Enum):
    BUFFER_SIZE = 1024
    MSG_END_FLG = "$$$"
    MSG_ACK = "$$$Receive$$$" 
    MAX_CONNECTIONS = 300
    NET_SLEEP_TIME = 1
    NET_RECV_TIMEOUT = 6


class AgentType(Enum):
    WINDOWS = "windows"
    LINUX = "linux"


class QueueType(Enum):
    PACKAGE_SEND = "PackageSend"
    PACKAGE_RECEIVE = "PackageReceive"
    MESSAGE_SEND = "MessageSend"
    MESSAGE_RECEIVE = "MessageReceive"
    PROCESS_STATUS = "ProcessStatus"
    PROCESS_REGISTRATION = "ProcessRegistration"