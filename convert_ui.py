# -*- coding: utf-8 -*-
# convert_ui.py

import sys
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QMessageBox, QComboBox

class Main(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Download mp4")
        self.resize(600, 200)
        self.center()

        vb = QVBoxLayout(self) 

        hbtop = QHBoxLayout()
        vb.addLayout(hbtop)
        self.line_path = QLineEdit()
        self.line_path.setPlaceholderText(".mp4 Storage Path")
        self.btn_save_path = QPushButton("Save_path")
        hbtop.addWidget(self.line_path)
        hbtop.addWidget(self.btn_save_path)

        hbbot = QHBoxLayout()
        vb.addLayout(hbbot)
        hbbot.addStretch()
        self.btn_download=QPushButton("Downloads")
        self.btn_cancel=QPushButton("Cancel")
        hbbot.addWidget(self.btn_download)
        hbbot.addWidget(self.btn_cancel)
        hbbot.addStretch()

        self.setLayout(vb)  

        self.show() 

    def center(self):
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = Main()
    sys.exit(app.exec_())
