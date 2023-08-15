import json

class ImageBrowser:
    def __init__(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = json.load(file)
            self.image_data = [(item['ID'], item['file_extension'], item['file_name']) for item in file_content]
        self.current_index = 0
        self.page_direction = "左右" # 默认翻页方向
        self.images_per_page = 1  # 每页显示的图像数量


        # Initialize the bookmarks dictionary
        self.bookmarks = {}  # Key: image_id, Value: bookmark_name

    def add_bookmark(self, image_id, bookmark_name):
        """Add a new bookmark."""
        self.bookmarks[image_id] = bookmark_name

    def remove_bookmark(self, image_id):
        """Remove a bookmark by image ID."""
        if image_id in self.bookmarks:
            del self.bookmarks[image_id]

    def edit_bookmark(self, image_id, new_bookmark_name):
        """Edit the name of a bookmark."""
        if image_id in self.bookmarks:
            self.bookmarks[image_id] = new_bookmark_name

    def get_bookmarks(self):
        """Return a list of bookmarks."""
        return self.bookmarks.items()

    def jump_to_image_id(self, image_id):
        for index, (img_id, _, _) in enumerate(self.image_data):
            if img_id == image_id:
                self.current_index = index
                break



    def create_html_content(self, scale="100%", preload_count=40):
        image_id, file_extension, _ = self.image_data[self.current_index]
        image_url = f"https://picshack.net/ib/{image_id}.{file_extension}"
        html_content = f"<div style='text-align:center;'><img src='{image_url}' alt='{image_id}' style='width:{scale};'/></div>"


        for i in range(1, preload_count + 1):
            preload_index = self.current_index + i
            if preload_index < len(self.image_data):
                preload_id, preload_extension, _ = self.image_data[preload_index]
                preload_url = f"https://picshack.net/ib/{preload_id}.{preload_extension}"
                html_content += f"<img src='{preload_url}' alt='{preload_id}' style='display:none;'/>"

        return html_content

    def create_vertical_html_content(self, scale="100%"):
        html_content = ""
        for image_id, file_extension, _ in self.image_data:
            image_url = f"https://picshack.net/ib/{image_id}.{file_extension}"
            html_content += f"<div style='text-align:center;'><img src='{image_url}' alt='{image_id}' style='width:{scale};'/></div><br/>"
        return html_content


    def navigate_page(self, direction):
        if direction == '下一页':
            self.current_index = min(self.current_index + self.images_per_page, len(self.image_data) - 1)
        elif direction == '上一页':
            self.current_index = max(self.current_index - self.images_per_page, 0)

    def jump_to_page(self, index):
        if 0 <= index < len(self.image_data):
            self.current_index = index

    def get_image_names(self):
        return [file_name for _, _, file_name in self.image_data]

    def get_current_index(self):
        return self.current_index

    def get_total_pages(self):
        return len(self.image_data)

    def get_page_direction(self):
        return self.page_direction

    def set_page_direction(self, direction):
        self.page_direction = direction

    def load_new_file(self, file_path):
        # 读取新的JSON文件并更新内容
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = json.load(file)
            self.image_data = [(item['ID'], item['file_extension'], item['file_name']) for item in file_content]
        self.current_index = 0

    def get_image_data_by_name(self, image_name):
        for image_data in self.image_data:
            if image_data[2] == image_name:
                return image_data
        return None

    def save_bookmarks(self, file_path):
        """Save bookmarks to a file."""
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(self.bookmarks, file, ensure_ascii=False, indent=4)

    def load_bookmarks(self, file_path):
        """Load bookmarks from a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.bookmarks = json.load(file)
        except FileNotFoundError:
            pass  # Handle the case where the file does not exist