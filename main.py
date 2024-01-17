# tkinter for small dialog boxes
from tkinter import messagebox, Tk
import pygame
import sys

# Window dimensions
window_width= 500
window_height= 500

window = pygame.display.set_mode((window_width, window_height))

columns = 25
rows = 25

box_width= window_width // columns
box_height= window_width // rows

grid = []
queue = []

class Box:
    def __init__(self,xPos,yPos):
        self.x = xPos
        self.y = yPos

        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.neighbors = []

    def draw(self, win, color):
        # draws rectangle with x-cord, y-cord, width,and height
        pygame.draw.rect(win, color, (self.x * box_width, self.y * box_height, box_width - 2, box_height - 2))
        # the -2 is for padding between the boxes by 2 pixels

    def set_neighbors(self):
        # left right neighbours
        if self.x>0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.x<columns-1:
            self.neighbors.append(grid[self.x + 1][self.y])
        # up-down neighbours
        if self.y>0:
            self.neighbors.append(grid[self.x][self.y - 1])
        if self.y<rows-1:
            self.neighbors.append(grid[self.x][self.y + 1])


# Makes the grid
for i in range(columns):
    # clears arr for the next row of boxes
    arr = []
    for j in range(rows):
        # after loop, arr becomes a row of boxes
        arr.append(Box(i,j))
    # fills grid row by row with arr
    grid.append(arr)
    # grid becomes like [[row1], [row2], ..., [rowi]]

# Makes neighbours
for i in range(columns):
    for j in range(rows):
        grid[i][j].set_neighbors()


# ininitalize the starting poiint
start_box = grid[0][0]
start_box.start = True
start_box.visited = True
# adds starting point in the queue
queue.append(start_box)

def main():
    # Triggers the algorithm
    begin_search = False
    target_box_set = False
    searching = True
    target_box = None

    while True:
        for event in pygame.event.get():
            # Closes Window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                # Gets mouse location
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]

                # Makes wall [0] = left mouse button
                if event.buttons[0]:
                    i = x // box_width
                    j = y // box_height
                    print(i,"-",j)
                    grid[i][j].wall = True

                # Set Target with [2] = Right mouse button and makes sure theres no target alredy set so we cant change target anymore
                if event.buttons[2] and not target_box_set:
                    target_box_set = True
                    i = x // box_width
                    j = y // box_height
                    target_box = grid[i][j]
                    target_box.target = True
            # Start Algorithm
            if event.type == pygame.KEYDOWN and target_box_set:
                begin_search = True

        if begin_search:
            # if theres boxes to search in queue when its >0
            if len(queue) > 0 and searching:
                current_box = queue.pop(0)
                current_box.visited = True
                # checks for target box
                if current_box == target_box:
                    searching = False
                else:
                    # iterates through neighbouts, if its not in queue then we add it
                    for neighbor in current_box.neighbors:
                        if not neighbor.queued and not neighbor.wall:
                            queue.append(neighbor)
                            neighbor.queued = True
            # If no solution
            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution","There is no solution!")
                    searching = False



        window.fill((0,0,0))

        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window, (80,80,80))

                if box.queued:
                    box.draw(window, (200,0,0))
                if box.visited:
                    box.draw(window, (0,200,0))

                if box.start:
                    box.draw(window, (0,200,200))
                if box.wall:
                    box.draw(window, (50,50,50))
                if box.target:
                    box.draw(window, (200,200,0))
                






        pygame.display.flip()


main()
