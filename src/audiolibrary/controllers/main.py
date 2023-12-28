from audiolibrary.controllers.browse import BrowseController
from audiolibrary.controllers.control import ControlController
from audiolibrary.controllers.liked import LikedController
from audiolibrary.controllers.popular import PopularController
from audiolibrary.controllers.settings import SettingsController

from audiolibrary.controllers.upload import UploadController
from audiolibrary.models import BrowseModel, LikedModel, PopularModel, ControlModel, UploadModel
from audiolibrary.models.settings import SettingsModel
from audiolibrary.models.main import MainModel, MenuItem
from audiolibrary.views.main import MainView


class MainController:

    def __init__(self, model: 'MainModel', widgets_factory: 'WidgetsFactory'):
        self.model = model
        self.widgets_factory = widgets_factory
        self.view = MainView(self, self.model, widgets_factory)

        self.view.show()
        self.view.model_loaded()

    def show_settings(self):
        SettingsController(
            SettingsModel(self.model.theme, self.model.config), self.widgets_factory, self.view
        )

    def show_page(self, page_id: MenuItem):
        match page_id:
            case MenuItem.BROWSE:
                model = BrowseModel(self.model.theme, self.model.config)
                BrowseController(model, self.widgets_factory, self.view)
            case MenuItem.LIKED:
                model = LikedModel(self.model.theme, self.model.config)
                LikedController(model, self.widgets_factory, self.view)
            case MenuItem.POPULAR:
                model = PopularModel(self.model.theme, self.model.config)
                PopularController(model, self.widgets_factory, self.view)
            case MenuItem.CONTROL:
                model = ControlModel(self.model.theme, self.model.config)
                ControlController(model, self.widgets_factory, self.view)
            case MenuItem.UPLOAD:
                model = UploadModel(self.model.theme, self.model.config)
                UploadController(model, self.widgets_factory, self.view)
            case _:
                raise ValueError(f"Unknown menu item type: {page_id!r}")
