import logging
import os
import textwrap
from os.path import getsize

from PyQt6 import QtCore
from PyQt6.QtGui import QDropEvent
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QStackedWidget, QToolButton, QFileDialog

from audiolibrary.utils.icon import svg_ico


class FileSelectBox(QWidget):
    def __init__(
            self,
            background_color,
            hover_color,
            text_color,
            icon_primary: str,
            icon_move: str,
            parent=None
    ):
        super().__init__(parent)

        self._file_filter_title = "File"
        self._file_filters = []
        self.setAcceptDrops(True)
        self.setMinimumHeight(100)

        widget_layout = QHBoxLayout(self)
        widget_layout.setContentsMargins(0, 0, 0, 0)
        widget_layout.setSpacing(0)

        sheet = QWidget()
        widget_layout.addWidget(sheet)
        sheet.setObjectName("sheet")
        sheet.setStyleSheet("""
            QWidget#sheet {
                background-color: $BG;
                border-radius: 5px;
                border: 2px dashed $HOVER;
            }
        """.replace(
            "$BG", background_color
        ).replace(
            "$HOVER", hover_color
        ))

        central_layout = QVBoxLayout()
        central_layout.setContentsMargins(0, 0, 0, 0)
        sheet.setLayout(central_layout)

        # StackedWidget
        self._stacked_widget = QStackedWidget(sheet)
        self._stacked_widget.setObjectName("stacked_widget")
        central_layout.addWidget(self._stacked_widget)

        # Empty state
        empty_state = QWidget()
        empty_state.mousePressEvent = lambda _: self.file_selection_window()
        empty_state.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        empty_state_layout = QVBoxLayout()
        empty_state_layout.setContentsMargins(10, 10, 10, 10)
        empty_state_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        empty_state_layout.setSpacing(20)
        empty_state.setLayout(empty_state_layout)
        self._stacked_widget.addWidget(empty_state)

        empty_state_icon_layout = QHBoxLayout()
        empty_state_icon_layout.setContentsMargins(0, 0, 0, 0)
        empty_state_icon_layout.setSpacing(0)
        empty_state_layout.addLayout(empty_state_icon_layout)

        empty_state_icon = QLabel()
        empty_state_icon.setObjectName("empty_state_icon")
        empty_state_icon.setStyleSheet("""
            QLabel#empty_state_icon {
                background-color: transparent;
                border: none;
                outline: none;
            }
            """)
        empty_state_icon.setPixmap(svg_ico(icon_primary, text_color).pixmap(QtCore.QSize(64, 64)))
        empty_state_icon.setScaledContents(True)
        empty_state_icon.setFixedSize(QtCore.QSize(64, 64))
        empty_state_icon_layout.addWidget(empty_state_icon)

        # Text
        empty_state_text_label = QLabel()
        self._empty_state_text_label = empty_state_text_label
        empty_state_text_label.setObjectName("empty_state_text_label")
        empty_state_text_label.setWordWrap(True)
        empty_state_text_label.setText("Select file or drag and drop here")
        empty_state_text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignTop)
        empty_state_text_label.setStyleSheet("""
            QLabel#empty_state_text_label {
                color: $TEXT_COLOR;
                font-size: 13px;
                font-weight: bold;
                border: none;
                outline: none;
            }
        """.replace(
            "$TEXT_COLOR", text_color
        ))
        empty_state_layout.addWidget(empty_state_text_label)

        # Move state
        move_state = QWidget()
        move_state_layout = QVBoxLayout()
        move_state_layout.setContentsMargins(10, 10, 10, 10)
        move_state_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        move_state_layout.setSpacing(20)
        move_state.setLayout(move_state_layout)
        self._stacked_widget.addWidget(move_state)

        move_state_icon_layout = QHBoxLayout()
        move_state_icon_layout.setContentsMargins(0, 0, 0, 0)
        move_state_icon_layout.setSpacing(0)
        move_state_layout.addLayout(move_state_icon_layout)

        move_state_icon = QLabel()
        move_state_icon.setObjectName("move_state_icon")
        move_state_icon.setStyleSheet("""
                QLabel#move_state_icon {
                    background-color: transparent;
                    border: none;
                    outline: none;
                }
                """)
        move_state_icon.setPixmap(svg_ico(icon_move, text_color).pixmap(QtCore.QSize(64, 64)))
        move_state_icon.setScaledContents(True)
        move_state_icon.setFixedSize(QtCore.QSize(64, 64))
        move_state_icon_layout.addWidget(move_state_icon)

        # Selected state
        selected_state = QWidget()
        selected_state_layout = QVBoxLayout()
        selected_state_layout.setContentsMargins(10, 10, 10, 10)
        selected_state_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        selected_state_layout.setSpacing(20)
        selected_state.setLayout(selected_state_layout)
        self._stacked_widget.addWidget(selected_state)

        selected_state_file = QWidget()
        selected_state_file.setObjectName("selected_state_file")
        selected_state_file.setStyleSheet("""
            QWidget#selected_state_file {
                background-color: transparent;
                border: 2px double $HOVER;
                border-radius: 10px;
            }
            """.replace(
            "$HOVER", hover_color
        ))
        selected_state_file_layout = QHBoxLayout()
        selected_state_file_layout.setContentsMargins(10, 10, 10, 10)
        selected_state_file_layout.setSpacing(10)
        selected_state_file.setLayout(selected_state_file_layout)
        selected_state_layout.addWidget(selected_state_file)

        selected_state_file_label = QLabel()
        selected_state_file_label.setObjectName("selected_state_file_label")
        selected_state_file_label.setStyleSheet("""
            QLabel#selected_state_file_label {
                background-color: transparent;
                border: none;
                outline: none;
                color: $TEXT_COLOR;
                font-weight: bold;
            }
            """.replace(
            "$TEXT_COLOR", text_color
        ))
        selected_state_file_label.setText("File:")
        selected_state_file_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self._selected_state_file_label = selected_state_file_label
        selected_state_file_layout.addWidget(selected_state_file_label)

        selected_state_file_delete_button = QToolButton()
        selected_state_file_delete_button.setObjectName("selected_state_file_delete_button")
        selected_state_file_delete_button.setStyleSheet("""
            QToolButton#selected_state_file_delete_button {
                background-color: transparent;
                border: none;
                outline: none;
            }
            """)
        selected_state_file_delete_button.setIcon(svg_ico("icons:trash.svg", text_color))
        selected_state_file_delete_button.setIconSize(QtCore.QSize(24, 24))
        selected_state_file_delete_button.setFixedSize(QtCore.QSize(24, 24))
        selected_state_file_delete_button.clicked.connect(lambda: self._stacked_widget.setCurrentIndex(0))
        selected_state_file_layout.addWidget(selected_state_file_delete_button)

        self._stacked_widget.setCurrentWidget(empty_state)

        self._selected_file_path = None

    def add_style(self, style: str):
        self.setStyleSheet(self.styleSheet() + style)

    def selected_filepath(self) -> str | None:
        if self._stacked_widget.currentIndex() == 2:
            return self._selected_file_path

    def set_file_filters(self, filters: list[str], title: str = None):
        if title:
            self._file_filter_title = title
        self._file_filters.extend(filters)

    def set_text(self, text: str):
        self._empty_state_text_label.setText(text)

    def set_file(self, path: str):
        if not os.path.exists(path):
            return

        if not os.path.isfile(path):
            return

        if self._file_filters:
            if not any(path.endswith(f.replace(' ', '').replace('*', '')) for f in self._file_filters):
                return

        filename = textwrap.shorten(os.path.basename(path), width=20, placeholder='...')
        size = round(getsize(path) / 1024 / 1024, 1)

        if size > 1024:
            size = round(size / 1024, 1)
            size = f"{size} GB"
        else:
            size = f"{size} MB"

        self._selected_file_path = path
        self._selected_state_file_label.setText(f"File: {filename} ({size})")
        self._stacked_widget.setCurrentIndex(2)

    def file_selection_window(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        file_dialog.setNameFilter(f"{self._file_filter_title} ({' '.join(self._file_filters)})")

        result = file_dialog.exec()
        if result == QFileDialog.DialogCode.Accepted:
            self.set_file(file_dialog.selectedFiles()[0])

    def dragEnterEvent(self, a0):
        if a0.mimeData().hasUrls():
            a0.acceptProposedAction()
            self._stacked_widget.setCurrentIndex(1)

    def dragLeaveEvent(self, a0):
        self._stacked_widget.setCurrentIndex(0)

    def dropEvent(self, a0: QDropEvent):
        if a0.mimeData().hasUrls():
            a0.acceptProposedAction()
            url = a0.mimeData().urls()[0]
            if not url.isLocalFile():
                return

            self.set_file(url.path())
