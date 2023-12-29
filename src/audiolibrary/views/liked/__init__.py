from typing import TypeVar

from PyQt6.QtWidgets import QWidget

from audiolibrary.utils.observer import DObserver
from audiolibrary.utils.ts_meta import TSMeta

from audiolibrary.models import MenuItem
from audiolibrary.views.liked.static_ui import UiLikedPage

ViewWidget = TypeVar('ViewWidget', bound=QWidget)


class LikedView(QWidget, DObserver, metaclass=TSMeta):
    id: MenuItem

    def __init__(self, controller, model, widgets_factory, parent: ViewWidget):
        super().__init__(parent)
        self.id = model.id
        self.controller = controller
        self.model = model
        self.widgets_factory = widgets_factory

        parent.ui.content_layout.addWidget(self)
        parent.ui.content_layout.setCurrentWidget(self)

        self.ui = UiLikedPage()
        self.ui.setup_ui(self, widgets_factory)

        # Регистрация представлений
        self.model.add_observer(self)

        # События

    def model_changed(self):
        ...

    def model_loaded(self):
        self.model_changed()
