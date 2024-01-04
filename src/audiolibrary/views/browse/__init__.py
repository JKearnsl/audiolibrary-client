from typing import TypeVar

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QStandardItem
from PyQt6.QtWidgets import QWidget, QListWidgetItem, QHBoxLayout, QLabel, QVBoxLayout, QToolButton

from audiolibrary.utils.icon import svg_ico
from audiolibrary.utils.observer import DObserver
from audiolibrary.utils.ts_meta import TSMeta

from audiolibrary.models import MenuItem
from audiolibrary.views.browse.static_ui import UiBrowsePage

ViewWidget = TypeVar('ViewWidget', bound=QWidget)


class MusicItemWidget(QListWidgetItem):
    id: any

    def __init__(
            self,
            title: str,
            subtitle: str,
            _id: any,
            hover_color: str,
            primary_color: str,
            text_secondary: str = None,
            ico=None
    ):
        super().__init__()
        self.id = _id
        self.setSizeHint(QSize(0, 40))
        self.setFlags(self.flags() & ~Qt.ItemFlag.ItemIsSelectable)
        self.setFlags(self.flags() & ~Qt.ItemFlag.ItemIsEnabled)

        widget = QWidget()
        self._widget = widget
        widget.setObjectName(f"item_{_id}")
        widget.setStyleSheet("""
            QWidget#$OBJECT_NAME {
                background-color: transparent;
                border: none;
                outline: none;
            }
            
            QWidget#$OBJECT_NAME:hover {
                background-color: $HOVER_COLOR;
            }
            
        """.replace(
            "$HOVER_COLOR", hover_color
        ).replace(
            "$OBJECT_NAME", widget.objectName()
        ))
        widget.setCursor(Qt.CursorShape.PointingHandCursor)

        widget_layout = QHBoxLayout(widget)
        widget_layout.setContentsMargins(5, 5, 5, 5)
        widget_layout.setSpacing(10)
        widget_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # Icon
        music_cover = QLabel()
        widget_layout.addWidget(music_cover)
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
        widget_layout.addLayout(right_side)

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

        widget.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        widget.enterEvent = lambda event: self.enter_hover()
        widget.leaveEvent = lambda event: self.leave_hover()

    def widget(self):
        return self._widget

    def enter_hover(self):
        self._gray_cove.show()

    def leave_hover(self):
        self._gray_cove.hide()

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} title={self.text()}>"


class BrowseView(QWidget, DObserver, metaclass=TSMeta):
    id: MenuItem

    def __init__(self, controller, model, widgets_factory, parent: ViewWidget):
        super().__init__(parent)
        self.id = model.id
        self.controller = controller
        self.model = model
        self.widgets_factory = widgets_factory

        parent.ui.content_layout.addWidget(self)
        parent.ui.content_layout.setCurrentWidget(self)

        self.ui = UiBrowsePage()
        self.ui.setup_ui(self, widgets_factory)

        # Регистрация представлений
        self.model.add_observer(self)

        # События
        self.ui.search_line.textChanged.connect(self.search_line_changed)

    def model_changed(self):
        ...

    def model_loaded(self):
        self.model_changed()

    def search_line_changed(self, text: str):
        result = self.controller.search(text)
        self.ui.result_list.model().removeRows(0, self.ui.result_list.model().rowCount())

        for model in result:
            item = MusicItemWidget(
                model.title,
                model.artist,
                model.id,
                self.widgets_factory.theme.hover,
                self.widgets_factory.theme.primary,
                self.widgets_factory.theme.text_secondary
            )
            self.ui.result_list.addItem(item)
            self.ui.result_list.setItemWidget(item, item.widget())
