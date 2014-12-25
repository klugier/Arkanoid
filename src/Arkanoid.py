#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import imp

import Game
import Settings

def main():
    isHelp = False
    isQuite = False
    isVersion = False
    
    i = 0
    for arg in sys.argv:
        if i > 0:
            if arg == "-h" or arg == "--help":
                isHelp = True
            elif arg == "-q" or arg == "--quite":
                isQuite = True
            elif arg == "-v" or arg == "--version":
                isVersion = True
        i += 1
    
    if isVersion:
        if not isQuite:
            sys.stdout.write(
                "Arkandoid - wersja 1.0\n")
        quit()
    elif isHelp:
        if not isQuite:
            sys.stdout.write(
                "Pomoc programu Arkanoid - Zbigniew Rębacz\n\n")
            sys.stdout.write("Opis:\n")
            sys.stdout.write(
                "Gra polegająca na odbijaniu piłeczki od paletki, w celu zbicia wszystki bloków w obrębie danego poziomu.\n")
            sys.stdout.write(
                "Do uruchomienia wymagany jest moduł \"pygame\". (Pod ubuntu: sudo apt-get install pygames)\n\n")
            sys.stdout.write("Pliki konfiguracyjne:\n")
            sys.stdout.write(
                "~/zr/Arkanoid/Settings.json - plik konfiguracyjny pozwalający na modyfikację niektórych opcji gry.\n")
            sys.stdout.write(
                "levels/*                    - pliki tekstowe zawierające opis poziomów.\n\n")
            sys.stdout.write("Sterowanie:\n")
            sys.stdout.write("Stzałka w lewo  - ruch paletki w lewo\n")
            sys.stdout.write("Stzałka w prawo - ruch paletki w prawo\n")
            sys.stdout.write("Spacja          - odbija początkową piłkę\n")
            sys.stdout.write("p               - wszytrzymuje grę\n\n")
            sys.stdout.write("Kody:\n")
            sys.stdout.write("F11             - wygrywa poziom\n\n")
        quit()

    try:
        imp.find_module("pygame")
    except ImportError:
        sys.stdout.write(
            "Moduł \"pygame\" nie istnieje. W celu zainstalowania brakującego modułu skontaktuj się z administratorem twoejgo systemu.\n\n")
        quit()

    # Właściwa część programu
    settings = Settings.GeneralSettings()
    settings.setIsQuite(isQuite)
    settings.load()

    arkanoid = Game.Arkanoid()
    arkanoid.setIsQuite(isQuite)
    arkanoid.init()
    arkanoid.run(800, 600)

    settings.save()

if __name__ == "__main__":
    main()
