import os
from PyQt5.QtCore import QRunnable, pyqtSignal, QObject, QThreadPool
from PyQt5.QtWidgets import QAbstractItemView, QDialog, QVBoxLayout, QListWidget, QPushButton, QFileDialog, QMessageBox
import requests


class DownloadSignals(QObject):
    download_result = pyqtSignal(str, bool)  # Signal to report individual file download result


class DownloadTask(QRunnable):
    def __init__(self, image_data, save_directory):
        super().__init__()
        self.image_data = image_data
        self.save_directory = save_directory
        self.signals = DownloadSignals()

    def run(self):
        image_id, extension, file_name = self.image_data
        url = f"https://picshack.net/ib/download/{image_id}"
        response = requests.get(url)
        success = False
        if response.status_code == 200:
            file_path = os.path.join(self.save_directory, f"{file_name}.{extension}")
            with open(file_path, 'wb') as file:
                file.write(response.content)
            success = True
        self.signals.download_result.emit(file_name, success)  # Emit result signal

class DownloadManager:
    MAX_CONCURRENT_DOWNLOADS = 10  # Maximum number of concurrent downloads

    def __init__(self, main_window, image_browser):
        self.main_window = main_window
        self.image_browser = image_browser
        self.thread_pool = QThreadPool()
        self.thread_pool.setMaxThreadCount(self.MAX_CONCURRENT_DOWNLOADS)

    def download_images(self):
        dialog = QDialog(self.main_window)
        dialog.setWindowTitle("选择要下载的图像")
        image_names = self.image_browser.get_image_names()
        layout = QVBoxLayout()
        list_widget = QListWidget()
        list_widget.addItems(image_names)
        list_widget.setSelectionMode(QAbstractItemView.MultiSelection)
        layout.addWidget(list_widget)
        button = QPushButton("确定")
        button.clicked.connect(dialog.accept)
        layout.addWidget(button)
        dialog.setLayout(layout)
        dialog.resize(700, 500)

        if dialog.exec_():
            selected_images = [self.image_browser.get_image_data_by_name(item.text()) for item in list_widget.selectedItems()]
            save_directory = QFileDialog.getExistingDirectory(self.main_window, "选择保存目录")

            self.successful_downloads = []
            self.failed_downloads = []
            self.remaining_downloads = len(selected_images)

            for image_data in selected_images:
                download_task = DownloadTask(image_data, save_directory)
                download_task.signals.download_result.connect(self.on_download_result)
                self.thread_pool.start(download_task)

    def on_download_result(self, file_name, success):
        if success:
            self.successful_downloads.append(file_name)
        else:
            self.failed_downloads.append(file_name)
        self.remaining_downloads -= 1

        # Report overall download result when all threads are done
        if self.remaining_downloads == 0:
            if self.successful_downloads:
                success_message = "\\n".join(self.successful_downloads)
                QMessageBox.information(self.main_window, "下载成功",
                                        f"以下图像已成功下载:\\n{success_message}")
            if self.failed_downloads:
                failure_message = "\\n".join(self.failed_downloads)
                QMessageBox.warning(self.main_window, "下载失败",
                                    f"以下图像下载失败，请稍后重试:\\n{failure_message}")