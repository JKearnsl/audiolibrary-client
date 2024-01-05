from typing import Literal

from PyQt6.QtCore import pyqtSignal, Qt, QSize
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QToolButton

from audiolibrary.utils.icon import svg_ico

PlayState = Literal["playing", "paused", "stopped"]


class AudioItemWidget(QWidget):
    playClicked = pyqtSignal()
    pauseClicked = pyqtSignal()

    def __init__(
            self,
            title: str,
            subtitle: str,
            _id: any,
            hover_color: str,
            primary_color: str,
            text_secondary: str = None,
            cover=None,
            parent: QWidget = None
    ):
        super().__init__(parent)

        self._hover_color = hover_color
        self.state: PlayState = "stopped"

        self.setCursor(Qt.CursorShape.PointingHandCursor)

        widget_layout = QHBoxLayout(self)
        widget_layout.setContentsMargins(0, 0, 0, 0)
        widget_layout.setSpacing(0)

        sheet = QWidget()
        widget_layout.addWidget(sheet)
        sheet.setObjectName("sheet")
        sheet.setStyleSheet("""
            QWidget#sheet {
                background-color: transparent;
                border: none;
                outline: none;
            }
        """)
        self._sheet = sheet

        sheet_layout = QHBoxLayout(sheet)
        sheet_layout.setContentsMargins(5, 5, 5, 5)
        sheet_layout.setSpacing(10)
        sheet_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # Icon
        music_cover = QLabel()
        sheet_layout.addWidget(music_cover)
        music_cover.setObjectName("music_cover")
        music_cover.setFixedSize(32, 32)
        music_cover.setStyleSheet("""
                    QLabel#music_cover {
                        border-radius: 5px;
                        background-color: $HOVER;
                    }
                """.replace(
            "$HOVER", hover_color
        ))
        music_cover.setAlignment(Qt.AlignmentFlag.AlignCenter)
        music_cover.setPixmap(svg_ico("icons:music-note.svg", primary_color).pixmap(24, 24))

        music_cover_layout = QVBoxLayout(music_cover)
        music_cover_layout.setContentsMargins(0, 0, 0, 0)
        music_cover_layout.setSpacing(0)

        # Gray Cover
        gray_cover = QLabel()
        self._gray_cove = gray_cover
        gray_cover.hide()
        gray_cover.setObjectName("gray_cover")
        gray_cover.setStyleSheet("""
                    QLabel#gray_cover {
                        background-color: rgba(0, 0, 0, 100);
                        border-radius: 5px;
                    }
                """)
        gray_cover.setFixedSize(32, 32)
        gray_cover.setAlignment(Qt.AlignmentFlag.AlignCenter)
        music_cover_layout.addWidget(gray_cover)

        gray_cover_layout = QHBoxLayout(gray_cover)
        gray_cover_layout.setContentsMargins(0, 0, 0, 0)
        gray_cover_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        gray_cover_layout.setSpacing(0)

        # Play Button
        play_button = QToolButton()
        play_button.setObjectName("play_button")
        play_button.setIcon(svg_ico("icons:play.svg", "white"))
        play_button.setIconSize(QSize(24, 24))
        play_button.setFixedSize(24, 24)

        play_button.setStyleSheet("""
            QToolButton {
                border-radius: 5px;
                background-color: transparent;
            }
        """.replace(
            "$HOVER", hover_color
        ))
        self.play_button = play_button
        gray_cover_layout.addWidget(play_button)

        # Text Block
        right_side = QVBoxLayout()
        right_side.setContentsMargins(0, 0, 0, 0)
        right_side.setSpacing(0)
        sheet_layout.addLayout(right_side)

        first_block = QHBoxLayout()
        first_block.setContentsMargins(0, 0, 0, 0)
        first_block.setSpacing(0)
        right_side.addLayout(first_block)

        labels = QVBoxLayout()
        labels.setContentsMargins(0, 0, 0, 0)
        labels.setSpacing(0)
        first_block.addLayout(labels)

        music_title = QLabel()
        music_title.setObjectName("music_title")
        music_title.setStyleSheet("""
               QLabel#music_title {
                   background-color: transparent;
                   color: $PRIMARY;
                   font-size: 12px;
               }
           """.replace(
            "$PRIMARY", primary_color
        ))
        music_title.setText(title)
        labels.addWidget(music_title)

        music_artist = QLabel()
        music_artist.setObjectName("music_artist")
        music_artist.setStyleSheet("""
           QLabel#music_artist {
               background-color: transparent;
               color: $TEXT_SECONDARY;
               font-size: 10px;
           }
       """.replace(
            "$TEXT_SECONDARY", text_secondary
        ))
        music_artist.setText(subtitle)
        labels.addWidget(music_artist)

        # Time Label
        time_label = QLabel()
        time_label.setObjectName("time_label")
        time_label.setStyleSheet("""
           QLabel#time_label {
               background-color: transparent;
               color: $TEXT_SECONDARY;
               font-size: 10px;
           }
       """.replace(
            "$TEXT_SECONDARY", text_secondary
        ))
        time_label.setText("3:45")
        first_block.addStretch(1)
        first_block.addWidget(time_label, alignment=Qt.AlignmentFlag.AlignVCenter)

        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        self.enterEvent = lambda event: self.enter_hover()
        self.leaveEvent = lambda event: self.leave_hover()

        # Events
        self.mouseReleaseEvent = lambda event: self.playClicked.emit()
        self.playClicked.connect(lambda: self.set_state("playing"))

    def set_state(self, state: Literal["playing", "paused", "stopped"]):
        self.state = state

        if state == "playing":
            self.play_button.setIcon(svg_ico("icons:pause.svg", "white"))
            self.enter_hover()
            return

        if state == "paused":
            self.play_button.setIcon(svg_ico("icons:play.svg", "white"))
            self.enter_hover()
            return

        if state == "stopped":
            self.play_button.setIcon(svg_ico("icons:play.svg", "white"))
            self.enter_hover()
            return

        raise Exception("Unknown state")

    def enter_hover(self):
        self._gray_cove.show()
        self.play_button.show()
        self._sheet.setStyleSheet("""
            QWidget#sheet {
                background-color: $HOVER;
                border: none;
                outline: none;
            }
        """.replace(
            "$HOVER", self._hover_color
        ))

    def leave_hover(self):
        self.play_button.hide()
        if self.state != "playing":
            self._gray_cove.hide()
            self._sheet.setStyleSheet("""
                QWidget#sheet {
                    background-color: transparent;
                    border: none;
                    outline: none;
                }
            """)
