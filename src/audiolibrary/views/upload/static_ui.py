from PyQt6 import QtCore, QtWidgets

from audiolibrary.views.widgets import WidgetsFactory


class UiUploadPage:
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
        central_layout.setContentsMargins(50, 50, 50, 0)
        central_layout.setSpacing(10)

        # Body
        from_block = QtWidgets.QWidget()
        from_block.setObjectName("from_block")
        from_block.setStyleSheet("""
            QWidget#from_block {
                background-color: $BG2;
                border-top-left-radius: 15px;
                border-top-right-radius: 15px;
                border: 1px solid $HOVER;
            }
        """.replace(
            "$BG2", widgets_factory.theme.second_background
        ).replace(
            "$HOVER", widgets_factory.theme.hover
        ))
        central_layout.addWidget(from_block)

        from_block_layout = QtWidgets.QVBoxLayout(from_block)
        from_block_layout.setContentsMargins(25, 25, 25, 25)
        from_block_layout.setSpacing(10)

        # Fields
        fields_layout = QtWidgets.QFormLayout()
        fields_layout.setContentsMargins(0, 0, 0, 0)
        fields_layout.setSpacing(10)
        from_block_layout.addLayout(fields_layout)

        # Title
        title_line = widgets_factory.line_edit()
        title_line.setObjectName("title_line")
        title_line.setPlaceholderText("ex. My song")
        self.title_line = title_line

        self.title_label = widgets_factory.label()
        fields_layout.addRow(self.title_label, title_line)

        # Description
        description_text = widgets_factory.textarea()
        description_text.setPlaceholderText("ex. My description")
        description_text.setMaximumHeight(100)
        self.description_text = description_text

        self.description_label = widgets_factory.label()
        fields_layout.addRow(self.description_label, description_text)

        # Artist
        artist_block = QtWidgets.QWidget()
        artist_block.setObjectName("artist_block")
        artist_block.setFixedWidth(200)
        artist_block.setStyleSheet("""
            QWidget#artist_block {
                background-color: transparent;
                border-radius: 5px;
                border: 1px solid $HOVER;
            }
        """.replace(
            "$HOVER", widgets_factory.theme.hover
        ))
        artist_block_layout = QtWidgets.QHBoxLayout(artist_block)
        artist_block_layout.setContentsMargins(5, 5, 5, 5)

        artist_list = widgets_factory.list()
        artist_list.add_style("""
            QListView {
                background-color: $BG1;
                border-top-left-radius: 5px;
                border-bottom-left-radius: 5px;
            }
        """.replace(
            "$BG1", widgets_factory.theme.first_background
        ))
        artist_list.setMaximumHeight(100)
        artist_block_layout.addWidget(artist_list)
        self.artist_list = artist_list

        # Artist tools
        artist_tools_layout = QtWidgets.QVBoxLayout()
        artist_block_layout.addLayout(artist_tools_layout)

        artist_add_button = widgets_factory.button()
        artist_add_button.setText("+")
        artist_tools_layout.addWidget(artist_add_button)
        artist_tools_layout.addStretch(1)

        self.artist_label = widgets_factory.label()

        fields_layout.addRow(self.artist_label, artist_block)


        # File
        file_block = widgets_factory.file_select_box()
        self.file_block = file_block
        from_block_layout.addWidget(file_block)

        # Rules Policy
        rules_block = QtWidgets.QWidget()
        rules_block.setObjectName("rules_block")
        rules_block.setStyleSheet("""
            QWidget#rules_block {
                background-color: $BG1;
                border-radius: 5px;
                border: 1px solid $HOVER;
            }
        """.replace(
            "$BG1", widgets_factory.theme.first_background
        ).replace(
            "$HOVER", widgets_factory.theme.hover
        ))
        from_block_layout.addWidget(rules_block)
        from_block_layout.addStretch(1)

        # Controls
        controls_layout = QtWidgets.QHBoxLayout()
        controls_layout.setContentsMargins(0, 0, 0, 0)

        # Reset Button
        reset_button = widgets_factory.button()
        self.reset_button = reset_button
        controls_layout.addWidget(reset_button)
        controls_layout.addStretch(1)

        # Send Button
        send_button = widgets_factory.primary_button()
        self.send_button = send_button
        controls_layout.addWidget(send_button)

        from_block_layout.addLayout(controls_layout)






        self.translate_ui(page)
        QtCore.QMetaObject.connectSlotsByName(page)

    def translate_ui(self, page: QtWidgets.QWidget):
        _translate = QtCore.QCoreApplication.translate
        page.setWindowTitle(_translate("upload_page_title", "Загрузка"))
        self.title_label.setText(_translate("upload_page_audio_title", "Название"))
        self.description_label.setText(_translate("upload_page_audio_description", "Описание"))
        self.artist_label.setText(_translate("upload_page_audio_artist", "Исполнитель(и)"))
        self.reset_button.setText(_translate("upload_page_audio_reset", "Сбросить"))
        self.send_button.setText(_translate("upload_page_audio_send", "Отправить"))
        self.file_block.set_text(_translate("upload_page_audio_file", "Выберите или перетащите файл"))
