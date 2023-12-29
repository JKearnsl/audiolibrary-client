from audiolibrary.controllers.auth import AuthController
from audiolibrary.controllers.main import MainController
from audiolibrary.models import MainModel
from audiolibrary.models.auth import AuthModel
from audiolibrary.views.widgets import WidgetsFactory


class ApplicationController:
    """
        Mediator between controllers


    """

    def __init__(self, api_service, widgets_factory: 'WidgetsFactory', config):
        self.api_service = api_service
        self.widgets_factory = widgets_factory
        self.config = config

    def auth(self):
        AuthController(
            AuthModel(
                self.api_service,
            ),
            self.widgets_factory,
            self
        )

    def main(self):
        MainController(
            MainModel(
                is_debug=self.config.VAR.BASE.DEBUG,
                app_title=self.config.VAR.BASE.APP_NAME,
                app_version=self.config.VAR.VERSION,
                contact=self.config.VAR.BASE.CONTACT,
                api_service=self.api_service,
            ),
            self.widgets_factory,
            self.config,
            self
        )
