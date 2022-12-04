"""
View class manages movement and raycasting,
assumes View is in a two dimensional list representing
the game world
"""

import math


class View:
    def __init__(self, map: list[list[int]], x: float, y: float, 
                 width: int=1024, height: int=768) -> None:
        """
        Params: 
            map: 2d list of ints representing the game world. ints are texture codes.
                 empty space must be 0
            x: x-position of character as a fractional index in map
            y: y-position of character as a fractional index in map
            width: width of the screen in pixels, determines number 
                    of vertical lines from self.castRays()
            height: height of the screen in pixels, determines length
                    of vertical lines from self.castRays() 
        Returns:
            View object
        """
        
        #map vars
        self._width = width
        self._height = height
        self.map = map 
        
        #player vars
        self._movSpeed = .1
        self._rotSpeed = 0.075

        self.posX = x
        self.posY = y
        self.dirX = 1.0
        self.dirY = 0.0
        self.absX = 0.0
        self.absY = .66

        #turning constants

        self.regTurnX = math.cos(self._rotSpeed)
        self.regTurnY = math.sin(self._rotSpeed)
        self.invTurnX = math.cos(-self._rotSpeed)
        self.invTurnY = math.sin(-self._rotSpeed)
    
    def _rotate(self, theta: float):
        """
        Preforms rotation of player perspective by a given number of radians
        """
        oldy = self.dirY
        #x1 = x0 * cos(theta) - y0 * sin(theta)
        self.dirX = self.dirX * math.cos(theta) - oldy * math.sin(theta)
        #y1 = x0 * sin(theta) + y0 * cos(theta)
        self.dirY = self.dirX * math.sin(theta) + oldy * math.cos(theta)
        #Rotate camera view
        oldAbsy = self.absY
        self.absX = self.absX * math.cos(theta) - oldAbsy * math.sin(theta)
        self.absY = self.absX * math.sin(theta) + oldAbsy * math.cos(theta)

    def lookLeft(self):
        #rotate the player view to the left
        stepAngle = self._rotSpeed
        self._rotate(stepAngle)
    
    def lookRight(self):
        #rotate the player view to the right
        stepAngle = -self._rotSpeed
        self._rotate(stepAngle)

    def moveForward(self):
        #Move the player forward (NOT ROTATION)
        mapX = int(self.posX + self.dirX * self._movSpeed)
        mapY = int(self.posY + self.dirY * self._movSpeed)
        if self.map[mapX][mapY] == 0:
            self.posX += self.dirX * self._movSpeed
            self.posY += self.dirY * self._movSpeed

        if self.map[mapX][mapY] == 5:
            self.app.newLevel = True
            self.app.score += 1
    
    def moveBack(self):
        #Move the player backward (NOT ROTATION)
        mapX = int(self.posX - self.dirX * self._movSpeed)
        mapY = int(self.posY - self.dirY * self._movSpeed)
        if self.map[mapX][mapY] == 0:
            self.posX -= self.dirX * self._movSpeed
            self.posY -= self.dirY * self._movSpeed
        
        if self.map[mapX][mapY] == 5:
            self.app.newLevel = True
            self.app.score += 1 
            
    def moveLeft(self): 
        #Move the player left (NOT ROTATION)
        if not self.map[int(self.posX - self.dirX * self._movSpeed)][int(self.posY)]:
            self.posX -= self.dirX * self._movSpeed
        if not self.map[int(self.posX)][int(self.posY + self.dirY * self._movSpeed)]:
            self.posY += self.dirY * self._movSpeed
     
    def moveRight(self):
        #Move the player right (NOT ROTATION)
        if not self.map[int(self.posX + self.dirX * self._movSpeed)][int(self.posY)]:
            self.posX += self.dirX * self._movSpeed

        if not self.map[int(self.posX)][int(self.posY - self.dirY * self._movSpeed)]:
            self.posY -= self.dirY * self._movSpeed
    
    def castRays(self):
        coordinates = []
        for i in range(self._width): 
            mapX = int(self.posX)
            mapY = int(self.posY)
            plrX = (2*i) / self._width - 1
            rayDirX = self.dirX + self.absX * plrX + 0.00001

            #avoid zero division error with raydiry
            rayDirY = self.dirY + self.absY * plrX + 0.00001 

            #calculate slope of ray
            dx = math.sqrt(1 + rayDirY**2/rayDirX**2)
            dy = math.sqrt(1 + rayDirX**2/rayDirY**2)
            
            #Handle negative slopes
            if rayDirX < 0:
                stepX = -1
                sideDistX = (self.posX - mapX) * dx
            else:
                stepX = 1
                sideDistX = (mapX + 1.0 - self.posX) * dx
            if rayDirY < 0:
                stepY = -1
                sideDistY = (self.posY - mapY) * dy
            else:
                stepY = 1
                sideDistY = (mapY + 1.0 - self.posY) * dy
            
            #Cast the ray
            contact = False
            while not contact:
                if sideDistX < sideDistY:
                    mapX += stepX
                    sideDistX += dx
                    side = 0

                else:
                    sideDistY += dy
                    mapY += stepY
                    side = 1
                if mapX < 0 or mapX >= len(self.map) or mapY < 0 or mapY >= len(self.map[0]):
                    contact = True
                    break
                if self.map[mapX][mapY] != 0:
                    contact = True

            #Calculate the distance to the wall
            if side == 0:
                perpWallDist = abs((mapX - self.posX + (1 - stepX) / 2) / rayDirX)
            else:
                perpWallDist = abs((mapY - self.posY + (1 - stepY) / 2) / rayDirY)
            
            #Calculate the height of the line on the screen
            #Add .00001 to avoid ZDE
            h = abs(int(self._height / (perpWallDist + 0.00001)))

            #Calculate the lowest and highest pixel to fill in the line
            drawStart = int(self._height / 2 - h / 2)
            drawEnd = int(self._height / 2 + h / 2)

            if drawStart < 0: 
                drawStart = 0
            if drawEnd >= self._height:
                drawEnd = self._height - 1
            
            #Return the coordinates of the line to be drawn 
            coordinates.append((i, drawStart, i, drawEnd, self.map[mapX][mapY]))
        return coordinates