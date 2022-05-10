import pygame
from Events import Events
import gameobject
from item import Item, PlantItem, SeedItem
from mouse import Mouse
import time
from pathfinding import Pathfinding

from report import Report
from tilemapEditor import Grid


class GameManager():
    time = 0
    lastTime = 0
    deltaTime = 0
    scale = 2
    farmer = None
    grid = None
    grid_collider = None

    def updateTime():
        GameManager.lastTime = GameManager.time
        GameManager.time = time.time()
        GameManager.deltaTime = GameManager.time - GameManager.lastTime

    def handleClick(gameObject):
        # pega a posição do mouse
        v2_mousePos = Mouse.getMousePos()

        # if GameObject in type(gameObject).mro():
        #     if gameObject.clickable == False:
        #         return

        if GameManager.farmer != None:
            if Mouse.clicked(0):
                GameManager.farmer.handleClick(gameObject, v2_mousePos)

    def loop():
        GameManager.updateTime()
        # objeto que está sob o mouse
        go_sob_mouse = None

        # for em todos os objetos pra achar o ULTIMO objeto que está sob o mouse
        for go in gameobject.GameObject.all_objects:
            # Verifica se o mouse está posicionado sobre o objeto
            if go.clickable and go.isPointInside(Mouse.getMousePos()):
                go_sob_mouse = go
        
        GameManager.handleClick(go_sob_mouse)

        for go in gameobject.GameObject.all_objects:
            go.loop()

        for item in Item.all_itens:
            if item.isCollide(GameManager.farmer):
                if GameManager.farmer.canAddToInventory():
                    if type(item) == PlantItem:
                        # Coletar planta
                        Item.all_itens.remove(item)
                        gameobject.GameObject.all_objects.remove(item)
                        Report.harvestReport(item.name)

                    elif type(item) == SeedItem:
                        # Reportar no relatorio ( talvez )
                        GameManager.farmer.addToInventory(item)
                        Item.all_itens.remove(item)
                        gameobject.GameObject.all_objects.remove(item)
