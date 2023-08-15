import os

import requests
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox

class DownloadManager:
    def __init__(self, main_window, image_browser):
        self.main_window = main_window
        self.image_browser = image_browser

    def download_images(self):
        # 创建自定义对话框
        dialog = QDialog(self.main_window)  # 使用 self.main_window
        dialog.setWindowTitle("选择要下载的图像")

        # 获取所有图像的名称
        image_names = self.image_browser.get_image_names()

        # 创建自定义对话框，注意这里使用 self.main_window 作为父窗口
        dialog = QDialog(self.main_window)

        # 创建自定义对话框
        dialog = QDialog(self.main_window)  # 使用 self.main_window
        dialog.setWindowTitle("选择要下载的图像")
        layout = QVBoxLayout()

        # 创建列表小部件并添加图像名称
        list_widget = QListWidget()
        list_widget.addItems(image_names)
        list_widget.setSelectionMode(QAbstractItemView.MultiSelection)
        layout.addWidget(list_widget)

        # 创建确定按钮并连接到对话框的接受槽
        button = QPushButton("确定")
        button.clicked.connect(dialog.accept)
        layout.addWidget(button)

        dialog.setLayout(layout)
        dialog.resize(700, 500)

        if dialog.exec_():
            selected_images = [item.text() for item in list_widget.selectedItems()]

            # 获取保存目录
            save_directory = QFileDialog.getExistingDirectory(self.main_window, "选择保存目录")  # 使用 self.main_window

            # 在选择的目录中保存图像
            successful_downloads = []
            failed_downloads = []
            for image_name in selected_images:
                image_data = self.image_browser.get_image_data_by_name(image_name)
                image_id, extension, file_name = image_data
                url = f"https://picshack.net/ib/download/{image_id}"
                response = requests.get(url)
                if response.status_code == 200:
                    file_path = os.path.join(save_directory, f"{file_name}.{extension}")
                    with open(file_path, 'wb') as file:
                        file.write(response.content)
                    successful_downloads.append(file_name)
                else:
                    failed_downloads.append(file_name)

            # 显示一次性的成功和失败消息
            if successful_downloads:
                success_message = "\n".join(successful_downloads)
                QMessageBox.information(self.main_window, "下载成功",
                                        f"以下图像已成功下载:\n{success_message}")  # 使用 self.main_window
            if failed_downloads:
                failure_message = "\n".join(failed_downloads)
                QMessageBox.warning(self.main_window, "下载失败",
                                    f"以下图像下载失败，请稍后重试:\n{failure_message}")  # 使用 self.main_window
        else:
            QMessageBox.warning(self.main_window, "取消下载", "下载已取消")  # 使用 self.main_window