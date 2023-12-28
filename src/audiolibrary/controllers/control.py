from audiolibrary.views.control import ControlView
from audiolibrary.views.widgets import WidgetsFactory


class ControlController:

    def __init__(self, model, widgets_factory: 'WidgetsFactory', parent):
        self.model = model
        self.widgets_factory = widgets_factory
        self.view = ControlView(self, self.model, widgets_factory, parent)

        self.view.show()
        self.view.model_loaded()

