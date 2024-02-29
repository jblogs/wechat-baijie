# -*- coding: utf-8 -*-
# Author:       JayZ
# Date:         2023/11/28 10:37
# Description:

from PySide6.QtCore import QObject, QThreadPool
from wechat.wx_operation import WxOperation


class Worker(QObject):

    def __init__(self):
        try:
            self.threadpool = QThreadPool()
            # self.wx_operation = WxOperation()
        except AssertionError:
            pass

    def reset_WxOperation(self):
        self.wx_operation = WxOperation()

    def send_message(self, msgs, newline_msg, files, friend, add_remark_name, target):
        # 包装 wx_operation 的逻辑
        msgs_list = list()
        if msgs:
            msgs_list = [msg for msg in msgs.split("\n")]
        if newline_msg:
            msgs_list.extend(["\n".join(newline_msg.split("\n"))])
        # 这里可以添加错误处理、日志记录等
        try:
            self.wx_operation.send_msg2(friend, target, msgs=msgs_list)
            # self.wx_operation.send_text_filetransfer('大年初一给您和家人拜年啦，祝虎年大吉，如虎添翼，诸事顺意！[福][福][福][烟花][烟花][烟花]')

            return True
        except Exception as e:
            print(f"{friend}  ==> 发送消息时出现错误: {e}")
            return False

    # def get_tag_friend_list(self, tag: str):
    #     return self.wx_operation.get_friend_list(tag=tag)

    def thread_complete(self):
        print("THREAD COMPLETE!")

    # def set_message(self, text: str):
    #     self.mainwindow.statusBar().showMessage(str)

    def fetch_friend_list(self, tag: str, csvfile: str, count: int):

        self.wx_operation.set_command(
            self.wx_operation.print_friend_list, tag, csvfile, count
        )
        self.wx_operation.signals.finished.connect(self.thread_complete)

        self.threadpool.start(self.wx_operation)
        # self.threadpool.finished.connect(self.handle_worker_finished)

    def send_out_messages_to_friends(
        self, msg: str, csvfile: str, only_log: bool = True
    ):
        self.wx_operation.set_command(
            self.wx_operation.process_send_message, msg, csvfile, only_log
        )
        self.wx_operation.signals.finished.connect(self.thread_complete)

        self.threadpool.start(self.wx_operation)

    def set_stop_flag(self):
        if self.wx_operation:
            print("inform to stop~~~~~~~~~~~~~~~~~")
            self.wx_operation.signals.set_flag(True)
