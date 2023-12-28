from audiolibrary.views.popular import PopularView
from audiolibrary.views.widgets import WidgetsFactory


class PopularController:

    def __init__(self, model, widgets_factory: 'WidgetsFactory', parent):
        self.model = model
        self.widgets_factory = widgets_factory
        self.view = PopularView(self, self.model, widgets_factory, parent)

        self.view.show()
        self.view.model_loaded()

