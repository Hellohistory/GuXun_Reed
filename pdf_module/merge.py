import os
from PIL import Image
from PyQt5.QtWidgets import QMessageBox


def merge_images_to_pdf(save_directory, downloaded_files, json_file_path):
    images = []
    for file_name in downloaded_files:
        image_path = os.path.join(save_directory, file_name)
        img = Image.open(image_path)
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        images.append(img)

    # 从JSON文件路径获取基本文件名，并用作PDF文件名
    json_base_name = os.path.splitext(os.path.basename(json_file_path))[0]
    pdf_path = os.path.join(save_directory, f'{json_base_name}.pdf')
    images[0].save(pdf_path, save_all=True, append_images=images[1:])
    QMessageBox.information(None, "保存成功", f"PDF文件已保存在: {pdf_path}")
