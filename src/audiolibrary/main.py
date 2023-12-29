import atexit
import os
import shutil
import sys
import tempfile

from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QApplication, QStyleFactory

from audiolibrary.api_service import APIServiceV1
from audiolibrary.config import InIConfig
from audiolibrary.controllers import ApplicationController
from audiolibrary.models.main import MainModel
from audiolibrary.themes import BASE_THEME
from audiolibrary.utils.theme import get_themes
from audiolibrary.views.widgets import WidgetsFactory


def main():
    QApplication.setDesktopSettingsAware(False)
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))

    QtCore.QDir.addSearchPath('icons', 'assets/icons')
    tempfile.tempdir = os.path.join(os.path.expanduser("~"), ".audiolibrary", "tmp", str(os.getpid()))
    os.makedirs(tempfile.tempdir, exist_ok=True)
    atexit.register(lambda: shutil.rmtree(tempfile.tempdir))

    config = InIConfig("config.ini")

    app.setApplicationName(config.VAR.BASE.APP_NAME)
    app.setApplicationDisplayName(config.VAR.BASE.APP_NAME)
    app.setOrganizationName("jkearnsl")
    app.setOrganizationDomain("jkearnsl")
    app.setApplicationVersion(config.VAR.VERSION)
    app.setDesktopFileName(f"jkearnsl.{config.VAR.BASE.APP_NAME}")

    app_icon = QtGui.QIcon()
    app_icon.addFile("icons:logo-16.png", QtCore.QSize(16, 16))
    app_icon.addFile("icons:logo-32.png", QtCore.QSize(24, 24))
    app_icon.addFile("icons:logo-32.png", QtCore.QSize(32, 32))
    app_icon.addFile("icons:logo-64.png", QtCore.QSize(48, 48))
    app_icon.addFile("icons:logo-64.png", QtCore.QSize(64, 64))
    app_icon.addFile("icons:logo-128.png", QtCore.QSize(128, 128))
    app_icon.addFile("icons:logo-256.png", QtCore.QSize(256, 256))
    app.setWindowIcon(app_icon)

    # Для сессии Wayland необходимо установить .desktop файл
    # Источники:
    # - https://github.com/OpenShot/openshot-qt/pull/3354
    # - https://github.com/openscad/openscad/blob/master/src/openscad.cc#L724
    # - https://github.com/openscad/openscad/issues/4505
    # - https://specifications.freedesktop.org/desktop-entry-spec/latest/ar01s02.html
    # - https://nicolasfella.de/posts/fixing-wayland-taskbar-icons/
    # - https://github.com/PhotoFlare/photoflare/pull/465/files#diff-c1c1d39b766177a787f02a2fd79839ceb5db497c09348db95001752e5f5b0dde
    # - https://specifications.freedesktop.org/desktop-entry-spec/desktop-entry-spec-latest.html
    # Для Windows необходимо установить .ico файл, а также app_id:
    # - https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105
    # И иконку рабочего стола:
    # - https://askubuntu.com/questions/476981/how-do-i-make-a-desktop-icon-to-launch-a-program

    theme = get_themes()[0].get(config.VAR.BASE.THEME_TITLE)
    if not theme:
        theme = BASE_THEME

    widgets_factory = WidgetsFactory(theme[0])
    api_service = APIServiceV1(config.VAR.BASE.API_URL)
    model = MainModel(
        is_debug=config.VAR.BASE.DEBUG,
        app_title=config.VAR.BASE.APP_NAME,
        app_version=config.VAR.VERSION,
        contact=config.VAR.BASE.CONTACT,
        api_service=api_service,
    )
    controller = ApplicationController(
        api_service=api_service,
        widgets_factory=widgets_factory,
        config=config,
    )
    controller.main()

    app.exec()


if __name__ == '__main__':
    sys.exit(main())
