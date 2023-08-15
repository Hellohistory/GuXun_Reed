from PyQt5.QtWidgets import QAction

def add_theme_menu(menubar, self):
    theme_menu = menubar.addMenu('主题')

    light_theme_action = QAction('配置1', self)
    light_theme_action.triggered.connect(lambda: self.change_theme(0))
    theme_menu.addAction(light_theme_action)

    dark_theme_action = QAction('配置2', self)
    dark_theme_action.triggered.connect(lambda: self.change_theme(1))
    theme_menu.addAction(dark_theme_action)

    blue_theme_action = QAction('配置3', self)
    blue_theme_action.triggered.connect(lambda: self.change_theme(2))
    theme_menu.addAction(blue_theme_action)

    bret_theme_action = QAction('配置4', self)
    bret_theme_action.triggered.connect(lambda: self.change_theme(3))
    theme_menu.addAction(bret_theme_action)

    acid_theme_action = QAction('配置5', self)
    acid_theme_action.triggered.connect(lambda: self.change_theme(4))
    theme_menu.addAction(acid_theme_action)
