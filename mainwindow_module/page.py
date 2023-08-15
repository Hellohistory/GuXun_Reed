from image_browser import ImageBrowser


class PageController:
    def __init__(self, main_window, image_browser: ImageBrowser):
        self.main_window = main_window
        self.image_browser = image_browser

    def update_content(self):
        scale_option = self.main_window.scale_selector.currentText()
        scale = scale_option if "%" in scale_option else "100%"

        # 根据翻页方向选择HTML内容生成方式
        if self.image_browser.get_page_direction() == "左右":
            html_content = self.image_browser.create_html_content(scale=scale)
        else:
            html_content = self.image_browser.create_vertical_html_content(scale=scale)

        self.main_window.view.setHtml(html_content)
        self.main_window.status_bar.showMessage(
            f"页面 {self.image_browser.get_current_index() + 1} / {self.image_browser.get_total_pages()}")

    def change_page_direction(self, direction):
        self.image_browser.set_page_direction(direction)
        self.update_content()

    def navigate_page(self, direction):
        self.image_browser.navigate_page(direction)
        self.update_content()

    def jump_to_page(self, index):
        self.image_browser.jump_to_page(index)
        self.update_content()
