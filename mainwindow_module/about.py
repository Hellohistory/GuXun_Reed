from PyQt5.QtWidgets import QMessageBox

class Aboutme:
    def __init__(self, main_window):
        self.main_window = main_window

    def show_about_dialog(self):
        info_text = (
            "<h2>故尋阅读</h2>"
            "<p>版本: 1.0</p>"
            "<p>作者: Hello history</p>"
            "<p>Gitthub仓库地址: <a href='https://github.com/Hellohistory/Guxun_Reed'>故尋阅读</a></p>"
        )
        QMessageBox.about(self.main_window, "关于故尋阅读", info_text)
