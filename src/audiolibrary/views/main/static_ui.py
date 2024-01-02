from PyQt6 import QtCore, QtGui, QtWidgets

from audiolibrary.models.main import MenuItem
from audiolibrary.utils.icon import svg_ico
from audiolibrary.views.widgets import WidgetsFactory, Label
from audiolibrary.views.widgets.list import ListItemWidget


class UiMainWindow:
    def setup_ui(
            self,
            main_window: QtWidgets.QWidget,
            widgets_factory: WidgetsFactory,
            version: str,
            app_name: str,
    ):
        main_window.setObjectName("main_window")
        main_window.setWindowTitle(app_name)
        main_window.resize(830, 600)
        main_window.setStyleSheet("""
            QWidget#main_window {
                background-color: $BG1;
            }
            QToolTip {
                background: #D9DBDD;
                border: 1px solid #000000;
                border-radius: 3px;
                color: #000000;
            }
        """.replace("$BG1", widgets_factory.theme.first_background))
        central_layout = QtWidgets.QHBoxLayout(main_window)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)

        # Menu widget
        menu_widget = QtWidgets.QWidget(main_window)
        menu_widget.setObjectName("menu_widget")
        menu_widget.setStyleSheet("""
            QWidget#menu_widget {
                background-color: $BG2;
                border-right: 1px solid $HOVER;
            }
        """.replace(
            "$BG2", widgets_factory.theme.second_background
        ).replace(
            "$HOVER", widgets_factory.theme.hover
        ))
        menu_widget.setFixedWidth(270)
        menu_layout = QtWidgets.QVBoxLayout(menu_widget)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.addWidget(menu_widget)

        # Menu header
        menu_header_widget = QtWidgets.QWidget()
        menu_header_widget.setObjectName("menu_header_widget")
        menu_header_widget.setToolTip(f"{app_name} {version}")
        menu_layout.addWidget(menu_header_widget)

        menu_header_layout = QtWidgets.QHBoxLayout(menu_header_widget)
        menu_header_layout.setContentsMargins(20, 15, 20, 10)

        # Menu header info widget
        info_stub = QtWidgets.QWidget()
        info_stub.setObjectName("menu_header_logo_widget")
        info_stub.setFixedHeight(50)

        menu_header_info_layout = QtWidgets.QHBoxLayout(info_stub)
        menu_header_info_layout.setContentsMargins(0, 0, 0, 0)
        menu_header_info_layout.setSpacing(5)
        menu_header_layout.addWidget(info_stub)

        logo = QtWidgets.QLabel()
        logo.setObjectName("logo")
        logo.setPixmap(main_window.windowIcon().pixmap(QtCore.QSize(64, 64)))
        logo.setScaledContents(True)
        logo.setFixedSize(QtCore.QSize(32, 32))
        menu_header_info_layout.addWidget(logo)

        program_title_layout = QtWidgets.QVBoxLayout()
        program_title_layout.setContentsMargins(4, 3, 0, 3)
        program_title_layout.setSpacing(0)
        menu_header_info_layout.addLayout(program_title_layout)

        title_widget = QtWidgets.QLabel()
        self.title_widget = title_widget
        title_widget.setObjectName("title_widget")
        title_widget.setText(app_name)
        title_widget.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        title_widget.setStyleSheet("""
            QLabel#title_widget {
                font-size: 14px;
                font-weight: 800;
                color: $TEXT_HEADER;
            }
        """.replace(
            "$TEXT_HEADER", widgets_factory.theme.text_header
        ))
        program_title_layout.addWidget(title_widget)

        description_widget = QtWidgets.QLabel()
        self.description_widget = description_widget
        description_widget.setObjectName("description_widget")
        description_widget.setText(version)
        description_widget.setStyleSheet("""
            QLabel#description_widget {
                font-size: 12px;
                font-weight: bold;
                color: $TEXT_SECONDARY;
            }
        """.replace(
            "$TEXT_SECONDARY", widgets_factory.theme.text_secondary
        ))
        program_title_layout.addWidget(description_widget)

        menu_header_layout.addItem(
            QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Fixed)
        )

        # Header Buttons
        signin_button = QtWidgets.QToolButton()
        signin_button.setObjectName("signin_button")
        signin_button.setIcon(QtGui.QIcon(svg_ico("icons:signin.svg", widgets_factory.theme.text_primary)))
        signin_button.setIconSize(QtCore.QSize(32, 32))
        signin_button.setStyleSheet("""
            QToolButton {
                border-radius: 5px;
                background-color: transparent;
            }
            QToolButton:hover {
                background-color: $HOVER;
            }
            QToolButton:pressed {
                background-color: transparent;
            }
                """.replace(
            "$HOVER", widgets_factory.theme.hover
        ))
        self.signin_button = signin_button
        menu_header_info_layout.addWidget(signin_button)

        logout_button = QtWidgets.QToolButton()
        logout_button.setObjectName("logout_button")
        logout_button.setIcon(QtGui.QIcon(svg_ico("icons:logout.svg", widgets_factory.theme.text_primary)))
        logout_button.setIconSize(QtCore.QSize(32, 32))
        logout_button.setStyleSheet(signin_button.styleSheet())
        self.logout_button = logout_button
        menu_header_info_layout.addWidget(logout_button)

        # Menu list
        menu_list_widget = widgets_factory.list()
        menu_list_widget.setObjectName("menu_list_widget")
        menu_list_widget.setIconSize(QtCore.QSize(16, 16))
        menu_list_model = menu_list_widget.model()
        self.menu_select_model = menu_list_widget.selectionModel()

        self.menu_item_browse = ListItemWidget("Menu item 1", MenuItem.BROWSE, "icons:browse.svg")
        self.menu_item_liked = ListItemWidget("Menu item 2", MenuItem.LIKED, "icons:liked.svg")
        self.menu_item_popular = ListItemWidget("Menu item 3", MenuItem.POPULAR, "icons:popular.svg")
        self.menu_item_control = ListItemWidget("Menu item 4", MenuItem.CONTROL, "icons:control.svg")
        self.menu_item_upload = ListItemWidget("Menu item 5", MenuItem.UPLOAD, "icons:upload.svg")

        menu_list_model.appendRow(self.menu_item_browse)
        menu_list_model.appendRow(self.menu_item_liked)
        menu_list_model.appendRow(self.menu_item_popular)
        menu_list_model.appendRow(self.menu_item_control)
        menu_list_model.appendRow(self.menu_item_upload)

        menu_layout.addWidget(menu_list_widget)
        self.menu_list_widget = menu_list_widget

        # Tool section
        menu_tool_layout = QtWidgets.QHBoxLayout()
        menu_settings_button = QtWidgets.QToolButton()
        menu_settings_button.setObjectName("menu_settings_button")
        menu_settings_button.setIcon(svg_ico("icons:settings.svg", widgets_factory.theme.text_secondary))
        menu_settings_button.setIconSize(QtCore.QSize(20, 20))
        menu_settings_button.setStyleSheet("""
            QToolButton#menu_settings_button {
                border-radius: 10px;
                background-color: transparent;
            }
            QToolButton#menu_settings_button:hover {
                background-color: $HOVER;
            }
            QToolButton#menu_settings_button:pressed {
                background-color: transparent;
            }
        """.replace(
            "$HOVER", widgets_factory.theme.hover
        ))
        self.menu_settings_button = menu_settings_button

        memory_usage_label = Label(widgets_factory.theme.text_secondary)
        memory_usage_label.setObjectName("memory_usage_label")
        memory_usage_label.add_style("""
            QLabel#memory_usage_label {
                font-size: 12px;
                font-weight: bold;
                }
        """)
        self.memory_usage_label = memory_usage_label

        # Context menu
        context_menu = QtWidgets.QMenu(main_window)
        context_menu.setObjectName("context_menu")
        context_menu.setStyleSheet("""
            QMenuBar {
                background-color: transparent;
            }

            QMenuBar::item {
                color : $TEXT_PRIMARY_COLOR;
                margin-top:4px;
                spacing: 3px;
                padding: 1px 10px;
                background: transparent;
                border-radius: 4px;
            }


            QMenuBar::item:selected {
                background: $BG2;
            }

            QMenuBar::item:pressed {
                background: $SELECTED_COLOR;
                color: #FFFFFF;
            }

            QMenu {
                background-color: $BG1;
                border: 1px solid $HOVER_COLOR;
                border-top-right-radius: 5px;
                border-top-left-radius: 5px;
                border-bottom-right-radius: 5px;
            }
            QMenu::item {
                color: $TEXT_PRIMARY_COLOR;
                padding: 5px 20px;
            }
            QMenu::item:selected {
                background-color: $HOVER_COLOR;
            } 
                """.replace(
            "$TEXT_PRIMARY_COLOR", widgets_factory.theme.text_primary
        ).replace(
            "$BG2", widgets_factory.theme.second_background
        ).replace(
            "$SELECTED_COLOR", widgets_factory.theme.primary
        ).replace(
            "$BG1", widgets_factory.theme.first_background
        ).replace(
            "$HOVER_COLOR", widgets_factory.theme.hover
        ))
        self.settings_item = context_menu.addAction("Settings")
        self.about_item = context_menu.addAction("About")
        self.context_menu = context_menu

        menu_tool_layout.addItem(
            QtWidgets.QSpacerItem(10, 0, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        )
        menu_tool_layout.addWidget(menu_settings_button)
        menu_tool_layout.addItem(
            QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        )
        menu_tool_layout.addWidget(memory_usage_label)
        menu_tool_layout.addItem(
            QtWidgets.QSpacerItem(10, 0, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        )
        menu_layout.addLayout(menu_tool_layout)
        menu_layout.addItem(
            QtWidgets.QSpacerItem(0, 10, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        )

        # Content layout
        content_layout = QtWidgets.QStackedLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setObjectName("content_widget")
        central_layout.addLayout(content_layout)
        self.content_layout = content_layout

        self.translate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def translate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        self.menu_item_browse.setText(_translate("menu_item_browse", "Обзор"))
        self.menu_item_liked.setText(_translate("menu_item_liked", "Понравившиеся"))
        self.menu_item_popular.setText(_translate("menu_item_popular", "Популярное"))
        self.menu_item_control.setText(_translate("menu_item_control", "Управление"))
        self.menu_item_upload.setText(_translate("menu_item_upload", "Загрузить"))
        self.menu_settings_button.setToolTip(_translate("menu_settings_button", "Настройки"))
        self.settings_item.setText(_translate("settings_item", "Настройки"))
        self.about_item.setText(_translate("about_item", "О программе"))
