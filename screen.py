import pygame
import random
from sortingfunctions import bubble_sort_step, selection_sort_step
from visualizers import bubble_sort_visual, selection_sort_visual

# initializing paygane
pygame.init()


WIDTH, HEIGHT = 800, 600
# creating the surface aka screen with the width and height we previously set
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# self explainatory
pygame.display.set_caption("Algorithm Visualizer")

# i generate random numbers we will sort and visualize later
numbers = [random.randint(10, 500) for _ in range(50)]
i = 0
j = 0
min_idx = 0
sorting = True
running = True
clock = pygame.time.Clock()

# loop that updates the surface while running
while running:
    screen.fill((0, 0, 0))

    # listens for every event in the window like clicking a button
    for event in pygame.event.get():
        # quits if we close the window
        if event.type == pygame.QUIT:
            running = False

    # width of the visualized numbers so that there is equally enough room for all of them
    bar_width = WIDTH // len(numbers)

    if sorting:
        numbers, i, j, min_idx, sorting = selection_sort_step(numbers, i, j, min_idx)
        # numbers, i, j, sorting = bubble_sort_step(numbers, i, j)

    # creating the numbers visual propereties, adjusting them during the sorting for bubble sort
    for idx, num in enumerate(numbers):
        # x, y, color = bubble_sort_visual(numbers, i, j, idx, HEIGHT, bar_width)
        x, y, color = selection_sort_visual(
            numbers, i, j, min_idx, idx, HEIGHT, bar_width
        )

        # pygame.draw.rect(surface, color, (x, y, width, height)) drawing the numbers
        pygame.draw.rect(screen, color, (x, y, bar_width, num))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
