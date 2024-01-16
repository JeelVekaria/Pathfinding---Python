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

class Box:
    def __init__(self,xPos,yPos):
        self.x = xPos
        self.y = yPos
    def draw(self, win, color):
        # draws rectangle with x-cord, y-cord, width,and height
        pygame.draw.rect(win, color, (self.x * box_width, self.y * box_height, box_height - 2, box_height - 2))

for i in range(columns):
    # clears arr for the next row of boxes
    arr = []
    for j in range(rows):
        # after loop, arr becomes a row of boxes
        arr.append(Box(i,j))
    # fills grid row by row with arr
    grid.append(arr)
    # grid becomes like [[row1], [row2], ..., [rowi]]

def main():
    while True:
        for event in pygame.event.get():
            # Closes Window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        window.fill((0,0,0))

        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window, (20,20,20))






        pygame.display.flip()


main()
