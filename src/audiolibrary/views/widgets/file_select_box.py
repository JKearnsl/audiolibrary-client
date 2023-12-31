from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel

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
        widget_layout = QHBoxLayout(self)
        widget_layout.setContentsMargins(0, 0, 0, 0)
        widget_layout.setSpacing(0)

        sheet = QWidget()
        sheet.setObjectName("sheet")
        sheet.setStyleSheet("""
            QWidget {
                background-color: $BG1;
                border-radius: 5px;
                border: 2px dashed $HOVER;
            }
        """.replace(
            "$BG1", background_color
        ).replace(
            "$HOVER", hover_color
        ))
        widget_layout.addWidget(sheet)

        self.setAcceptDrops(True)
        self.setMinimumHeight(100)

        central_layout = QVBoxLayout(sheet)
        central_layout.setContentsMargins(10, 10, 10, 10)
        central_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        central_layout.setSpacing(20)

        # Body
        icon_layout = QHBoxLayout()
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.setSpacing(0)
        central_layout.addLayout(icon_layout)

        icon = QLabel()
        icon.setObjectName("icon")
        icon.setStyleSheet("""
            QLabel#icon {
                background-color: transparent;
                border: none;
                outline: none;
            }
            """)
        icon.setPixmap(svg_ico(icon_primary, text_color).pixmap(QtCore.QSize(64, 64)))
        icon.setScaledContents(True)
        icon.setFixedSize(QtCore.QSize(64, 64))
        icon_layout.addWidget(icon)
        self._icon_widget = icon

        # Text
        text_label = QLabel()
        text_label.setObjectName("text_label")
        text_label.setWordWrap(True)
        text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignTop)
        text_label.setStyleSheet("""
            QLabel#text_label {
                color: $TEXT_COLOR;
                font-size: 13px;
                font-weight: bold;
                border: none;
                outline: none;
            }
        """.replace(
            "$TEXT_COLOR", text_color
        ))
        central_layout.addWidget(text_label)
        self._text_label = text_label
        self._icon_primary = icon_primary
        self._icon_move = icon_move
        self._text_color = text_color
        self._selected_file = None

    def add_style(self, style: str):
        self.setStyleSheet(self.styleSheet() + style)

    def set_text(self, text: str = "Select File or Drag and Drop"):
        self._text_label.setText(text)

    def dragEnterEvent(self, a0):
        if a0.mimeData().hasUrls():
            a0.acceptProposedAction()
            self._icon_widget.setPixmap(
                svg_ico(self._icon_move, self._text_color).pixmap(QtCore.QSize(64, 64))
            )
            self._text_label.hide()

    def dragLeaveEvent(self, a0):
        self._icon_widget.setPixmap(
            svg_ico(self._icon_primary, self._text_color).pixmap(QtCore.QSize(64, 64))
        )
        self._text_label.show()

    def dropEvent(self, a0):
        if a0.mimeData().hasUrls():
            a0.acceptProposedAction()
            self.setStyleSheet(self.styleSheet() + """
                QWidget {
                    border: 2px dashed $HOVER;
                }
            """.replace(
                "$HOVER", "#00FF00"
            ))

            self.text_label.setText("File Selected")
            self.text_label.setStyleSheet("""
                QLabel#text_label {
                    color: $TEXT_COLOR;
                }
            """.replace(
                "$TEXT_COLOR", "#00FF00"
            ))

            self.file_selected.emit(a0.mimeData().urls()[0].toLocalFile())
