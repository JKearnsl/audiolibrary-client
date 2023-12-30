from PyQt6 import QtCore, QtWidgets, QtGui

from audiolibrary.views.widgets import WidgetsFactory


class UiControlPage:
    def setup_ui(self, page: QtWidgets.QWidget, widgets_factory: WidgetsFactory):
        page.setObjectName("page")
        page_layout = QtWidgets.QVBoxLayout(page)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.setSpacing(0)

        customize_sheet = QtWidgets.QWidget(page)
        customize_sheet.setObjectName("customize_sheet")
        customize_sheet.setStyleSheet("""
                QWidget#customize_sheet {
                    background-color: $BG1;
                }
            """.replace(
        "$BG1", widgets_factory.theme.first_background)
        )
        page_layout.addWidget(customize_sheet)

        central_layout = QtWidgets.QVBoxLayout(customize_sheet)
        central_layout.setContentsMargins(20, 20, 20, 20)
        central_layout.setSpacing(10)
        central_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)

        page_layout = QtWidgets.QVBoxLayout()
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.setSpacing(10)
        central_layout.addLayout(page_layout)

        # Body

        self.translate_ui(page)
        QtCore.QMetaObject.connectSlotsByName(page)

    def translate_ui(self, page: QtWidgets.QWidget):
        _translate = QtCore.QCoreApplication.translate
