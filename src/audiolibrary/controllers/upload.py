from audiolibrary.views.upload import UploadView
from audiolibrary.views.widgets import WidgetsFactory


class UploadController:

    def __init__(self, model, widgets_factory: 'WidgetsFactory', parent):
        self.model = model
        self.widgets_factory = widgets_factory
        self.view = UploadView(self, self.model, widgets_factory, parent)

        self.view.show()
        self.view.model_loaded()
