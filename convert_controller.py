#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import importlib
import subprocess
import logging as logger

from PySide2.QtWidgets import QApplication, QFileDialog, QMessageBox

import convert_model
import convert_ui

importlib.reload(convert_model)
importlib.reload(convert_ui)

logfile_path = os.path.join(os.path.dirname(sys.argv[0]), "log")
if not os.path.exists(logfile_path):
    os.mkdir(logfile_path)
LOGFILE = os.path.join(logfile_path, "ami_handler_log")


class ConvertController(convert_ui.Main):
    def __init__(self, url):
        super().__init__()
        self.logger = self.init_log(LOGFILE)
        self.model = convert_model.ShotgunAction(url)
        self._dir_path = "/RAPA/test_sunhee_"
        self.connect_btn()
        self.set_data()

    def set_data(self): 
        self.protocol, self.action, self.params = self.model.parse_url()
        
        self.selected_ids = []
        if 'selected_ids' in self.params:
            if len(self.params["selected_ids"]) > 1:
                sids = self.params["selected_ids"].split(",")
                self.selected_ids = [int(id) for id in sids]
            else:
                self.selected_ids = [int(self.params["selected_ids"])]
        else:
            self.selected_ids = []

        self.entity_type = self.params.get("entity_type", None)

    def check_action(self):
        if self.action == 'convert_mp4':
            self.convert()

        else:
            print("No Action")

    def connect_btn(self):
        self.btn_save_path.clicked.connect(self.slot_save_path)
        self.btn_download.clicked.connect(self.convert_video)
        self.btn_cancel.clicked.connect(self.slot_cancel)

    def slot_save_path(self):
        self.dir_path = QFileDialog.getExistingDirectory(None, "Select Save Path", "/RAPA/test_sunhee_", QFileDialog.ShowDirsOnly)
        self.line_path.setText(self.dir_path)

    def slot_cancel(self):
        self.close()

    def convert_video(self):
        for selected_id in self.selected_ids:
            try:
                published_file = self.model.sg.find_one(self.entity_type, [['id', 'is', int(selected_id)]], ['code', 'sg_local_path'])
                if not published_file or not published_file['sg_local_path']:
                    self.logger.error(f"No valid path found for entity ID {selected_id}")
                    continue

                local_file_path = published_file['sg_local_path']
                filename = f"{published_file['code']}.mp4"
                unique_filename = self.generate_unique_filename(self._dir_path, filename) 
                output_path = os.path.join(self._dir_path, unique_filename)

                command = [
                    'ffmpeg',
                    '-framerate', '24', 
                    '-pattern_type', 'glob',
                    '-i', f'{local_file_path}/*.jpg',
                    output_path
                ]
                subprocess.run(command, check=True)
                self.logger.info(f"Video converted successfully: {output_path}")
            except Exception as e:
                self.logger.error(f"Error retrieving ShotGrid data: {e}")

    @staticmethod
    def generate_unique_filename(path, filename):
            original_filename = os.path.splitext(filename)[0]
            file_extension = os.path.splitext(filename)[1]
            counter = 1
            final_filename = filename
            while os.path.exists(os.path.join(path, final_filename)):
                final_filename = f"{original_filename}_{counter}{file_extension}"
                counter += 1
            return final_filename

    def init_log(self, filename):
        logger.basicConfig(
            level=logger.DEBUG,
            format="%(asctime)s %(levelname)s %(message)s",
            datefmt='%Y-%m-%d %H:%M:%S',
            filemode='w'
        )
        return logger
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    url = sys.argv[1] if len(sys.argv) > 1 else "default_url" 
    cc = ConvertController(url)
    sys.exit(app.exec_())

