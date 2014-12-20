#!/usr/bin/python
# -*- coding: utf-8 -*-

# Strażnik
if __name__ == "__main__":
    print "Ostrzeżenie: aby uruchomić aplikację uruchmo skrypt o nazwie \"Arkanoid.py\"!"
    quit()

import pygame
import os
import sys
import random

from pygame.locals import *

import Settings

class Colision(object):
    """
    Klasa reprezentująca kolizję w grze.
    Posiada informację z jakiego typu kolizją mamy do czynienia co pozwala
    podjąć odpowiednią decyzję np. w którą stronę należy odbić piłkę.
    """

    def __init__(self, left, right, top, bottom):
        self._left = left
        self._right = right
        self._top = top
        self._bottom = bottom

    def isLeftColision(self):
        return self._left

    def isRightColision(self):
        return self._right

    def isTopColision(self):
        return self._top

    def isBottomColision(self):
        return self._bottom

    def isAny(self):
        if self._left or self._right or self._top or self._bottom:
            return True
        else:
            return False

    _left = None
    _right = None
    _top = None
    _bottom = None


class GameObject(object):
    """
    Wyjściowa klasa dla wszystkich obiektów gry.
    """
    
    def __init__(self, left, right, top, bottom):
        self.setRect(left, right, top, bottom)
        self._color = pygame.Color(255, 255, 255)
        self._speedX = 0
        self._speedY = 0

    def setRect(self, left, right, top, bottom):
        self._left = left
        self._right = right
        self._top = top
        self._bottom = bottom

    def setColor(self, color):
        self._color = color

    def setSpeedX(self, speedX):
        self._speedX = speedX

    def setSpeedY(self, speedY):
        self._speedY = speedY

    def getLeft(self):
        return self._left

    def getRight(self):
        return self._right

    def getTop(self):
        return self._top

    def getBottom(self):
        return self._bottom

    def getSpeedX(self):
        return self._speedX

    def getSpeedY(self):
        return self._speedY

    def moveAboutTheSpeed(self):
        self._left = self._left + self._speedX
        self._right = self._right + self._speedX
        self._top = self._top + self._speedY
        self._bottom = self._bottom + self._speedY

    def move(self, x, y):
        self._left = self._left + x
        self._right = self._right + x
        self._top = self._top + y
        self._bottom = self._bottom + y

    def isColision(self, gameObject):
        left = False
        right = False
        top = False
        bottom = False

        if self._speedX < 0:
            newLeft = self._left + self._speedX
            if gameObject._right >= 0 and newLeft < gameObject._right:
                centerY = self._top + (self._bottom - self._top) / 2
                if gameObject._top < 0 or gameObject._bottom < 0:
                    left = True
                elif newLeft > gameObject._left:
                    if centerY > gameObject._top and centerY < gameObject._bottom:
                        left = True
        elif self._speedX > 0:
            newRight = self._right + self._speedX
            if gameObject._left >= 0 and newRight > gameObject._left:
                centerY = self._top + (self._bottom - self._top) / 2
                if gameObject._top < 0 or gameObject._bottom < 0:
                    right = True
                elif newRight < gameObject._right:
                    if centerY > gameObject._top and centerY < gameObject._bottom:
                        right = True

        if self._speedY < 0:
            newTop = self._top + self._speedY
            if gameObject._bottom >= 0 and newTop < gameObject._bottom:
                centerX = self._left + (self._right - self._left) / 2
                if gameObject._left < 0 or gameObject._right < 0:
                    top = True
                elif newTop > gameObject._top:
                    if centerX > gameObject._left and centerX < gameObject._right:
                        top = True

        elif self._speedY > 0:
            newBottom = self._bottom + self._speedY
            if gameObject._top >= 0 and newBottom > gameObject._top:
                centerX = self._left + (self._right - self._left) / 2
                if gameObject._left < 0 or gameObject._right < 0:
                    bottom = True
                elif newBottom < gameObject._bottom:
                    if centerX > gameObject._left and centerX < gameObject._right:
                        bottom = True

        return Colision(left, right, top, bottom)

    def draw(self):
        pass

    _left = None
    _right = None
    _top = None
    _bottom = None

    _color = None

    _speedX = None
    _speedY = None


