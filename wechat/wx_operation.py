# -*- coding: utf-8 -*-
# @Author : Frica01, jayz
# 在原作者Frica01的基础上修改，结合pyside6

"""微信群发消息"""

import os
import sys
import subprocess
import time
import csv

import uiautomation as auto
import win32con
import win32gui

from PySide6.QtCore import QObject, Signal, Slot, QMutex, QRunnable
import traceback
import wechat.utils as utils

auto.SetGlobalSearchTimeout(3)


class WxSignals(QObject):
    """
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    progress
        int indicating % progress

    """

    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)
    statusinfo = Signal(str)

    flag = False
    mutex = QMutex()

    def set_flag(self, newflag: bool):
        self.mutex.lock()
        self.flag = newflag
        self.mutex.unlock()

    def get_flag(self) -> bool:
        self.mutex.lock()
        flag = self.flag
        self.mutex.unlock()
        return flag


class WxOperation(QRunnable):
    """
    微信群发消息的类。

    ...

    Attributes:
    ----------
    wx_window: auto.WindowControl
        微信控制窗口
    input_edit: wx_window.EditControl
        聊天界面输入框编辑控制窗口
    search_edit: wx_window.EditControl
        搜索输入框编辑控制窗口

    """

    def __init__(self):
        super(WxOperation, self).__init__()

        self.preparewx()
        self.signals = WxSignals()

    def set_command(self, fn, *args, **kwargs):
        self.signals.set_flag(False)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        # Add the callback to our kwargs
        # self.kwargs['progress_callback'] = self.signals.progress

    @Slot()
    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """

        # Retrieve args/kwargs here; and fire processing using them
        try:

            result = self.fn(*self.args, **self.kwargs)
        except Exception:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done

    def preparewx(self):
        self.__wake_up_window()  # Windows系统层面唤醒微信窗口
        self.wx_window = auto.WindowControl(Name="微信", ClassName="WeChatMainWndForPC")
        # print('hhhhhhhhhhhhee')
        print(self.wx_window.GetChildren())
        assert self.wx_window.Exists(3, 0.5), "窗口不存在"
        # self.input_edit = self.wx_window.EditControl(Name='输入')
        self.search_edit = self.wx_window.EditControl(Name="搜索")

    @staticmethod
    def minimize_wx():
        """结束时候最小化微信窗口"""
        hwnd = win32gui.FindWindow("WeChatMainWndForPC", "微信")
        if win32gui.IsWindowVisible(hwnd):
            # 展示窗口，以下几行代码都可以唤醒窗口
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

    @staticmethod
    def __wake_up_window():
        """唤醒微信窗口"""
        hwnd = win32gui.FindWindow("WeChatMainWndForPC", "微信")
        # 展示窗口
        win32gui.SetForegroundWindow(hwnd)
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWDEFAULT)

    def __get_current_panel_nickname(self) -> str:
        """获取当前面板的好友昵称"""
        for idx in range(1, 10):
            current_panel_nickname = self.wx_window.TextControl(foundIndex=idx).Name
            if current_panel_nickname:
                return current_panel_nickname

    def __goto_chat_box(self, name: str) -> bool:
        """
        跳转到指定 name好友的聊天窗口。

        Args:
            name(str): 必选参数，好友名称

        Returns:
            None
        """
        assert name, "无法跳转到名字为空的聊天窗口"
        self.wx_window.SendKeys(text="{Ctrl}f", waitTime=0.2)
        self.wx_window.SendKeys(text="{Ctrl}a", waitTime=0.1)
        self.wx_window.SendKey(key=auto.SpecialKeyNames["DELETE"])
        auto.SetClipboardText(text=name)
        self.wx_window.SendKeys(text="{Ctrl}v", waitTime=0.1)
        for idx, item in enumerate(
            self.wx_window.ListControl(foundIndex=2).GetChildren()
        ):
            _name = item.Name
            if idx == 0:  # 跳过第一个 标签
                continue
            if _name == "":
                return False
            if _name == name:
                item.Click(waitTime=0.1)
                # self.wx_window.SendKey(key=auto.SpecialKeyNames['ENTER'], waitTime=0.2)
                time.sleep(0.5)
                return True
        return False

    
    def send_text_filetransfer(self, *msgs) -> None:
        """
        发送文本.

        Args:
            input_name(str): 必选参数, 为输入框
            *msgs(Iterable or str): 必选参数，为发送的文本

        Returns:
            None
        """
        for msg in msgs:
            assert msg, "发送的文本内容为空"
            # 捕捉错误, 如果定位不到指定的聊天输入框, 则跳过本次发送 # TODO 添加未处理记录

            # mm = auto.GetClipboardBitmap()
            print(msg)
            try:
                # for idx, item in enumerate(self.wx_window.ListControl(foundIndex=2).GetChildren()):
                #     _name = item.Name
                #     print(_name)
                #     if idx == 0:    # 跳过第一个 标签
                #         continue
                #     if _name == "":
                #         continue
                #     if _name == '文件传输助手':
                #         item.Click(waitTime=0.2)
                #         # self.wx_window.SendKey(key=auto.SpecialKeyNames['ENTER'], waitTime=0.2)
                #         time.sleep(1)

                self.wx_window.ButtonControl(Name="文件传输助手").Click(waitTime=0.2)
                time.sleep(1)
                self.input_edit = self.wx_window.EditControl(Name="文件传输助手")
            except LookupError:
                print("error")
                continue
            self.input_edit.SendKeys(text="{Ctrl}a", waitTime=0.1)
            self.input_edit.SendKey(key=auto.SpecialKeyNames["DELETE"])
            # self.input_edit.SendKeys(text=msg, waitTime=0.1) # 一个个字符插入,不建议使用该方法
            # 设置到剪切板再黏贴到输入框

            auto.SetClipboardText(msg)
            self.input_edit.SendKeys(text="{Ctrl}v", waitTime=0.1)
            self.wx_window.SendKey(key=auto.SpecialKeyNames["ENTER"], waitTime=0.2)

    def __send_file(self, *file_paths) -> None:
        """
        发送文件.

        Args:
            *file_paths(Iterable or str): 必选参数，为文件的路径

        Returns:
            None
        """
        all_path = str()
        for path in file_paths:
            full_path = os.path.abspath(path=path)
            assert os.path.exists(full_path), f"{full_path} 文件路径有误"
            all_path += "'" + full_path + "',"
        args = ["powershell", f"Get-Item {all_path[:-1]} | Set-Clipboard"]
        # 去除console 弹窗
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags = (
            subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW
        )
        startupinfo.wShowWindow = subprocess.SW_HIDE
        subprocess.Popen(args=args, startupinfo=startupinfo)
        time.sleep(0.5)
        self.input_edit.SendKeys(text="{Ctrl}v", waitTime=0.2)
        self.wx_window.SendKey(key=auto.SpecialKeyNames["ENTER"], waitTime=0.2)


    @Slot()
    def print_friend_list(
        self, tag: str = None, csvfile: str = "friends.csv", count: int = 200
    ):
        """
        获取微信好友名称.

        Args:
            tag(str): 可选参数，如不指定，则获取所有好友

        """

        self.signals.statusinfo.emit("开始抓取好友，目标个数：" + str(count))

        def click_tag():
            """点击标签"""
            contacts_management_window.ButtonControl(Name="标签").Click()

        # 点击 通讯录管理

        i = count
        try:
            self.wx_window.ButtonControl(Name="通讯录").Click()
            self.wx_window.ListControl(Name="联系人").ButtonControl(
                Name="通讯录管理"
            ).Click()
            contacts_management_window = (
                auto.GetForegroundControl()
            )  # 切换到通讯录管理，相当于切换到弹出来的页面

            contacts_management_window.ButtonControl(Name="最大化").Click()
        except Exception as ex:
            self.signals.statusinfo.emit("自动操作出错：" + str(ex))
            return

        if tag:
            click_tag()  # 点击标签
            try:
                contacts_management_window.PaneControl(Name=tag).Click()
                time.sleep(0.3)
            except Exception as exp:
                print("find tag ", tag, " error:", str(exp))
                self.signals.statusinfo.emit("查找标签" + tag + "出错：" + str(exp))

            click_tag()  # 关闭标签
        # 获取滑动模式
        scroll = contacts_management_window.ListControl().GetScrollPattern()
        # assert scroll, "没有可滑动对象"

        def grab_from_name_node(name_node: auto.Control, name_list: list):
            try:
                nick_name = name_node.TextControl().Name  # 用户名
                remark_name = name_node.ButtonControl(
                    foundIndex=2
                ).Name  # 用户备注名，索引1会错位，索引2是备注名，索引3是标签名

                nm = remark_name if remark_name else nick_name

                name_node.ButtonControl(Name=nm).Click(x=1, y=1)
                time.sleep(0.2)
                wechat_name = (
                    contacts_management_window.TextControl(Name="微信号：")
                    .GetNextSiblingControl()
                    .Name
                )

                location = ""
                try:
                    # ltc = contacts_management_window.TextControl(Name='地区：')
                    location = (
                        contacts_management_window.TextControl(Name="地区：")
                        .GetNextSiblingControl()
                        .Name
                    )
                except LookupError:
                    print(nm, "没有地区")

                thetag = ""
                try:
                    thetag = (
                        contacts_management_window.TextControl(Name="标签")
                        .GetNextSiblingControl()
                        .Name
                    )
                except LookupError:
                    print(nm, "没有标签")
                print(nm, "标签：", thetag)

                name_list.append(
                    [
                        nick_name,
                        remark_name,
                        wechat_name,
                        location,
                        thetag,
                        "您",
                        "您",
                        "Y",
                    ]
                )
                print([nick_name, remark_name, wechat_name, location, thetag])
                # print('\n')
                auto.SendKey(auto.SpecialKeyNames["ESC"])
            except Exception as ex:
                print("Get entry from name node error", ex)

        name_list = list()
        if not scroll:
            for (
                name_node
            ) in (
                contacts_management_window.ListControl().GetChildren()
            ):  # 获取当前页面的 列表 -> 子节点
                grab_from_name_node(name_node, name_list)
                i = i - 1
                if i <= 0 or self.signals.get_flag():
                    break

        else:
            # rate: int = int(float(102000 / num))  # 根据输入的num计算滑动的步长
            # for pct in range(0, 102000, rate):  # range不支持float，不导入numpy库，采取迂回这的方式
            stillpage = True
            lastnm = ""
            while not self.signals.get_flag() and stillpage:
                # 每次滑动一点点，-1代表不用滑动
                # print("pct:" , pct)
                # scroll.SetScrollPercent(horizontalPercent=-1, verticalPercent=pct / 100000)
                curr_page_nodes = list()
                try:
                    curr_page_nodes = (
                        contacts_management_window.ListControl().GetChildren()
                    )
                except Exception as e:
                    print("Get page node exception", e)
                    return

                for name_node in curr_page_nodes:
                    nick_name = name_node.TextControl().Name  # 用户名
                    remark_name = name_node.ButtonControl(
                        foundIndex=2
                    ).Name  # 用户备注名，索引1会错位，索引2是备注名，索引3是标签名
                    nm = remark_name if remark_name else nick_name
                    if nm == lastnm:
                        stillpage = False
                    else:
                        lastnm = nm
                    break

                if not stillpage:
                    break

                for name_node in curr_page_nodes:  # 获取当前页面的 列表 -> 子节点
                    if self.signals.get_flag():
                        break

                    grab_from_name_node(name_node, name_list)

                    i = i - 1
                    if i <= 0:
                        stillpage = False
                        self.signals.set_flag(True)

                if not self.signals.get_flag():
                    contacts_management_window.ListControl().SendKey(
                        auto.SpecialKeyNames["PAGEDOWN"]
                    )
                    time.sleep(0.2)

        contacts_management_window.SendKey(
            auto.SpecialKeyNames["ESC"]
        )  # 结束时候关闭 "通讯录管理" 窗口
        print(len(name_list))
        with open(csvfile, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["昵称", "备注名", "微信名", "地区", "标签", "称谓", "敬语", "标志"]
            )
            writer.writerows(name_list)

    def get_group_chat_list(self) -> list:
        """获取群聊通讯录中的用户名称"""
        name_list = list()
        auto.ButtonControl(Name="聊天信息").Click()
        time.sleep(0.5)
        chat_members_win = self.wx_window.ListControl(Name="聊天成员")
        if not chat_members_win.Exists():
            return list()
        self.wx_window.ButtonControl(Name="查看更多").Click()
        for item in chat_members_win.GetChildren():
            name_list.append(item.ButtonControl().Name)
        return name_list

    def get_chat_records(self, page: int = 1) -> list:
        """
        获取聊天列表的聊天记录.

        Args:
            page(int): 可选参数，如不指定，只获取1页聊天记录

        Returns:
            list
        """
        chat_records = list()

        def extract_msg() -> None:
            all_msgs = self.wx_window.ListControl(Name="消息").GetChildren()
            for msg_node in all_msgs:
                msg = msg_node.Name
                if not msg:
                    continue
                if msg_node.PaneControl().Name:
                    chat_records.append(
                        {
                            "type": "Time",
                            "name": "System",
                            "msg": msg_node.PaneControl().Name,
                        }
                    )
                    continue
                if "你已添加了" in msg and "现在可以开始聊天了" in msg:
                    chat_records.append(
                        {"type": "System", "name": "System", "msg": msg}
                    )
                    continue
                if msg in [
                    "以下为新消息",
                    "查看更多消息",
                    "该类型文件可能存在安全风险，建议先检查文件安全性后再打开。",
                ]:
                    chat_records.append(
                        {"type": "System", "name": "System", "msg": msg}
                    )
                    continue
                if "撤回了一条消息" in msg or "尝试撤回上一条消息" in msg:
                    chat_records.append(
                        {
                            "type": "Other",
                            "name": "".join(msg.split(" ")[:-1]),
                            "msg": msg.split(" ")[-1],
                        }
                    )
                    continue
                if msg in [
                    "发出红包，请在手机上查看",
                    "收到红包，请在手机上查看",
                    "你发送了一次转账收款提醒，请在手机上查看",
                    "你收到了一次转账收款提醒，请在手机上查看",
                ]:
                    chat_records.append(
                        {"type": "RedEnvelope", "name": "System", "msg": msg}
                    )
                    continue
                if "领取了你的红包" in msg:
                    _ = msg.split("领取了你的红包")
                    chat_records.append(
                        {"type": "RedEnvelope", "name": _[0], "msg": _[1]}
                    )
                    continue
                name = msg_node.ButtonControl(foundIndex=1).Name
                if msg == "[文件]":
                    file_name = msg_node.PaneControl().TextControl(foundIndex=1).Name
                    size = msg_node.PaneControl().TextControl(foundIndex=2).Name
                    chat_records.append(
                        {
                            "type": "File",
                            "name": name,
                            "msg": f"size: {size}  ---  file_name: {file_name}",
                        }
                    )
                    continue
                if msg == "微信转账":
                    operation = msg_node.PaneControl().TextControl(foundIndex=2).Name
                    amount = msg_node.PaneControl().TextControl(foundIndex=3).Name
                    chat_records.append(
                        {
                            "type": "RedEnvelope",
                            "name": name,
                            "msg": msg + f"    {operation}    " + amount,
                        }
                    )
                    continue
                if "引用" in msg and "的消息" in msg:
                    chat_records.append({"type": "Cited", "name": name, "msg": msg})
                    continue
                if msg == "[聊天记录]":
                    if not name:
                        name = msg_node.ButtonControl(foundIndex=2).Name
                chat_records.append({"type": "Content", "name": name, "msg": msg})

        for _ in range(page):
            self.wx_window.WheelUp(wheelTimes=15)
        extract_msg()
        return chat_records

    

    def __send_msg2(
        self, input_name: str, wechatname: str, msg: str, mockit: bool
    ) -> bool:
        try:
            # 如果当前面板已经是需发送好友, 则无需再次搜索跳转
            if self.__get_current_panel_nickname() != input_name:
                if not self.__goto_chat_box(name=input_name):
                    print("昵称不匹配:::", input_name)
                    return False
        except Exception as ex:
            print("搜索好友失败：：：", input_name, str(ex))
            return False

        if self.signals.get_flag():
            return False
        # 获取到真实的昵称（获取当前面板的备注名称）, 有时候好友昵称输入不全, 可以匹配到，但输入发送内容时候会报错
        # name = self.__get_current_panel_nickname()
        #

        try:
            self.input_edit = None
            print("定位聊天编辑控件--->", input_name)
            self.input_edit = self.wx_window.EditControl(Name=input_name)
        except Exception as ex:
            print("定位聊天编辑控件失败：：：", input_name, str(ex))
            return False

        if self.signals.get_flag():
            return False

        try:

            self.input_edit.SendKeys(text="{Ctrl}a", waitTime=0.1)
            self.input_edit.SendKey(key=auto.SpecialKeyNames["DELETE"])
            # self.input_edit.SendKeys(text=msg, waitTime=0.1) # 一个个字符插入,不建议使用该方法
            # 设置到剪切板再黏贴到输入框
            if not mockit:
                auto.SetClipboardText(text=msg)
            else:
                auto.SetClipboardText("")

            self.input_edit.SendKeys(text="{Ctrl}v", waitTime=0.1)

            if self.signals.get_flag():
                return False

            self.wx_window.SendKey(key=auto.SpecialKeyNames["ENTER"], waitTime=0.2)

        except Exception as ex:
            print("发送消息失败：：：", input_name, "消息（", msg, "）", str(ex))
            return False

        return True

    def parse_mgs(self, msg_template, title, you):
        return msg_template.replace("{称谓}", title).replace("{敬语}", you)

    @Slot()
    def process_send_message(self, msg_template: str, csvfile: str, only_log: bool):

        if not msg_template or not msg_template.strip():
            print("Empty message, just return")
            self.signals.statusinfo.emit("发送的消息为空")
            return

        msg_logs = list()

        plan = []
        # 打开CSV文件
        with open(csvfile, mode="r", encoding="utf-8-sig") as file:
            # 创建CSV读取器
            csv_reader = csv.reader(file)
            # 跳过头部
            header = next(csv_reader)
            #'昵称','备注名','微信名','地区','标签','称谓','敬语','标志'
            nickname_idx = header.index("昵称") if "昵称" in header else -1
            namecomment_idx = header.index("备注名") if "备注名" in header else -1
            wechatname_idx = header.index("微信名") if "微信名" in header else -1
            location_idx = header.index("地区") if "地区" in header else -1
            tag_idx = header.index("标签") if "标签" in header else -1
            title_idx = header.index("称谓") if "称谓" in header else -1
            you_idx = header.index("敬语") if "敬语" in header else -1
            mark_idx = header.index("标志") if "标志" in header else -1

            # 初始化行计数器
            row_count = 0
            skip_count = 0
            # 遍历CSV文件中的每一行
            for row in csv_reader:
                # 更新行计数器
                row_count += 1
                row_entry = {}
                if mark_idx > -1 and mark_idx < len(row):
                    # 如果标记为N，就忽略这一行
                    if row[mark_idx] == "N":
                        skip_count += 1
                        print("skip:::", row)
                        continue
                    else:
                        row_entry["mark"] = row[mark_idx]

                if nickname_idx > -1 and nickname_idx < len(row):
                    row_entry["nickname"] = row[nickname_idx]

                if namecomment_idx > -1 and namecomment_idx < len(row):
                    row_entry["namecomment"] = row[namecomment_idx]

                if utils.is_empty_entry(row_entry, "nickname") and utils.is_empty_entry(
                    row_entry, "namecomment"
                ):
                    skip_count += 1
                    print("skip nameless:::", row)
                    continue

                if wechatname_idx > -1 and wechatname_idx < len(row):
                    row_entry["wechatname"] = row[wechatname_idx]

                if location_idx > -1 and location_idx < len(row):
                    row_entry["location"] = row[location_idx]

                if tag_idx > -1 and tag_idx < len(row):
                    row_entry["tag"] = row[tag_idx]

                if title_idx > -1 and title_idx < len(row):
                    row_entry["title"] = row[title_idx]

                if utils.is_empty_entry(row_entry, "title"):
                    row_entry["title"] = "您"

                if you_idx > -1 and you_idx < len(row):
                    row_entry["you"] = row[you_idx]

                if utils.is_empty_entry(row_entry, "you"):
                    row_entry["you"] = "您"

                plan.append(row_entry)

        print("计划处理记录条数：：", len(plan))
        self.signals.statusinfo.emit("处理发送消息，接收人个数：" + str(len(plan)))

        suc_count = 0
        for task in plan:
            if self.signals.get_flag():
                break
            msg = self.parse_mgs(msg_template, task["title"], task["you"])
            input_name = (
                task["namecomment"]
                if not utils.is_empty_entry(task, "namecomment")
                else task["nickname"]
            )

            if self.__send_msg2(input_name, task["wechatname"], msg, only_log):
                msg_logs.append(
                    [
                        task["nickname"] if "nickname" in task else "",
                        task["namecomment"] if "namecomment" in task else "",
                        task["wechatname"] if "wechatname" in task else "",
                        task["location"] if "location" in task else "",
                        task["tag"] if "tag" in task else "",
                        task["title"] if "title" in task else "",
                        task["you"] if "you" in task else "",
                        "D",
                        msg,
                    ]
                )
                suc_count += 1
                self.signals.statusinfo.emit(
                    "处理 " + input_name + " 成功，总共成功" + str(suc_count) + "条"
                )
            else:
                msg_logs.append(
                    [
                        task["nickname"] if "nickname" in task else "",
                        task["namecomment"] if "namecomment" in task else "",
                        task["wechatname"] if "wechatname" in task else "",
                        task["location"] if "location" in task else "",
                        task["tag"] if "tag" in task else "",
                        task["title"] if "title" in task else "",
                        task["you"] if "you" in task else "",
                        "E",
                        msg,
                    ]
                )
                self.signals.statusinfo.emit(
                    "处理 " + input_name + " 失败，总共成功" + str(suc_count) + "条"
                )

        # write logs
        if len(msg_logs) == 0:
            return
        with open(
            file=utils.fmtfn("_log[%Y%m%d-%H%M%S].csv"),
            mode="w",
            newline="",
            encoding="utf-8-sig",
        ) as afile:
            writer = csv.writer(afile)
            writer.writerow(
                [
                    "昵称",
                    "备注名",
                    "微信名",
                    "地区",
                    "标签",
                    "称谓",
                    "敬语",
                    "标志",
                    "已发送信息",
                ]
            )
            writer.writerows(msg_logs)
