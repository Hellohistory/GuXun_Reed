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

        self.image_browser.bookmarks_modified = True

        # 保存书签到原始文件路径
        self.image_browser.save_bookmarks(self.image_browser.file_path)

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
            # 使用列表控件中的行索引来确定要重命名的书签的索引
            index = self.bookmark_list.row(item)
            image_id, _, _, _ = self.image_browser.image_data[index]

            # 使用ImageBrowser类的edit_bookmark方法来编辑书签
            self.image_browser.edit_bookmark(image_id, new_name)

            # 更新列表控件中的项
            item.setText(new_name)

            # 保存书签到原始文件路径
            self.image_browser.save_bookmarks(self.image_browser.file_path)

            # 设置文件已更改标记
            self.image_browser.file_changed = True

    def delete_bookmark(self, item):
        bookmark_name = item.text()
        image_id = None
        for img_id, _, _, bm_name in self.image_browser.image_data:
            if bm_name == bookmark_name:
                image_id = img_id
                break

        if image_id is not None:
            self.image_browser.remove_bookmark(image_id)
            self.update_bookmark_list()
            # 设置书签已更改标记
            self.image_browser.bookmarks_modified = True
        else:
            print("Bookmark not found!")

    def update_bookmark_list(self):
        self.bookmark_list.clear()
        for _, _, _, bookmark_name in self.image_browser.image_data:
            if bookmark_name:  # 只添加非空书签
                item = QListWidgetItem(bookmark_name)
                self.bookmark_list.addItem(item)

    def jump_to_bookmark(self):
        selected_item = self.bookmark_list.currentItem()
        if selected_item:
            bookmark_name = selected_item.text()
            for img_id, _, _, name in self.image_browser.image_data:
                if name == bookmark_name:
                    self.image_browser.jump_to_image_id(img_id)
                    self.main_window.page_controller.update_content()  # 调用PageController的update_content方法
                    break

    def save_changes(self, main_window):
        # 检查书签是否被修改
        if self.image_browser.bookmarks_modified:
            msg_box = QMessageBox(main_window)
            msg_box.setText("您要保存对书签的更改吗？")

            yes_button = msg_box.addButton("是", QMessageBox.YesRole)
            no_button = msg_box.addButton("否", QMessageBox.NoRole)

            msg_box.setDefaultButton(yes_button)

            result = msg_box.exec_()

            if msg_box.clickedButton() == yes_button:
                # 用户点击了"是"按钮
                self.image_browser.save_bookmarks(self.image_browser.file_path)
                self.image_browser.bookmarks_modified = False  # 重置标志
            else:
                # 用户点击了"否"按钮
                new_file_path = self.image_browser.file_path.replace('.json', '_bookmark.json')
                self.image_browser.save_bookmarks(new_file_path)
                self.image_browser.bookmarks_modified = False  # 重置标志
