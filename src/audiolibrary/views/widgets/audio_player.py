from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtWidgets import QVBoxLayout, QLayout, QHBoxLayout, QWidget, QLabel, QToolButton, QSlider

from audiolibrary.utils.icon import svg_ico


class AudioPlayer(QWidget):
    nextClicked = QtCore.pyqtSignal()
    prevClicked = QtCore.pyqtSignal()
    playClicked = QtCore.pyqtSignal()
    pauseClicked = QtCore.pyqtSignal()

    def __init__(
            self,
            primary: str,
            hover: str,
            text_secondary: str,
            parent=None
    ):
        super().__init__(parent)
        widget_layout = QVBoxLayout(self)
        widget_layout.setContentsMargins(0, 0, 0, 0)
        widget_layout.setSpacing(0)

        sheet = QWidget(self)
        sheet.setObjectName("sheet")
        sheet.setStyleSheet("""
            QWidget#sheet {
                background-color: transparent;
            }
        """)
        widget_layout.addWidget(sheet)

        central_layout = QHBoxLayout(sheet)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(10)
        self._layout = central_layout
        sheet.setLayout(central_layout)

        # Player buttons
        player_buttons_layout = QHBoxLayout()
        player_buttons_layout.setContentsMargins(0, 0, 0, 0)
        player_buttons_layout.setSpacing(10)
        central_layout.addLayout(player_buttons_layout)

        player_prev_button = QToolButton()
        player_prev_button.setObjectName("player_prev_button")
        player_prev_button.setIcon(QtGui.QIcon(svg_ico("icons:prev.svg", primary)))
        player_prev_button.setIconSize(QtCore.QSize(24, 24))
        player_prev_button.setStyleSheet("""
        QToolButton {
            border-radius: 5px;
            background-color: transparent;
        }
        QToolButton:hover {
            background-color: rgba(0, 0, 0, 30);
        }
        QToolButton:pressed {
            background-color: transparent;
        }
            """.replace(
            "$HOVER", hover
        ))
        self.player_prev_button = player_prev_button
        player_buttons_layout.addWidget(player_prev_button)

        player_play_button = QToolButton()
        player_play_button.setObjectName("player_play_button")
        player_play_button.setIcon(QtGui.QIcon(svg_ico("icons:play.svg", primary)))
        player_play_button.setIconSize(QtCore.QSize(24, 24))

        player_play_button.setStyleSheet("""
            QToolButton {
                border-radius: 5px;
                background-color: transparent;
            }
            QToolButton:hover {
                background-color: rgba(0, 0, 0, 30);
            }
            QToolButton:pressed {
                background-color: transparent;
            }
                """.replace(
            "$HOVER", hover
        ))
        self.player_play_button = player_play_button
        player_buttons_layout.addWidget(player_play_button)

        player_next_button = QToolButton()
        player_next_button.setObjectName("player_next_button")
        player_next_button.setIcon(QtGui.QIcon(svg_ico("icons:next.svg", primary)))
        player_next_button.setIconSize(QtCore.QSize(24, 24))
        player_next_button.setStyleSheet("""
            QToolButton {
                border-radius: 5px;
                background-color: transparent;
            }
            QToolButton:hover {
                background-color: rgba(0, 0, 0, 30);
            }
            QToolButton:pressed {
                background-color: transparent;
            }
                """.replace(
            "$HOVER", hover
        ))
        self.player_next_button = player_next_button
        player_buttons_layout.addWidget(player_next_button)

        # Music info
        music_info_layout = QHBoxLayout()
        music_info_layout.setContentsMargins(0, 0, 0, 0)
        music_info_layout.setSpacing(10)
        central_layout.addLayout(music_info_layout)

        music_cover = QLabel()
        music_cover.setObjectName("music_cover")
        music_cover.setFixedSize(40, 40)
        music_cover.setStyleSheet("""
            QLabel#music_cover {
                border-radius: 5px;
                background-color: $HOVER;
            }
        """.replace(
            "$HOVER", hover
        ))
        music_cover.setPixmap(
            svg_ico("icons:music-note.svg", primary).pixmap(20, 20, QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On))
        music_cover.setContentsMargins(10, 10, 10, 10)
        self.music_cover = music_cover
        music_info_layout.addWidget(music_cover)

        music_info_right_side = QVBoxLayout()
        music_info_right_side.setContentsMargins(0, 0, 0, 0)
        music_info_right_side.setSpacing(0)
        music_info_layout.addLayout(music_info_right_side)

        music_info_first_block = QHBoxLayout()
        music_info_first_block.setContentsMargins(0, 0, 0, 0)
        music_info_first_block.setSpacing(0)
        music_info_right_side.addLayout(music_info_first_block)

        music_info_labels = QVBoxLayout()
        music_info_labels.setContentsMargins(0, 0, 0, 0)
        music_info_labels.setSpacing(0)
        music_info_first_block.addLayout(music_info_labels)

        music_title = QLabel()
        music_title.setObjectName("music_title")
        music_title.setStyleSheet("""
            QLabel#music_title {
                background-color: transparent;
                color: $PRIMARY;
                font-size: 14px;
            }
        """.replace(
            "$PRIMARY", primary
        ))
        self.music_title = music_title
        music_info_labels.addWidget(music_title)

        music_artist = QLabel()
        music_artist.setObjectName("music_artist")
        music_artist.setStyleSheet("""
            QLabel#music_artist {
                background-color: transparent;
                color: $TEXT_SECONDARY;
                font-size: 12px;
            }
        """.replace(
            "$TEXT_SECONDARY", text_secondary
        ))

        self.music_artist = music_artist
        music_info_labels.addWidget(music_artist)

        # Time Label
        time_label = QLabel()
        time_label.setObjectName("time_label")
        time_label.setStyleSheet("""
            QLabel#time_label {
                background-color: transparent;
                color: $TEXT_SECONDARY;
                font-size: 12px;
            }
        """.replace(
            "$TEXT_SECONDARY", text_secondary
        ))
        self.time_label = time_label
        music_info_first_block.addStretch(1)
        music_info_first_block.addWidget(time_label, alignment=Qt.AlignmentFlag.AlignBottom)

        # TimeLine
        time_line_widget = QSlider()
        time_line_widget.setObjectName("time_line_widget")
        time_line_widget.setOrientation(QtCore.Qt.Orientation.Horizontal)
        time_line_widget.setStyleSheet("""
            QSlider#time_line_widget {
                background-color: transparent;
            }
            QSlider::groove:horizontal {
                border-radius: 5px;
                height: 5px;
                background-color: $HOVER;
            }
            QSlider::handle:horizontal {
                width: 10px;
                margin: -2px 0;
                border-radius: 5px;
                background-color: $PRIMARY;
            }
        """.replace(
            "$HOVER", hover
        ).replace(
            "$PRIMARY", primary
        ))
        self.time_line_widget = time_line_widget
        music_info_right_side.addWidget(time_line_widget)

        music_artist.setText("Artist")
        music_title.setText("Title")
        time_label.setText("00:00")

        # Media Player
        media_widget = QMediaPlayer()
        self.media_widget = media_widget

        audio_output = QAudioOutput()
        audio_output.setVolume(100)
        self.audio_output = audio_output
        media_widget.setAudioOutput(audio_output)
        self.media_widget = media_widget

        # Theme
        self._primary = primary

        # События
        player_next_button.clicked.connect(self.nextClicked.emit)
        player_prev_button.clicked.connect(self.prevClicked.emit)
        player_play_button.clicked.connect(self.play_button_clicked)

        media_widget.durationChanged.connect(lambda duration: time_line_widget.setMaximum(duration))
        media_widget.positionChanged.connect(lambda position: time_line_widget.setValue(position))
        media_widget.positionChanged.connect(
            lambda position: time_label.setText(f"{position // 1000 // 60}:{position // 1000 % 60:02}")
        )

        time_line_widget.sliderMoved.connect(lambda position: media_widget.setPosition(position))
        time_line_widget.sliderMoved.connect(
            lambda position: time_label.setText(f"{position // 1000 // 60}:{position // 1000 % 60:02}")
        )

    def layout(self) -> QLayout | None:
        return self._layout

    def set_title(self, title: str):
        self.music_title.setText(title)

    def set_artist(self, artist: str):
        self.music_artist.setText(artist)

    def set_cover(self, cover: QtGui.QPixmap):
        self.music_cover.setPixmap(cover)

    def set_audio(self, audio: QUrl):
        self.media_widget.setSource(audio)

    def play_button_clicked(self):
        if self.media_widget.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.media_widget.pause()
            self.player_play_button.setIcon(QtGui.QIcon(svg_ico("icons:play.svg", self._primary)))
            self.pauseClicked.emit()
        else:
            self.media_widget.play()
            self.player_play_button.setIcon(QtGui.QIcon(svg_ico("icons:pause.svg", self._primary)))
            self.playClicked.emit()
