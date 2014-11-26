#!/usr/bin/python
# -*- coding: utf-8 -*-

# Strażnik
if __name__ == "__main__":
    print "Ostrzeżenie: aby uruchomić aplikację uruchmo skrypt o nazwie \"Arkanoid.py\"!"
    quit()

import json
import os


class GeneralSettings(object):
    _instance = None

    def __init__(self):
        filePath = os.path.dirname(os.path.realpath(__file__))
        filePath += "/samples/"

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(GeneralSettings, cls).__new__(cls)

        return cls._instance

    def getLives(self):
        return self._lives

    def getCheats(self):
        if self._cheats == 1:
            return True
        else:
            return False

    def setIsQuite(self, isQuite):
        self._isQuite = isQuite

    def load(self):
        filePath = self.__getFilePath()

        if os.path.isfile(filePath):
            f = open(filePath, 'r')
            self.__fromJson(f.read())
            f.close()
        else:
            self.save()

    def save(self):
        if not os.path.exists(self.__getPath()):
            os.makedirs(self.__getPath())

        f = open(self.__getFilePath(), 'w')
        f.write(self.__toJson())
        f.close()

    def __toJson(self):
        data = {
            "GeneralSettings": {
                "Lives": self._lives,
                "Cheats": self._cheats}}
        return json.dumps(data, sort_keys=False, indent=2)

    def __fromJson(self, jsonStr):
        try:
            data = json.loads(jsonStr)
            self._lives = data["GeneralSettings"]["Lives"]
            self._cheats = data["GeneralSettings"]["Cheats"]
        except:
            if not self._isQuite:
                print "Settings::__fromJson - Parsowanie pliku nie powiodło się!"

    def __getPath(self):
        path = os.path.expanduser("~")
        path += "/.zr/Arkanoid/"
        return path

    def __getFilePath(self):
        path = self.__getPath()
        path += "Settings.json"
        return path

    _samplesPath = None
    _isQuite = False

    _lives = 3
    _cheats = 1
