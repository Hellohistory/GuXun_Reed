import os

import requests
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox


class DownloadThread(QThread):
    download_progress = pyqtSignal(str, int)  # Signal to report individual file download progress
    download_complete = pyqtSignal(list, list)  # Signal to report all files download completion

    def __init__(self, image_browser, selected_images, save_directory):
        super().__init__()
        self.image_browser = image_browser
        self.selected_images = selected_images
        self.save_directory = save_directory

    def run(self):
        successful_downloads = []
        failed_downloads = []
        for idx, image_name in enumerate(self.selected_images):
            image_data = self.image_browser.get_image_data_by_name(image_name)
            image_id, extension, file_name = image_data
            url = f"https://picshack.net/ib/download/{image_id}"
            response = requests.get(url)
            if response.status_code == 200:
                file_path = os.path.join(self.save_directory, f"{file_name}.{extension}")
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                successful_downloads.append(file_name)
            else:
                failed_downloads.append(file_name)
            self.download_progress.emit(image_name, idx + 1)  # Emit progress signal

        self.download_complete.emit(successful_downloads, failed_downloads)  # Emit completion signal


class DownloadManager:
    def __init__(self, main_window, image_browser):
        self.main_window = main_window
        self.image_browser = image_browser

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
            selected_images = [item.text() for item in list_widget.selectedItems()]
            save_directory = QFileDialog.getExistingDirectory(self.main_window, "选择保存目录")

            # Create and configure the download thread
            self.download_thread = DownloadThread(self.image_browser, selected_images, save_directory)
            self.download_thread.download_progress.connect(self.on_download_progress)
            self.download_thread.download_complete.connect(self.on_download_complete)
            self.download_thread.start()
        else:
            QMessageBox.warning(self.main_window, "取消下载", "下载已取消")

    def on_download_progress(self, image_name, idx):
        # You can update a progress bar or status message here
        pass

    def on_download_complete(self, successful_downloads, failed_downloads):
        if successful_downloads:
            success_message = "\\n".join(successful_downloads)
            QMessageBox.information(self.main_window, "下载成功",
                                    f"以下图像已成功下载:\\n{success_message}")
        if failed_downloads:
            failure_message = "\\n".join(failed_downloads)
            QMessageBox.warning(self.main_window, "下载失败",
                                f"以下图像下载失败，请稍后重试:\\n{failure_message}")
