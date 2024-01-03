from audiolibrary.views.browse import BrowseView
from audiolibrary.views.widgets import WidgetsFactory


class BrowseController:

    def __init__(self, model, widgets_factory: 'WidgetsFactory', parent):
        self.model = model
        self.widgets_factory = widgets_factory
        self.view = BrowseView(self, self.model, widgets_factory, parent)

        self.view.show()
        self.view.model_loaded()

    def search(self, query: str):
        return self.model.search(query)