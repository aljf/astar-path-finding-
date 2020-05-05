# try:
import pygame
import sys
import math
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
# except:
#     import install_requirements
#
#     import pygame
#     import sys
#     import math
#     from tkinter import *
#     from tkinter import ttk
#     from tkinter import messagebox
#     import os

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)

margin = 5
width = 20
height = 20
cols = 25
row = 25


class Tile:
    def __init__(self, x, y):
        self.i = x
        self.j = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.color = white
        self.neighbors = []
        self.previous = None
        self.obs = False
        self.closed = False
        self.value = 1

    def display_tile(self, color, rh):
        pygame.draw.rect(screen, color, (self.i * width, self.j * height, width, height), rh)
        self.color = color
        pygame.display.update()

    def show_red_path(self, rh):
        if self.color == white:
            pygame.draw.rect(screen, red, (self.i * width, self.j * height, width, height), rh)
            self.color = red
            pygame.display.update()

    def addNeighbors(self, grid):
        i = self.i
        j = self.j
        if i < cols - 1 and grid[self.i + 1][j].obs is False:
            self.neighbors.append(grid[self.i + 1][j])
        if i > 0 and grid[self.i - 1][j].obs is False:
            self.neighbors.append(grid[self.i - 1][j])
        if j < row - 1 and grid[self.i][j + 1].obs is False:
            self.neighbors.append(grid[self.i][j + 1])
        if j > 0 and grid[self.i][j - 1].obs is False:
            self.neighbors.append(grid[self.i][j - 1])


def distance_to_end(n, e):
    d = math.sqrt((n.i - e.i)**2 + (n.j - e.j)**2)
    return d


grid = []
for i in range(cols):
    grid.append([])
    for j in range(row):
        grid[i].append(0)
        grid[i][j] = Tile(i, j)


for i in range(cols):
    for j in range(row):
        grid[i][j].addNeighbors(grid)


def astar(grid):

    start_tile.g = start_tile.h = start_tile.f = 0
    end_tile.g = end_tile.h = end_tile.f = 0
    openList = []
    closedList = []

    openList.append(start_tile)
    while len(openList) > 0:
        current_tile = openList[0]
        current_index = 0
        for index, item in enumerate(openList):
            if item.f < current_tile.f:
                current_tile = item
                current_index = index

        openList.pop(current_index)
        closedList.append(current_tile)

        # end found
        if current_tile == end_tile:
            start_tile.display_tile(green, 0)
            for i in range(round(current_tile.f)):
                current_tile.closed = False
                current_tile.display_tile(yellow, 0)
                current_tile = current_tile.previous
            end_tile.display_tile(green, 0)
            break


        neighbors = current_tile.neighbors
        for i in range(len(neighbors)):
            neighbor =neighbors[i]
            if neighbor not in closedList:
                tempG = current_tile.g + current_tile.value
                if neighbor in openList:
                    if neighbor.g > tempG:
                        neighbor.g = tempG
                else:
                    neighbor.g = tempG
                    openList.append(neighbor)
            neighbor.h = distance_to_end(neighbor, end_tile)
            neighbor.f = neighbor.g + neighbor.h

            if neighbor.previous == None:
                neighbor.previous = current_tile
        current_tile.closed = True

    if int_var.get():
        for i in range(len(closedList)):
            if closedList != start_tile:
                closedList[i].show_red_path(0)

        pygame.display.update()
    pass

def onsubmit():
    global end
    global start_tile
    global end_tile
    st = startBox.get().split(',')
    ed = endBox.get().split(',')
    start_tile = grid[int(st[0])][int(st[1])]
    end_tile = grid[int(ed[0])][int(ed[1])]
    start_tile.color = green
    end_tile.color = green
    window.quit()
    window.destroy()


window = Tk()
labelStart = Label(window, text='Start(x,y): ')
startBox = Entry(window)
labelEnd = Label(window, text='End(x,y): ')
endBox = Entry(window)
int_var = IntVar()
showPath = ttk.Checkbutton(window, text='Show Path :', onvalue=1, offvalue=0, variable=int_var)
submit = Button(window, text='Submit', highlightbackground='#00FFFF', command=onsubmit)

showPath.grid(columnspan=2, row=2)
submit.grid(columnspan=2, row=3)
labelStart.grid(row=1, pady=3)
endBox.grid(row=1, column=1, pady=3)
startBox.grid(row=0, column=1, pady=3)
labelEnd.grid(row=0, pady=3)

window.update()
mainloop()

pygame.init()

pygame.display.set_caption("Path Finder")
screen = pygame.display.set_mode([510, 510])
clock = pygame.time.Clock()

for i in range(cols):
    for j in range(row):
        grid[i][j].display_tile(white, 1)

running = True


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    path = astar(grid)

    pygame.display.update()




pygame.quit()
Tk().wm_withdraw()
