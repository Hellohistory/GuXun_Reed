import os
import sys
from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow
from image_browser import ImageBrowser

def resource_path(relative_path):
    """ 获取绝对路径以使程序找到打包后的文件 """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def main():
    # 获取示例.json的绝对路径
    file_path = resource_path('测试文件.json')

    # 创建图像浏览器实例
    image_browser = ImageBrowser(file_path=file_path)

    # 如果有默认文件，可以在此加载
    image_browser.load_new_file(file_path)  # 可选择加载默认文件

    # 创建窗口
    app = QApplication(sys.argv)
    window = MainWindow(image_browser)

    # 显示窗口
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