class Block(GameObject):
    """
    Klasa reprezentuje blok w grze. Celem gracza jest zniszczenie wszystkich
    obiektów tego typu na danej planszy.
    """
    
    def __init__(self, left, right, top, bottom):
        super(self.__class__, self).__init__(left, right, top, bottom)

    def getPoints(self):
        return self._points

    def setColor(self, color):
        self._color = color

    def setLines(self, lines, linesColor):
        self._lines = lines
        self._linesColor = linesColor

    def setPoints(self, points):
        self._points = points

    def draw(self, dpy):
        width = self._right - self._left
        height = self._bottom - self._top

        pygame.draw.rect(
            dpy,
            self._color,
            (self._left,
             self._top,
             width,
             height))
        if self._lines:
            pygame.draw.line(
                dpy,
                self._linesColor,
                (self._left,
                 self._top),
                (self._right,
                 self._top),
                2)
            pygame.draw.line(
                dpy,
                self._linesColor,
                (self._left,
                 self._bottom),
                (self._right,
                 self._bottom),
                2)
            pygame.draw.line(
                dpy,
                self._linesColor,
                (self._left,
                 self._top),
                (self._left,
                 self._bottom),
                2)
            pygame.draw.line(
                dpy,
                self._linesColor,
                (self._right,
                 self._top),
                (self._right,
                 self._bottom),
                2)

    _lines = False
    _linesColor = None
    _color = None

    _points = None


class Ball(GameObject):
    """
    Klasa reprezentuje piłkę, czyli obiekt który porusza się po planszy i rozbija
    bloki.
    """
    
    def __init__(self, left, right, top, bottom):
        super(self.__class__, self).__init__(left, right, top, bottom)
        self._r = int((self._right - self._left) / 2)

    def setBorder(self, border, borderColor):
        self._border = True
        self._borderColor = borderColor

    def draw(self, dpy):
        x = int(self._left + ((self._right - self._left) / 2))
        y = int(self._top + ((self._bottom - self._top) / 2))

        width = self._right - self._left
        height = self._bottom - self._top

        pygame.draw.circle(dpy, self._color, (x, y), self._r, 0)
        if self._border:
            pygame.draw.circle(dpy, self._borderColor, (x, y), self._r, 1)

    _r = None
    _border = False
    _borderColor = None


# **********************************************************************

