from audiolibrary.config import InIConfig
from audiolibrary.controllers.browse import BrowseController
from audiolibrary.controllers.control import ControlController
from audiolibrary.controllers.liked import LikedController
from audiolibrary.controllers.popular import PopularController
from audiolibrary.controllers.settings import SettingsController
from audiolibrary.controllers.upload import UploadController
from audiolibrary.models import BrowseModel, LikedModel, PopularModel, ControlModel, UploadModel
from audiolibrary.models.main import MainModel, MenuItem
from audiolibrary.models.settings import SettingsModel
from audiolibrary.views.main import MainView
from audiolibrary.views.widgets import WidgetsFactory


class MainController:

    def __init__(
            self,
            model: 'MainModel',
            widgets_factory: 'WidgetsFactory',
            config: 'InIConfig',
            deeplink_event_bus,
            app_controller
    ):
        self.model = model
        self.config = config
        self.widgets_factory = widgets_factory
        self.deeplink_event_bus = deeplink_event_bus
        self.app_controller = app_controller
        self.view = MainView(self, model, widgets_factory, deeplink_event_bus)

        self.view.show()
        self.view.model_loaded()

    def show_settings(self):
        SettingsController(
            SettingsModel(self.config), self.widgets_factory, self.view
        )

    def show_auth(self):
        self.view.close()
        self.app_controller.auth()

    def logout(self):
        self.model.logout()
        self.show_auth()

    def show_page(self, page_id: MenuItem):
        match page_id:
            case MenuItem.BROWSE:
                model = BrowseModel()
                BrowseController(model, self.widgets_factory, self.view)
            case MenuItem.LIKED:
                model = LikedModel()
                LikedController(model, self.widgets_factory, self.view)
            case MenuItem.POPULAR:
                model = PopularModel()
                PopularController(model, self.widgets_factory, self.view)
            case MenuItem.CONTROL:
                model = ControlModel()
                ControlController(model, self.widgets_factory, self.view)
            case MenuItem.UPLOAD:
                model = UploadModel()
                UploadController(model, self.widgets_factory, self.view)
            case _:
                raise ValueError(f"Unknown menu item type: {page_id!r}")

    def close(self):
        # self.model.save_session()
        ...

    def is_auth(self) -> bool:
        return self.model.is_auth()

    def get_current_user(self) -> dict:
        return self.model.get_current_user()
