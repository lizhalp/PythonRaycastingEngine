
import tkinter as tk
from view import View

class Model:
    def __init__(self, gameMap: list[list[int]], x, y) -> None:
        self.map = gameMap
        self.view = View(gameMap, x, y)

class Screen:
    """
    Note: Do not modify any values in Model within the methods
    of this class, doing so violates the principles of the 
    model-view-controller archtiecture
    """
    def __init__(self, model: Model) -> None:
        self.model = model
        self.root = tk.Tk(screenName="Tkinter Raycasting Demo")
        self.root.geometry("1024x768")
        self.mainCanvas = tk.Canvas(width=1024, height=768)
        self.textures = ["red", "blue", "green", "purple"]
        self.mainCanvas.pack()
        for line in self.model.view.castRays():
            self.mainCanvas.create_line(
                line[0], line[1], line[2], line[3],
                fill = self.textures[line[4]]
            )

    def drawLines(self) -> None:
        """Draw the player's current view on the canvas"""
        self.mainCanvas.delete("all")
        for line in self.model.view.castRays():
            self.mainCanvas.create_line(
                line[0], line[1], line[2], line[3], 
                fill = self.textures[line[4]]
            )

class Controller:
    """Given user inputs, modify the Model"""
    def __init__(self, model: Model, screen: Screen) -> None:
        self.model = model
        self.screen = screen

#---------KB Bindings----------#

        def moveForwardUpdate(e):
            self.model.view.moveForward()
            self.screen.drawLines()
    
        def moveBackUpdate(e):
            self.model.view.moveBack()
            self.screen.drawLines()
        
        def lookLeftUpdate(e):
            self.model.view.lookLeft()
            self.screen.drawLines()

        def lookRightUpdate(e):
            self.model.view.lookRight()
            self.screen.drawLines()
        
        def toggleSprinting(e):
            if self.model.view.isSprinting == False:
                self.model.view.isSprinting = True
                self.model.view._movSpeed = .2
            else:
                self.model.view._movSpeed = .1
                self.model.view.isSprinting = False




        self.screen.root.bind("<w>", moveForwardUpdate)
        self.screen.root.bind("<a>", lookRightUpdate)
        self.screen.root.bind("<s>", moveBackUpdate)
        self.screen.root.bind("<d>", lookLeftUpdate)
        self.screen.root.bind("<r>", toggleSprinting)



if __name__ == "__main__":
    gameMap = [
        [1, 1, 1, 1, 1],
        [1, 0, 2, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1]
    ]
    model = Model(gameMap, 1, 1)
    screen = Screen(model)
    controller = Controller(model, screen)
    screen.root.mainloop()