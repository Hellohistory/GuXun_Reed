import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QComboBox, QMainWindow, QStatusBar, \
    QApplication
from PyQt5.QtWidgets import QSplitter
from PyQt5.QtWidgets import QToolBar, QAction
from PyQt5.QtWidgets import QVBoxLayout, QListWidget, QPushButton

from image_browser import ImageBrowser  # 导入核心逻辑类
from mainwindow_module.about import Aboutme
from mainwindow_module.bookmark import AboutBookmark
from mainwindow_module.theme_menu import add_theme_menu
from mainwindow_module.download_images import DownloadManager
from STYLESHEET import LIGHT_THEME, DARK_THEME, BLUE_THEME, BRET_THEME, ACID_THEME

# 定义QSS样式表
STYLESHEET = LIGHT_THEME # 默认主题

# 创建应用程序并设置样式
app = QApplication(sys.argv)
app.setStyleSheet(STYLESHEET)


class MainWindow(QMainWindow):
    def __init__(self, image_browser):
        super().__init__()
        self.image_browser = image_browser

        # 设置窗口标题
        self.setWindowTitle("故尋阅读")

        # 创建菜单栏
        menubar = self.menuBar()

        # 设置窗口的初始大小
        self.resize(1000, 800)

        # 创建菜单条
        menubar = self.menuBar()

        self.bookmark_list = QListWidget()
        bookmark_file_path = "bookmarks.json"  # 与保存书签时使用的路径相同
        self.image_browser.load_bookmarks(bookmark_file_path)

        # 创建下载管理器实例，并传递当前窗口和 image_browser
        self.download_manager = DownloadManager(self, image_browser)

        # 创建关于对话框管理器实例
        self.about_manager = Aboutme(self)

        # 添加文件菜单
        file_menu = menubar.addMenu('文件')
        open_json_action = QAction('打开 JSON 文件', self)
        open_json_action.triggered.connect(self.select_json_file)
        file_menu.addAction(open_json_action)

        # 调用添加主题菜单的函数
        add_theme_menu(menubar, self)

        # 添加下载操作
        download_action = QAction('下载', self)
        download_action.triggered.connect(self.download_manager.download_images)  # 注意这里的修改
        file_menu.addAction(download_action)

        # 添加帮助菜单（如之前所示）
        help_menu = menubar.addMenu('帮助')
        about_action = QAction('关于', self)
        about_action.triggered.connect(self.about_manager.show_about_dialog)  # 使用 about_manager
        help_menu.addAction(about_action)

        # 创建工具栏
        self.toolbar = QToolBar("工具栏")
        self.addToolBar(self.toolbar)

        # 创建左右翻页按钮
        left_right_page_action = QAction("左右翻页", self)
        left_right_page_action.triggered.connect(lambda: self.change_page_direction('左右'))
        self.toolbar.addAction(left_right_page_action)

        # 创建上下翻页按钮
        up_down_page_action = QAction("上下翻页", self)
        up_down_page_action.triggered.connect(lambda: self.change_page_direction('上下'))
        self.toolbar.addAction(up_down_page_action)


        # 添加显示/隐藏选择栏的操作
        toggle_action = QAction("显示/隐藏选择栏", self)
        toggle_action.triggered.connect(self.toggle_page_selector)
        self.toolbar.addAction(toggle_action)


        # 创建中央小部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建左侧选择栏
        self.left_v_layout = QVBoxLayout()
        self.page_list = QListWidget() # 使用 QListWidget 替代 QComboBox
        self.left_v_layout = QVBoxLayout()
        self.page_list = QListWidget() # 使用 QListWidget 替代 QComboBox
        self.page_list.addItems(self.image_browser.get_image_names())
        self.page_list.currentRowChanged.connect(self.jump_to_page)
        self.left_v_layout.addWidget(self.page_list)

        # 创建右侧垂直布局
        right_v_layout = QVBoxLayout()
        top_h_layout = QHBoxLayout()
        prev_button = QPushButton("上一页")
        next_button = QPushButton("下一页")
        prev_button.clicked.connect(lambda: self.navigate_page('上一页'))
        next_button.clicked.connect(lambda: self.navigate_page('下一页'))
        self.scale_selector = QComboBox()
        self.scale_selector.addItems(["50%", "75%", "100%", "200%", "400%", "根据宽度", "根据长度", "实际比例"])
        self.scale_selector.currentIndexChanged.connect(self.update_content)

        # 删除此处的翻页方向选择器
        top_h_layout.addWidget(prev_button)
        top_h_layout.addWidget(self.scale_selector)
        top_h_layout.addWidget(next_button)
        self.view = QWebEngineView()
        right_v_layout.addLayout(top_h_layout)
        right_v_layout.addWidget(self.view)

        # 创建左侧和右侧的容器小部件
        left_widget = QWidget()
        left_widget.setLayout(self.left_v_layout)
        right_widget = QWidget()
        right_widget.setLayout(right_v_layout)

        # 使用QSplitter分隔左侧和右侧
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(1, 4)

        main_layout = QVBoxLayout()
        main_layout.addWidget(splitter)
        central_widget.setLayout(main_layout)

        # 创建状态栏并设置在窗口底部
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.setWindowIcon(QIcon('logo.png'))

        # 创建书签面板 (QDockWidget)
        self.bookmark_panel = QDockWidget('书签', self)

        # 将列表添加到书签面板中
        self.bookmark_panel.setWidget(self.bookmark_list)

        # 将书签面板添加到主窗口的右侧
        self.addDockWidget(Qt.RightDockWidgetArea, self.bookmark_panel)

        # 创建书签管理器实例，并传递当前窗口和 image_browser
        self.about_bookmark = AboutBookmark(self, image_browser, self.bookmark_list, self.bookmark_panel)

        # 为书签列表添加右键菜单
        self.bookmark_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.bookmark_list.customContextMenuRequested.connect(self.about_bookmark.show_bookmark_context_menu)

        # 创建书签动作
        bookmark_action = QAction('书签', self)
        bookmark_action.triggered.connect(self.about_bookmark.toggle_bookmark_panel) # 修改为新的方法

        # 添加书签操作
        add_bookmark_action = QAction('添加书签', self)
        add_bookmark_action.triggered.connect(self.about_bookmark.add_bookmark) # 修改为新的方法
        self.toolbar.addAction(add_bookmark_action)

        self.about_bookmark.update_bookmark_list()  # 更新UI中的书签列表

        # 将书签动作添加到工具栏
        self.toolbar.addAction(bookmark_action)

        self.bookmark_list.itemClicked.connect(self.about_bookmark.jump_to_bookmark)

        # 将焦点设置到左侧选择栏的列表小部件上
        self.page_list.setFocus()

        # 初始时隐藏书签面板
        self.bookmark_panel.hide()

        # 加载初始内容
        self.update_content()

    def navigate_page(self, direction):
        self.image_browser.navigate_page(direction)
        self.update_content()

    def jump_to_page(self, index):
        self.image_browser.jump_to_page(index)
        self.update_content()

    def change_theme(self, index):
        themes = [LIGHT_THEME, DARK_THEME, BLUE_THEME, BRET_THEME, ACID_THEME]
        selected_theme = themes[index]
        app.setStyleSheet(selected_theme)

    def change_page_direction(self, direction):
        self.image_browser.set_page_direction(direction)
        self.update_content()

    def toggle_page_selector(self):
        left_widget = self.left_v_layout.parentWidget()
        left_widget.setVisible(not left_widget.isVisible())

    def update_content(self):
        scale_option = self.scale_selector.currentText()
        scale = scale_option if "%" in scale_option else "100%"

        # 根据翻页方向选择HTML内容生成方式
        if self.image_browser.get_page_direction() == "左右":
            html_content = self.image_browser.create_html_content(scale=scale)
        else:
            html_content = self.image_browser.create_vertical_html_content(scale=scale)

        self.view.setHtml(html_content)
        self.status_bar.showMessage(
            f"页面 {self.image_browser.get_current_index() + 1} / {self.image_browser.get_total_pages()}")


    def select_json_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "选择JSON文件", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_path:
            self.image_browser.load_new_file(file_path)
            self.page_list.clear()
            self.page_list.addItems(self.image_browser.get_image_names())
            self.update_content()


    def keyPressEvent(self, event):
        current_row = self.page_list.currentRow()
        if event.key() == Qt.Key_Right or event.key() == Qt.Key_Down:
            new_row = min(current_row + 1, self.page_list.count() - 1)
            self.page_list.setCurrentRow(new_row)
            self.jump_to_page(new_row)
        elif event.key() == Qt.Key_Left or event.key() == Qt.Key_Up:
            new_row = max(current_row - 1, 0)
            self.page_list.setCurrentRow(new_row)
            self.jump_to_page(new_row)
        else:
            super().keyPressEvent(event)


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