from audiolibrary.views.liked import LikedView
from audiolibrary.views.widgets import WidgetsFactory


class LikedController:

    def __init__(self, model, widgets_factory: 'WidgetsFactory', parent):
        self.model = model
        self.widgets_factory = widgets_factory
        self.view = LikedView(self, self.model, widgets_factory, parent)

        self.view.show()
        self.view.model_loaded()

