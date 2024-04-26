# -*- coding: utf-8 -*i-
# convert_model.py

import logging as logger
import shotgun_api3
import urllib


class ShotgunAction:
    def __init__(self, url):
        self.url = url
        self.sg = self.connect_Shotgrid()

    def connect_Shotgrid(self):
        SERVER_PATH = "https://west-intern.shotgrid.autodesk.com"
        SCRIPT_NAME = 'sunhee_api'
        SCRIPT_KEY = 'jfvGltb_yxpbpshzytrhja6on'
        return shotgun_api3.Shotgun(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY)

    def get_entitiy_info(self, entity_type: str, id: str, fields: list):
        return self.sg.find_one(entity_type, [['id', 'is', int(id)]], fields)

    def parse_url(self):
        try:
            protocol, path = self.url.split(":", 1)
            logger.info("protocol: %s" % protocol)

            action, params = path.split("?", 1)
            action = action.strip("/")
            logger.info("action: %s" % action)

            params = params.split("&")
            p = {"column_display_names": [], "cols": []}
            for arg in params:
                key, value = map(urllib.parse.unquote, arg.split("=", 1))
                if key == "column_display_names" or key == "cols":
                    p[key].append(value)
                else:
                    p[key] = value
            params = p
            logger.info("params: %s" % params)
            return protocol, action, params
        except ValueError:
            logger.error("URL parsing error: Invalid URL format")
            return None, None, {}

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "default_url"
    app = QApplication(sys.argv)
    if url != "default_url":
        cc = CovertController(url)
        sys.exit(app.exec_())
    else:
        print("No valid URL provided. Please provide a valid ShotGrid URL.")    
