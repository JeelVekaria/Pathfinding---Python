# tkinter for small dialog boxes
from tkinter import messagebox, Tk
import pygame
import sys
pygame.init()

# Window dimensions
window_width= 500
window_height= 500

window = pygame.display.set_mode((window_width, window_height+60))

columns = 25
rows = 25

box_width= window_width // columns
box_height= window_width // rows

font = pygame.font.Font(None, 25)

grid = []
queue = []
path = []

def draw_bottom_text(line1, line2, line3):
    # Create text surfaces for each line, S, E, Space
    text_surface_line1 = font.render(line1, True, (0, 200, 200)) 
    text_surface_line2 = font.render(line2, True, (200, 200, 0)) 
    text_surface_line3 = font.render(line3, True, (200,200,200)) 

    # Get the text rectangles for each line
    text_rect_line1 = text_surface_line1.get_rect()
    text_rect_line2 = text_surface_line2.get_rect()
    text_rect_line3 = text_surface_line3.get_rect()

    # Center the text lines at the bottom of the window
    text_rect_line1.center = (window_width // 2, window_height + 30 - 18)  
    text_rect_line2.center = (window_width // 2, window_height + 30 + 0)  
    text_rect_line3.center = (window_width // 2, window_height + 30 + 18)  

    # Draw the text on the window
    window.blit(text_surface_line1, text_rect_line1)
    window.blit(text_surface_line2, text_rect_line2)
    window.blit(text_surface_line3, text_rect_line3)

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
        self.prior = None

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



# adds starting point in the queue

def main():
    # Triggers the algorithm
    begin_search = False
    searching = True
    # target_box = None
    
    # target_box_set = True
    target_box =grid[(len(grid[0])//4)*3][len(grid)//2]
    target_box.target = True

    start_box = grid[len(grid[0])//4][len(grid)//2]
    start_box.start = True
    queue.append(start_box)

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
                if event.buttons[0] and y<window_height:
                    i = x // box_width
                    j = y // box_height
                    print(i,"-",j)
                    grid[i][j].wall = True

            # Smakes sure theres no target alredy set so we cant change target anymore
            # Start Algorithm
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

                if event.key == pygame.K_SPACE:
                    begin_search = True

                if event.key == pygame.K_e and y<window_height:
                    # Set to false to clear previous target node color
                    target_box.target = False
                    i = x // box_width
                    j = y // box_height
                    # if target_box.x != start_box.x and target_box.y != start_box.y:
                    target_box = grid[i][j]
                    # Set to trie to set color at new node
                    target_box.target = True

                if event.key == pygame.K_s and y<window_height:
                    start_box.start = False
                    i = x // box_width
                    j = y // box_height
                    start_box = grid[i][j]
                    start_box.start = True
                    queue.pop()
                    queue.append(start_box)


        if begin_search:
            # if theres boxes to search in queue when its >0
            if len(queue) > 0 and searching:
                current_box = queue.pop(0)
                current_box.visited = True
                # checks for target box
                if current_box == target_box:
                    searching = False
                    # saves shortest path in path varaible from start to target
                    while current_box.prior != start_box:
                        path.append(current_box.prior)
                        current_box = current_box.prior
                else:
                    # iterates through neighbouts, if its not in queue then we add it
                    for neighbor in current_box.neighbors:
                        if not neighbor.queued and not neighbor.wall:
                            queue.append(neighbor)
                            neighbor.prior = current_box
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
                if box in path:
                    box.draw(window, (0,0,200))

                if box.start:
                    box.draw(window, (0,200,200))
                if box.wall:
                    box.draw(window, (50,50,50))
                if box.target:
                    box.draw(window, (200,200,0))
                





        draw_bottom_text("Press S/E to place starting/ending node", "Drag left click to place walls", "Press Space to start Dijkstra's Algorithm")
        pygame.display.flip()


main()
