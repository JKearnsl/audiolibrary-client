from typing import TypeVar

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QWidget, QListWidgetItem

from audiolibrary.models import MenuItem
from audiolibrary.utils.observer import DObserver
from audiolibrary.utils.ts_meta import TSMeta
from audiolibrary.views.browse.static_ui import UiBrowsePage

ViewWidget = TypeVar('ViewWidget', bound=QWidget)


class MusicItem(QListWidgetItem):
    def __init__(self):
        super().__init__()
        self.setSizeHint(QSize(0, 40))
        self.setFlags(self.flags() & ~Qt.ItemFlag.ItemIsSelectable)
        self.setFlags(self.flags() & ~Qt.ItemFlag.ItemIsEnabled)


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
            item = MusicItem()
            widget = self.widgets_factory.audio_item(
                model.title,
                model.artist,
                model.id,
            )
            self.ui.result_list.addItem(item)
            self.ui.result_list.setItemWidget(item, widget)
