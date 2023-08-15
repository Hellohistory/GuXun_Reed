from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QListWidgetItem, QInputDialog, QMenu
from PyQt5.QtWidgets import QMessageBox

class AboutBookmark:
    def __init__(self, main_window, image_browser, bookmark_list, bookmark_panel):
        self.main_window = main_window
        self.image_browser = image_browser
        self.bookmark_list = bookmark_list
        self.bookmark_panel = bookmark_panel

    def add_bookmark(self):
        current_image_id = self.image_browser.image_data[self.image_browser.current_index][0]

        if current_image_id in self.image_browser.bookmarks:
            QMessageBox.warning(self.main_window, "书签错误", "此页面已添加到书签，不能重复添加。")
            return

        next_bookmark_number = len(self.image_browser.bookmarks) + 1
        bookmark_name = f"书签{next_bookmark_number}"

        self.image_browser.add_bookmark(current_image_id, bookmark_name)

        self.update_bookmark_list()
        self.toggle_bookmark_panel()

        bookmark_file_path = "bookmarks.json"
        self.image_browser.save_bookmarks(bookmark_file_path)

    def toggle_bookmark_panel(self):
        if self.bookmark_panel.isVisible():
            self.bookmark_panel.hide()
        else:
            self.bookmark_panel.show()

    def show_bookmark_context_menu(self, position):
        index = self.bookmark_list.indexAt(position)
        selected_item = self.bookmark_list.item(index.row())

        if selected_item:
            context_menu = QMenu(self.main_window)

            rename_action = QAction("重命名", self.main_window)
            rename_action.triggered.connect(lambda: self.rename_bookmark(selected_item))
            context_menu.addAction(rename_action)

            delete_action = QAction("删除", self.main_window)
            delete_action.triggered.connect(lambda: self.delete_bookmark(selected_item))
            context_menu.addAction(delete_action)

            context_menu.exec_(self.bookmark_list.viewport().mapToGlobal(position))

    def rename_bookmark(self, item):
        old_name = item.text()
        new_name, ok = QInputDialog.getText(self.main_window, "重命名书签", "输入新的书签名称:", text=old_name)

        if ok and new_name:
            image_id = [key for key, value in self.image_browser.bookmarks.items() if value == old_name][0]
            self.image_browser.bookmarks[image_id] = new_name

            self.update_bookmark_list()

            bookmark_file_path = "bookmarks.json"
            self.image_browser.save_bookmarks(bookmark_file_path)

    def delete_bookmark(self, item):
        bookmark_name = item.text()
        image_id = [key for key, value in self.image_browser.bookmarks.items() if value == bookmark_name][0]

        del self.image_browser.bookmarks[image_id]

        self.update_bookmark_list()

    def update_bookmark_list(self):
        self.bookmark_list.clear()
        for image_id, bookmark_name in self.image_browser.bookmarks.items():
            item = QListWidgetItem(bookmark_name)
            self.bookmark_list.addItem(item)

    def jump_to_bookmark(self):
        selected_item = self.bookmark_list.currentItem()
        if selected_item:
            bookmark_name = selected_item.text()
            for image_id, name in self.image_browser.get_bookmarks():
                if name == bookmark_name:
                    self.image_browser.jump_to_image_id(image_id)
                    self.main_window.update_content()
                    break