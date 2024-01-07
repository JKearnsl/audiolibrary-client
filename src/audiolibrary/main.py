import atexit
import logging
import os
import shutil
import sys
import tempfile
from urllib.parse import urlparse

from PyQt6 import QtCore, QtGui
from PyQt6.QtNetwork import QLocalSocket, QLocalServer, QAbstractSocket
from PyQt6.QtWidgets import QApplication, QStyleFactory

from audiolibrary.api_service import APIServiceV1
from audiolibrary.config import InIConfig
from audiolibrary.controllers import ApplicationController
from audiolibrary.themes import BASE_THEME
from audiolibrary.utils.theme import get_themes
from audiolibrary.views.widgets import WidgetsFactory


class DeepLinkEventBus(QtCore.QObject):
    album = QtCore.pyqtSignal(str)
    track = QtCore.pyqtSignal(str)
    news = QtCore.pyqtSignal(str)


class AudioLibraryApp(QApplication):
    def __init__(self, *args):
        super().__init__(*args)
        data_path = os.path.join(os.path.expanduser("~"), ".audiolibrary")
        tempfile.tempdir = os.path.join(data_path, "tmp", str(os.getpid()))
        os.makedirs(tempfile.tempdir, exist_ok=True)
        atexit.register(lambda: shutil.rmtree(tempfile.tempdir))

        self._server = None
        self._client = QLocalSocket()
        self._client.connectToServer(self.__class__.__name__)

        deep_link: str | None = (
            args[0][args[0].index("--"):][-1]
            if "--" in args[0] and len(args[0][args[0].index("--"):]) > 0
            else None
        )
        if self._client.waitForConnected(500):
            if deep_link:
                self._client.write(deep_link.encode())
                self._client.waitForBytesWritten()
            self._client.disconnectFromServer()
            sys.exit(0)

        self._server = QLocalServer()
        self._server.listen(self.__class__.__name__)
        if not self._server.isListening():
            match self._server.serverError():
                case QAbstractSocket.SocketError.AddressInUseError:
                    logging.warning("[Server] ServerError: Address in use, trying to remove server.")
                    QLocalServer.removeServer(self.__class__.__name__)
                    self._server.listen(self.__class__.__name__)
                    if not self._server.isListening():
                        raise RuntimeError("ServerError: Address in use.")
                case QAbstractSocket.SocketError.ConnectionRefusedError:
                    raise RuntimeError("ServerError: Connection refused.")
                case QAbstractSocket.SocketError.HostNotFoundError:
                    raise RuntimeError("ServerError: Host not found.")
                case _:
                    raise RuntimeError("ServerError: Unknown error.")
        else:
            logging.debug(f"[Server] Listening on {self._server.serverName()}")

        self.deeplink_event_bus = DeepLinkEventBus()
        self._server.newConnection.connect(self.handle_deep_link)

        QApplication.setDesktopSettingsAware(False)
        self.setStyle(QStyleFactory.create("Fusion"))

        QtCore.QDir.addSearchPath('icons', 'assets/icons')

        if os.path.exists("../../config.ini"):
            config_path = "../../config.ini"
        elif os.path.exists(os.path.join(data_path, "config.ini")):
            config_path = os.path.join(data_path, "config.ini")
        else:
            raise FileNotFoundError("Файл конфигурации не найден")

        config = InIConfig(config_path)

        self.setApplicationName(config.VAR.BASE.APP_NAME)
        self.setApplicationDisplayName(config.VAR.BASE.APP_NAME)
        self.setOrganizationName("jkearnsl")
        self.setOrganizationDomain("jkearnsl")
        self.setApplicationVersion(config.VAR.VERSION)
        self.setDesktopFileName(f"jkearnsl.{config.VAR.BASE.APP_NAME}")

        # Application icon
        app_icon = QtGui.QIcon()
        app_icon.addFile("icons:logo-16.png", QtCore.QSize(16, 16))
        app_icon.addFile("icons:logo-32.png", QtCore.QSize(24, 24))
        app_icon.addFile("icons:logo-32.png", QtCore.QSize(32, 32))
        app_icon.addFile("icons:logo-64.png", QtCore.QSize(48, 48))
        app_icon.addFile("icons:logo-64.png", QtCore.QSize(64, 64))
        app_icon.addFile("icons:logo-128.png", QtCore.QSize(128, 128))
        app_icon.addFile("icons:logo-256.png", QtCore.QSize(256, 256))
        self.setWindowIcon(app_icon)

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

        controller = ApplicationController(
            api_service=api_service,
            widgets_factory=widgets_factory,
            config=config,
            deeplink_event_bus=self.deeplink_event_bus,
        )
        controller.main()

        if deep_link:
            self._client.write(deep_link.encode())

        self.exec()

    def handle_deep_link(self):
        while self._server.hasPendingConnections():
            client = self._server.nextPendingConnection()
            if client.waitForReadyRead():
                content = client.readAll().data().decode()

                # check schema
                try:
                    url = urlparse(content)
                    if not all([url.scheme == "audiolibrary", url.netloc]):
                        raise ValueError
                except ValueError:
                    logging.warning(f"[Server] Invalid DeepLink: {content}")
                    return
                logging.info(f"[Server] Open DeepLink: {content}")

                # Match url.netloc
                match url.netloc:
                    case "album":
                        self.deeplink_event_bus.album.emit(url.path.replace("/", ""))
                    case "track":
                        self.deeplink_event_bus.track.emit(url.path.replace("/", ""))
                    case "news":
                        self.deeplink_event_bus.news.emit(url.path.replace("/", ""))
                    case _:
                        logging.warning(f"[Server] Invalid DeepLink: {content}")
                        return

    def __del__(self):
        logging.info("[Server] Closing server")
        if self._server:
            self._server.close()
            QLocalServer.removeServer(self.__class__.__name__)


if __name__ == '__main__':
    AudioLibraryApp(sys.argv)
