import sys
from ctypes import windll

from PySide6.QtWidgets import QApplication

from view.main_window import MainWindow

try:
    # myapp_id = 'company.product.sub_product.version'
    myapp_id = "jblogs.wechat-bainian.wechat-bainianmain.0227"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myapp_id)
except ImportError:
    pass

if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
