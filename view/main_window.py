# -*- coding: utf-8 -*-

from PySide6.QtCore import QPoint, Qt, QSize
from PySide6.QtWidgets import (
    QMainWindow,
    QGraphicsDropShadowEffect,
    QFileDialog,
    QMessageBox,
)
from PySide6.QtGui import QIcon

from view.Ui_mainwin import Ui_theMainWindow
from work.worker import Worker
import csv
import os
import sys
import wechat.utils


class MainWindow(QMainWindow, Ui_theMainWindow):
    def __init__(self):
        super().__init__()

        # 首先声明所有实例变量
        self.model = Worker()

        # 使用由Qt Designer生成的Ui类初始化UI
        self.setupUi(self)
        self.init_ui()
        self.init_connections()
        self.init_text_edit_style()
        self.init_drag_and_drop()
        self.init_window_position()

        # 置顶窗口
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

    

    #
    def resource_path(self, relative_path: str):
        """
        生成资源文件目录访问路径，确保在main.py运行时和打包成exe运行时都能够访问到资源文件
        Args:
            relative_path (str): 从工作目录（或exe所在目录）开始的资源相对路径，如‘resource\\xx.img’

        Returns:
            str: 结合了实际工作目录，或临时目录（在exe运行下）与资源相对路径的资源文件全路径表示
        """        
        if getattr(sys, 'frozen', False): #是否Bundle Resource
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    

    def init_ui(self):
        icon = QIcon()
        icon.addFile(self.resource_path("resource/teamwork.ico"), QSize(), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)

    def set_graphics_effect(self):
        # 添加阴影
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(30)
        effect.setOffset(0, 0)
        effect.setColor(Qt.gray)
        self.setGraphicsEffect(effect)

    def init_connections(self):
        self.pushButton_webc.clicked.connect(self.on_checkwebc_clicked)

        self.pushButton_fetchfs.clicked.connect(self.on_fetchfs_clicked)
        self.pushButton_stop.clicked.connect(self.on_stop_clicked)
        self.checkBox_usetag.toggled.connect(self.on_usetag_clicked)
        self.pushButton_seltgtcsv.clicked.connect(self.on_seltgtcsv_clicked)

        self.pushButton_wlog.clicked.connect(self.on_wlog_clicked)
        self.pushButton_sendout.clicked.connect(self.on_send_clicked)

    def init_text_edit_style(self):
        self.textEdit_msg.setText(
            "龙腾万里，福禄双全。在这龙年新春开启之时，给{称谓}拜年！[抱拳][抱拳]祝愿{敬语}身体健康，财源广进；事业蒸蒸日上，阖家幸福美满。新年快乐！[福][福][福][烟花][烟花][烟花]"
        )

    def init_drag_and_drop(self):
        self.drag_and_drop_files = list()
        # 可拖拽
        self.setAcceptDrops(True)

    def init_window_position(self):
        self._move = False
        self.m_position = QPoint(0, 0)

    def on_usetag_clicked(self):
        if self.checkBox_usetag.isChecked():
            self.lineEdit_tag.setEnabled(True)
        else:
            self.lineEdit_tag.setEnabled(False)

    def on_seltgtcsv_clicked(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Csv files (*.csv)")

        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            print(selected_files)
            if len(selected_files) > 0:
                if self.check_target_csvfile(str(selected_files[0])):
                    self.lineEdit_tgtcsv.setText(str(selected_files[0]))

    def check_target_csvfile(self, filename: str):
        try:
            with open(filename, "r", newline="", encoding="utf-8-sig") as file:
                csvreader = csv.reader(file)
                header = next(csvreader)
                #'昵称','备注名','微信名','地区','标签','称谓','敬语','标志'
                if "昵称" in header and "备注名" in header and "微信名" in header:
                    return True
                else:
                    self.show_message_box(
                        "格式错误",
                        "csv文件没有包含正确的表头：昵称,备注名,微信名……",
                        level="warning",
                    )
                    return False
        except Exception as e:
            print("读取csv文件异常：", e)
            self.show_message_box("错误🆘", "csv文件读取异常", level="error")
            return False
        return True

    def on_checkwebc_clicked(self):
        try:
            if not self.model:
                self.model = Worker()

            self.model.reset_WxOperation()
            self.model.wx_operation.signals.statusinfo.connect(self.show_status_message)
        except Exception as e:
            print("发生异常:", e)
            self.show_message_box("严重错误🆘", "微信未启动!", level="error")
            return

    def show_status_message(self, text: str):
        self.statusBar().showMessage(text)

    def on_fetchfs_clicked(self):
        try:
            if not self.model:
                self.model = Worker()

            self.model.reset_WxOperation()
            self.model.wx_operation.signals.statusinfo.connect(self.show_status_message)
        except Exception as e:
            print("发生异常:", e)
            self.show_message_box("严重错误🆘", "微信未启动!", level="error")
            return

        csvfile = (
            self.lineEdit_fcsv.text()
            if self.lineEdit_fcsv.text() != ""
            else self.lineEdit_fcsv.placeholderText()
        )
        csvfile = wechat.utils.fmtfn(csvfile)
        self.model.fetch_friend_list(
            tag=self.lineEdit_tag.text() if self.lineEdit_tag.isEnabled() else None,
            csvfile=csvfile,
            count=5,
        )

    def on_stop_clicked(self):
        self.model.set_stop_flag()

    def on_wlog_clicked(self):
        try:
            if not self.model:
                self.model = Worker()

            self.model.reset_WxOperation()
            self.model.wx_operation.signals.statusinfo.connect(self.show_status_message)
        except Exception as e:
            print("发生异常:", e)
            self.show_message_box("严重错误🆘", "微信未启动!", level="error")
            return

        targetfile = self.lineEdit_tgtcsv.text()
        if not self.check_target_csvfile(targetfile):
            return
        msg = self.textEdit_msg.toPlainText()
        self.model.send_out_messages_to_friends(msg, targetfile, True)

    def on_send_clicked(self):
        try:
            if not self.model:
                self.model = Worker()

            self.model.reset_WxOperation()
            self.model.wx_operation.signals.statusinfo.connect(self.show_status_message)
        except Exception as e:
            print("发生异常:", e)
            self.show_message_box("严重错误🆘", "微信未启动!", level="error")
            return

        targetfile = self.lineEdit_tgtcsv.text()
        if not self.check_target_csvfile(targetfile):
            return
        msg = self.textEdit_msg.toPlainText()
        self.model.send_out_messages_to_friends(msg, targetfile, False)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            self.drag_and_drop_files = event.mimeData().urls()
            event.accept()  # 鼠标放开函数事件
            self.select_files()
        else:
            event.ignore()

    # 鼠标点击事件产生
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._move = True
            self.m_position = event.globalPos() - self.pos()
            event.accept()

    # 鼠标移动事件
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self._move:
            self.move(QMouseEvent.globalPos() - self.m_position)
            QMouseEvent.accept()

    # 鼠标释放事件
    def mouseReleaseEvent(self, QMouseEvent):
        self._move = False

    # 在 MainWindow 类中重写 closeEvent 方法
    def closeEvent(self, event):
        # self.controller.minimize_wx()   # 最小化微信
        # self.controller.thread_pool.waitForDone()  # 等待所有线程完成
        event.accept()

    def show_message_box(self, title, message, level="warning"):
        if level == "warning":
            QMessageBox.warning(self, title, message)
        else:
            QMessageBox.critical(self, title, message)
