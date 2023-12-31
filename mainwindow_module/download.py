import os
from PyQt5.QtCore import QRunnable, pyqtSignal, QObject, QThreadPool
from PyQt5.QtWidgets import QAbstractItemView, QDialog, QVBoxLayout, QListWidget, QPushButton, QFileDialog, QMessageBox, \
    QTextEdit
import requests

from pdf_module.merge import merge_images_to_pdf


class DownloadSignals(QObject):
    download_result = pyqtSignal(tuple, bool)  # 修改信号定义，接受一个元组和一个布尔值

class DownloadTask(QRunnable):
    def __init__(self, image_data, save_directory):
        super().__init__()
        self.image_data = image_data
        self.save_directory = save_directory
        self.signals = DownloadSignals()

    def run(self):
        image_id, extension, file_name, boookmark= self.image_data
        url = f"https://picshack.net/ib/download/{image_id}"
        response = requests.get(url)
        success = False
        if response.status_code == 200:
            file_path = os.path.join(self.save_directory, f"{file_name}.{extension}")
            with open(file_path, 'wb') as file:
                file.write(response.content)
                success = True
            self.signals.download_result.emit(self.image_data, success)  # 注意这里传递整个 image_data

class DownloadManager:
    MAX_CONCURRENT_DOWNLOADS = 10  # 最大支持同时下载的文件数

    def __init__(self, main_window, image_browser):
        self.main_window = main_window
        self.image_browser = image_browser
        self.thread_pool = QThreadPool()
        self.thread_pool.setMaxThreadCount(self.MAX_CONCURRENT_DOWNLOADS)
        self.successful_downloads = []  # 初始化成功下载的文件列表
        self.failed_downloads = []  # 初始化失败下载的文件列表

    def download_images(self):
        dialog = QDialog(self.main_window)
        dialog.setWindowTitle("选择要下载的图像")
        image_names = self.image_browser.get_image_names()
        layout = QVBoxLayout()
        list_widget = QListWidget()
        list_widget.addItems(image_names)
        list_widget.setSelectionMode(QAbstractItemView.MultiSelection)
        layout.addWidget(list_widget)

        # 创建全选按钮并连接到自定义槽函数
        select_all_button = QPushButton("全选/取消全选")
        select_all_button.clicked.connect(lambda: self.toggle_select_all(list_widget))
        layout.addWidget(select_all_button)

        confirm_button = QPushButton("确定")
        confirm_button.clicked.connect(dialog.accept)
        layout.addWidget(confirm_button)
        dialog.setLayout(layout)
        dialog.resize(700, 500)

        if dialog.exec_():
            selected_images = [self.image_browser.get_image_data_by_name(item.text()) for item in
                               list_widget.selectedItems()]
            self.save_directory = QFileDialog.getExistingDirectory(self.main_window, "选择保存目录")

            self.successful_downloads = []
            self.failed_downloads = []
            self.remaining_downloads = len(selected_images)

            for image_data in selected_images:
                download_task = DownloadTask(image_data, self.save_directory)
                download_task.signals.download_result.connect(self.on_download_result)
                self.thread_pool.start(download_task)

    def on_download_result(self, image_data, success):
        if success:
            self.successful_downloads.append(image_data)
        else:
            self.failed_downloads.append(image_data)
        self.remaining_downloads -= 1

        if self.remaining_downloads == 0:
            if self.failed_downloads:
                self.show_failed_downloads()
            else:
                QMessageBox.information(self.main_window, "下载成功", "全部下载成功!")
                reply = QMessageBox.question(self.main_window, '合并为PDF?', "是否将下载的图片合并为PDF文件?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    downloaded_files = [f"{item[2]}.{item[1]}" for item in self.successful_downloads]  # 注意顺序
                    merge_images_to_pdf(self.save_directory, downloaded_files, self.image_browser.file_path)

    def toggle_select_all(self, list_widget):
        # 根据当前选择状态切换全选/全不选
        if list_widget.count() != len(list_widget.selectedItems()):
            list_widget.selectAll()
        else:
            list_widget.clearSelection()

    # 下载失败的情况
    def show_failed_downloads(self):
        dialog = QDialog(self.main_window)
        dialog.setWindowTitle("下载失败")
        layout = QVBoxLayout()
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        failure_messages = [f"{file_name} - {error_message}" for file_name, error_message in self.failed_downloads]
        text_edit.setText("\n".join(failure_messages))
        layout.addWidget(text_edit)
        button = QPushButton("确定")
        button.clicked.connect(dialog.accept)
        layout.addWidget(button)
        dialog.setLayout(layout)
        dialog.exec_()
