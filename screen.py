import pygame
import random
from sortingfunctions import (
    bubble_sort_step,
    selection_sort_step,
    insertion_sort_step,
    merge_sort_prepare,
    merge_sort_steps_unpacking,
)
from visualizers import (
    bubble_sort_visual,
    selection_sort_visual,
    insertation_sort_visual,
    merge_sort_visual,
)

# initializing paygane
pygame.init()


WIDTH, HEIGHT = 800, 600
# creating the surface aka screen with the width and height we previously set
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# self explainatory
pygame.display.set_caption("Algorithm Visualizer")

# i generate random numbers we will sort and visualize later
numbers = [random.randint(10, 500) for _ in range(50)]
i = 1
j = 0
min_idx = 0
key = 0
inserting = False
sorting = True
running = True
clock = pygame.time.Clock()

# mergesort: precompute all steps upfront, then play them back frame by frame
merge_steps = merge_sort_prepare(numbers)
merge_step_index = 0
active_indices = []
ci = -1
cj = -1

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
        numbers, active_indices, ci, cj, merge_step_index, sorting = (
            merge_sort_steps_unpacking(merge_steps, merge_step_index)
        )

    # creating the numbers visual propereties, adjusting them during the sorting
    for idx, num in enumerate(numbers):
        x, y, color = merge_sort_visual(
            numbers, active_indices, ci, cj, idx, HEIGHT, bar_width
        )

        # pygame.draw.rect(surface, color, (x, y, width, height)) drawing the numbers
        pygame.draw.rect(screen, color, (x, y, bar_width, num))

    pygame.display.update()
    clock.tick(6)

pygame.quit()