class Arkanoid(object):
    """
    Klasa gry. Zawiera całą logikę obsługę zdarzeń. Ponadto odpowiada za wywoływanie
    metod rysujących.
    """
    
    def init(self):
        pygame.init()
        # os.environ['SDL_VIDEO_CENTERED'] = '1'

        self._fpsClock = pygame.time.Clock()
        self._fps = 60
        self._levelColor = pygame.Color(0, 0, 0)

        self._isQuite = False

    def setIsQuite(self, quite):
        self._isQuite = quite

    def run(self, cx, cy):
        # Inicjalizacja
        self.cx = cx
        self.cy = cy

        try:
            self.dpy = pygame.display.set_mode((self.cx, self.cy))
            pygame.display.set_caption("Arkanoid - Zbigniew Rębacz")
        except pygame.error:
            if not self._isQuite:
                print "Błąd krytyczny: Nie udało się utworzyć okna!"
            quit()

        self._fontInterfaceHuge = pygame.font.SysFont("sansserif", 100)
        self._fontInterfaceBig = pygame.font.SysFont("sansserif", 45)
        self._fontInterface = pygame.font.SysFont("sansserif", 24)
        self._fontInterfaceSmall = pygame.font.SysFont("sansserif", 22)

        # Inicjalizacja zmiennych gry
        while True:
            self._gameLives = int(Settings.GeneralSettings().getLives())
            self._gameScore = 0
            self._gameOver = False
            self._gameRestart = False

            self._levelLast = False
            breakLevelLoop = False
            levelList = self.__listLevels()

            i = 0
            for level in levelList:
                if i + 1 == len(levelList):
                    self._levelLast = True

                self.__loadLevel(level)
                self.__loadPaddle()
                self.__loadBall()
                self._leftDown = False
                self._rightDown = False
                while True:
                    if self._levelLast and len(self._levelBlocks) == 0:
                        self._gameVictory = True
                    elif len(self._levelBlocks) == 0:
                        break

                    if self.__analyzeEvent():
                        breakLevelLoop = True
                        break

                    self.__drawScene()
                    self.__moveBall()

                    pygame.display.update()
                    self._fpsClock.tick(self._fps)
                if breakLevelLoop:
                    break
                i = i + 1

            if not self._gameRestart:
                break

    def __analyzeEvent(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return True
            elif event.type == KEYDOWN:
                if self._gameOver or self._gameVictory:
                    if event.key == K_ESCAPE:
                        return True
                    elif event.key == K_RETURN:
                        self._gameVictory = False
                        self._gameOver = False
                        self._gameRestart = True
                        return True
                else:
                    if event.key == K_SPACE:
                        self.__startBall()
                    elif event.key == K_LEFT:
                        self._leftDown = True
                    elif event.key == K_RIGHT:
                        self._rightDown = True
                    elif event.key == K_p:
                        self._gamePause = not self._gamePause
                    elif event.key == K_F11:
                        if Settings.GeneralSettings().getCheats():
                            self._levelBlocks = []
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    self._leftDown = False
                elif event.key == K_RIGHT:
                    self._rightDown = False

        if not self._gamePause:
            if self._leftDown:
                self.__movePaddle(-5)
            if self._rightDown:
                self.__movePaddle(5)

    def __drawScene(self):
        if self._gameOver or self._gameVictory:
            self.dpy.fill((0, 0, 0))
        else:
            self.dpy.fill(self._levelColor)

        self.__drawPanel()

        if self._gameOver:
            self.__drawGameOver()
            return

        if self._gameVictory:
            self.__drawVictory()
            return

        self._levelBall.draw(self.dpy)
        self._levelPaddle.draw(self.dpy)
        for block in self._levelBlocks:
            block.draw(self.dpy)

    def __drawGameOver(self):
        top = (self.cy / 30) * 3
        color = pygame.Color(255, 42, 0)

        gameOver = self._fontInterfaceHuge.render("Game Over!", True, color)
        score = self._fontInterfaceBig.render(
            "Your score: " + str(self._gameScore), True, color)
        info = self._fontInterface.render(
            "[ Press ESC to quit or Enter to play again ]",
            True,
            color)

        y = (self.cy + top - gameOver.get_height() -
             score.get_height() - info.get_height()) // 2
        y2 = y + gameOver.get_height() + 3
        self.dpy.blit(gameOver, ((self.cx - gameOver.get_width()) // 2, y))
        self.dpy.blit(score, ((self.cx - score.get_width()) // 2, y2))
        self.dpy.blit(
            info,
            ((self.cx - info.get_width()) // 2,
             y2 + score.get_height() + 3))

    def __drawVictory(self):
        top = (self.cy / 30) * 3
        color = pygame.Color(28, 127, 0)

        gameOver = self._fontInterfaceHuge.render("Victory!", True, color)
        score = self._fontInterfaceBig.render(
            "Your score: " + str(self._gameScore), True, color)
        info = self._fontInterface.render(
            "[ Press ESC to quit or Enter to play again ]",
            True,
            color)

        y = (self.cy + top - gameOver.get_height() -
             score.get_height() - info.get_height()) // 2
        y2 = y + gameOver.get_height() + 3
        self.dpy.blit(gameOver, ((self.cx - gameOver.get_width()) // 2, y))
        self.dpy.blit(score, ((self.cx - score.get_width()) // 2, y2))
        self.dpy.blit(
            info,
            ((self.cx - info.get_width()) // 2,
             y2 + score.get_height() + 3))

    def __drawPanel(self):
        height = (self.cy / 30) * 3
        color = pygame.Color(140, 140, 140)

        levelName = self._fontInterface.render(self._levelName, True, color)
        score = self._fontInterfaceSmall.render(
            "Score: " + str(self._gameScore), True, color)
        lives = self._fontInterfaceSmall.render(
            "Lives: " + str(self._gameLives), True, color)

        pygame.draw.rect(
            self.dpy, pygame.Color(
                0, 0, 0), (0, 0, self.cx, height))
        pygame.draw.rect(
            self.dpy, pygame.Color(
                170, 85, 0), (0, height - 3, self.cx, 3))

        self.dpy.blit(
            levelName, ((self.cx - levelName.get_width()) // 2, 8))
        self.dpy.blit(score, (10, height - 10 - score.get_height()))
        self.dpy.blit(
            lives,
            ((self.cx - lives.get_width() - 10),
             height - 10 - lives.get_height()))

    def __findLevelPath(self):
        levelPath = os.path.dirname(os.path.realpath(__file__))
        levelPath += "/levels/"
        return levelPath

    def __loadLevel(self, levelFile):
        self.__loadLevel0(self.__findLevelPath() + levelFile)

    def __listLevels(self):
        levels = []
        for level in sorted(os.listdir(self.__findLevelPath())):
            levels.append(level)
        return levels

    def __loadLevel0(self, levelPath):
        try:
            content = []

            with open(levelPath) as f:
                content = f.readlines()

            if content:
                self._levelBlocks = []
                self._levelColor = pygame.Color(28, 85, 0)

                isName = False
                i = 3
                for line in content:
                    firstCharacter = line[0:1]
                    if firstCharacter == "#":
                        continue

                    if not isName:
                        self._levelName = line.rstrip()
                        isName = True
                        continue

                    j = 0
                    for c in line:
                        width = self.cx / 20
                        height = self.cy / 30

                        left = j * width
                        right = j * width + width
                        top = i * height
                        bottom = i * height + height

                        if c == "*":
                            block = Block(left, right, top, bottom)
                            block.setLines(True, self._levelColor)
                            block.setColor(pygame.Color(255, 170, 0))
                            block.setPoints(100)
                            self._levelBlocks.append(block)
                        elif c == "?":
                            block = Block(left, right, top, bottom)
                            block.setLines(True, self._levelColor)
                            block.setColor(pygame.Color(85, 170, 255))
                            block.setPoints(500)
                            self._levelBlocks.append(block)
                        elif c == "+":
                            block = Block(left, right, top, bottom)
                            block.setLines(True, self._levelColor)
                            block.setColor(pygame.Color(113, 42, 150))
                            block.setPoints(1000)
                            self._levelBlocks.append(block)
                        j += 1

                    i += 1

        except IOError:
            print "Game::__loadLevel0 - nie udało wczytać się pliku z poziomem! (" + levelPath + ")"
            quit()

    def __loadPaddle(self):
        width = self.cx / 10
        height = self.cy / 35

        left = ((self.cx - width) / 2)
        right = left + width
        bottom = self.cy - height
        top = bottom - height

        self._levelPaddle = Block(left, right, top, bottom)
        self._levelPaddle.setLines(True, pygame.Color(85, 42, 0))
        self._levelPaddle.setColor(pygame.Color(141, 42, 0))

    def __movePaddle(self, value):
        leftTemp = self._levelPaddle.getLeft()
        rightTemp = self._levelPaddle.getRight()

        left = self._levelPaddle.getLeft() + value
        right = self._levelPaddle.getRight() + value
        top = self._levelPaddle.getTop()
        bottom = self._levelPaddle.getBottom()

        width = right - left

        ballValue = value
        if left < 0:
            ballValue = 0
            left = 0
            right = width
        elif right > self.cx:
            ballValue = 0
            left = self.cx - width
            right = self.cx

        if self._levelBallStop:
            self._levelBall.move(ballValue, 0)

        self._levelPaddle.setRect(left, right, top, bottom)

    def __loadBall(self):
        width = self.cx * 0.02
        height = width

        left = ((self.cx - width) / 2)
        right = left + width
        bottom = self._levelPaddle.getTop()
        top = bottom - height

        self._levelBall = Ball(left, right, top, bottom)
        self._levelBall.setBorder(True, pygame.Color(0, 0, 0))
        self._levelBall.setColor(pygame.Color(226, 85, 0))
        self._levelBallStop = True

    def __startBall(self):
        if self._levelBallStop:
            num = random.randint(0, 1)
            if num == 0:
                self._levelBall.setSpeedX(-1)
            else:
                self._levelBall.setSpeedX(1)
            self._levelBall.setSpeedY(-4)

            self._levelBallStop = False
            self.__moveBall()

    def __moveBall(self):
        if not self._levelBallStop:
            LeftWall = GameObject(-1, 0, -1, -1)
            RightWall = GameObject(self.cx, -1, -1, -1)
            TopWall = GameObject(-1, -1, -1, (self.cy / 30) * 3)
            BottomWall = GameObject(-
                                    1, -
                                    1, self.cy +
                                    self._levelBall.getBottom() -
                                    self._levelBall.getTop(), 0)

            colision = self._levelBall.isColision(self._levelPaddle)
            if colision.isLeftColision() or colision.isRightColision():
                self._levelBall.setSpeedX(-1 * self._levelBall.getSpeedX())
            elif colision.isBottomColision() or colision.isTopColision():
                pLeft = self._levelPaddle.getLeft()
                pRight = self._levelPaddle.getRight()
                pLength = pRight - pLeft
                bCenter = self._levelBall.getLeft() + ((self._levelBall.getRight() -
                          self._levelBall.getLeft()) / 2) + self._levelBall.getSpeedX()

                step = int(pLength / 8)
                # print str(pLeft) + " " + str(bCenter) + " " + str(pRight)
                # + " Step: " + str(step)
                for i in range(8):
                    if bCenter >= pLeft + i * \
                            step and bCenter <= pLeft + ((i + 1) * step):
                        # print "Kolizja"
                        if -4 + i == 0:
                            self._levelBall.setSpeedX(-
                                                      1 *
                                                      self._levelBall.getSpeedX())
                        else:
                            self._levelBall.setSpeedX(-4 + i)
                        break
                self._levelBall.setSpeedY(-1 * self._levelBall.getSpeedY())

            # Odbicie na ścianach
            colision = self._levelBall.isColision(LeftWall)
            if colision.isLeftColision():
                self._levelBall.setSpeedX(-1 * self._levelBall.getSpeedX())

            colision = self._levelBall.isColision(RightWall)
            if colision.isRightColision():
                self._levelBall.setSpeedX(-1 * self._levelBall.getSpeedX())

            colision = self._levelBall.isColision(TopWall)
            if colision.isTopColision():
                self._levelBall.setSpeedY(-1 * self._levelBall.getSpeedY())

            colision = self._levelBall.isColision(BottomWall)
            if colision.isBottomColision():
                self._gameLives = self._gameLives - 1
                if self._gameLives == 0:
                    self._gameOver = True
                self.__loadPaddle()
                self.__loadBall()
                # self._levelBall.setSpeedY(-1 * self._levelBall.getSpeedY())

            for block in self._levelBlocks:
                colision = self._levelBall.isColision(block)
                if colision.isBottomColision() or colision.isTopColision():
                    self._gameScore = self._gameScore + block.getPoints()
                    self._levelBlocks.remove(block)
                    self._levelBall.setSpeedY(- 1 *
                                              self._levelBall.getSpeedY())
                elif colision.isLeftColision() or colision.isRightColision():
                    self._gameScore = self._gameScore + block.getPoints()
                    self._levelBlocks.remove(block)
                    self._levelBall.setSpeedX(-1 *
                                              self._levelBall.getSpeedX())

            if not self._gamePause and not self._gameVictory and not self._gameOver:
                self._levelBall.moveAboutTheSpeed()

    _levelBlocks = []
    _levelColor = None
    _levelBall = None
    _levelBallStop = None
    _levelBallSX = None
    _levelBallSY = None
    _levelPaddle = None
    _levelName = None
    _levelLast = None

    _gameLives = None
    _gamePause = False
    _gameScore = None
    _gameOver = None
    _gameVictory = None
    _gameRestart = None

    _leftDown = None
    _rightDown = None

    _fpsClock = None
    _fps = None

    _fontInterfaceHuge = None
    _fontInterfaceBig = None
    _fontInterface = None
    _fontInterfaceSmall = None

    _isQuite = False

    dpy = None
    cx = None
    cy = None
