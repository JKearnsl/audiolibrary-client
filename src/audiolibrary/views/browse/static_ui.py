from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QListWidget

from audiolibrary.views.widgets import WidgetsFactory


class UiBrowsePage:
    def setup_ui(self, page: QtWidgets.QWidget, widgets_factory: WidgetsFactory):
        page.setObjectName("page")
        page_layout = QtWidgets.QVBoxLayout(page)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.setSpacing(0)

        scroll_area = QtWidgets.QScrollArea(page)
        scroll_area.setObjectName("scroll_area")
        scroll_area.setStyleSheet("""
            QWidget#scroll_area {
                background-color: $BG1;
                border: none;
                outline: none;
            }
        """.replace(
            "$BG1", widgets_factory.theme.first_background)
        )
        scroll_area.setWidgetResizable(True)
        page_layout.addWidget(scroll_area)

        central_layout = QtWidgets.QVBoxLayout(scroll_area)
        central_layout.setContentsMargins(30, 20, 30, 20)
        central_layout.setSpacing(10)
        central_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignTop)

        # Body

        # SlideShow
        slide_show = widgets_factory.slide_show()

        button = widgets_factory.button()
        slide_show.add_slide(
            image_path="/home/jkearnsl/Изображения/fec910ef1203e78b4c3a6fbe4b9a8f7e.jpg",
            title="Название альбома",
            description="Описание альбома",
            button=button
        )
        button2 = widgets_factory.button()
        slide_show.add_slide(
            image_path="/home/jkearnsl/Изображения/akKFtPZtBJ0.jpg",
            title="Название альбома2",
            description="Описание альбома2",
            button=button2
        )
        button3 = widgets_factory.button()
        slide_show.add_slide(
            image_path="/home/jkearnsl/Изображения/wallpaper/iybTCTjKNos.jpg",
            title="Название альбома3",
            description="Описание альбома3",
            button=button3
        )
        central_layout.addWidget(slide_show)

        # Search Block
        search_block = QtWidgets.QWidget()
        search_block.setObjectName("search_block")
        search_block.setStyleSheet("""
            QWidget#search_block {
                background-color: $BG2;
                border-radius: 5px;
                border: 1px solid $HOVER;
            }
        """.replace(
            "$BG2", widgets_factory.theme.second_background
        ).replace(
            "$HOVER", widgets_factory.theme.hover
        ))

        search_block_layout = QtWidgets.QVBoxLayout(search_block)
        search_block_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.addWidget(search_block)

        search_line = widgets_factory.line_edit()
        search_line.setObjectName("search_line")
        self.search_line = search_line
        search_block_layout.addWidget(search_line)

        result_list = QListWidget()
        result_list.setObjectName("result_list")
        result_list.setStyleSheet("""
            QListWidget#result_list {
                background-color: transparent;
            }
        """)
        result_list.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        result_list.hide()
        search_block_layout.addWidget(result_list)
        search_block_layout.addStretch(1)
        search_line.focusIn.connect(lambda: result_list.show())
        search_line.focusOut.connect(lambda: result_list.hide() if not search_line.text() else None)
        self.result_list = result_list

        central_layout.addStretch(1)
        self.translate_ui(page)
        QtCore.QMetaObject.connectSlotsByName(page)

    def translate_ui(self, page: QtWidgets.QWidget):
        _translate = QtCore.QCoreApplication.translate
        self.search_line.setPlaceholderText(_translate("browse_page_search_placeholder", "Поиск"))
