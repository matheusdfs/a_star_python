import PIL
import os
import pygame as pyg
import numpy as np
import math
import matplotlib.pyplot as plt

tam_pixel = 10

class Node:
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def a_star(maze, start, end, screen):
    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                running = False

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)
        pyg.draw.rect(screen, (0, 0, 255), [current_node.position[0] * tam_pixel, current_node.position[1] * tam_pixel, tam_pixel, tam_pixel])
        pyg.display.flip()

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:  # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            jump: bool = 0

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                jump = 1

            for actual in open_list:
                if actual.position[0] == node_position[0] and actual.position[1] == node_position[1]:
                    jump = 1

            for actual in closed_list:
                if actual.position[0] == node_position[0] and actual.position[1] == node_position[1]:
                    jump = 1

            if jump:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

            if new_position[0] != 0 and new_position[1] != 0:
                new_node.g = current_node.g + 1.8
            else:
                new_node.g = current_node.g + 1

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            #child.g = current_node.g + math.sqrt(((current_node.position[0] - child.position[0]) ** 2) + ((current_node.position[1] - child.position[1]) ** 2))
            child.h = 1.2*(math.sqrt(((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)))
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


def main():

    print("Open the image and transforming in a grey scale...")

    img = PIL.Image.open("map_input.png")
    gray_img = img.convert("L")
    plt.imshow(gray_img, cmap='gray')
    plt.savefig("./map_output.png")
    maze = np.array(gray_img)

    n_row = len(maze)
    n_columns = len(maze[0])

    i = 0
    j = 0

    start = (-1, -1)
    end = (-1, -1)

    print("Classifying each pixel in the image...")

    screen = pyg.display.set_mode((n_row*tam_pixel, n_columns*tam_pixel))
    pyg.display.set_caption('A_STAR PROGRESS')
    background_colour = (255, 255, 255)
    screen.fill(background_colour)

    # Search and set start and end
    for i in range(n_row):
        for j in range(n_columns):
            if 100 <= maze[i][j] <= 140:
                start = (i, j)
                maze[i][j] = 0
                pyg.draw.rect(screen, (0, 255, 0), [i * tam_pixel, j * tam_pixel, tam_pixel, tam_pixel])
            elif 80 <= maze[i][j] <= 99:
                end = (i, j)
                maze[i][j] = 0
                pyg.draw.rect(screen, (255, 0, 0), [i * tam_pixel, j * tam_pixel, tam_pixel, tam_pixel])
            elif maze[i][j] <= 79:
                maze[i][j] = 1
                pyg.Rect((i,j), (10, 10))
                pyg.draw.rect(screen, (0, 0, 0), [i * tam_pixel, j * tam_pixel, tam_pixel, tam_pixel])
            else:
                maze[i][j] = 0
                pyg.draw.rect(screen, (255, 255, 255), [i*tam_pixel, j*tam_pixel, tam_pixel, tam_pixel] )

    pyg.display.flip()

    # Change the value of the start and end to 0, that means a walkable place
    maze[start[0]][start[1]] = 0
    maze[end[0]][end[1]] = 0
    path = 0

    print("Searching for the best way through...")

    if start != (-1, -1) and end != (-1, -1):
        path = a_star(maze, start, end, screen)
    else:
        print("Start or end of the map is not found!")



    for best_path in path:
        pyg.draw.rect(screen, (255, 223, 0), [best_path[0] * tam_pixel, best_path[1] * tam_pixel, tam_pixel, tam_pixel])
        pyg.display.flip()

    print(path)

    os.system("pause")


if __name__ == '__main__':
    main()
