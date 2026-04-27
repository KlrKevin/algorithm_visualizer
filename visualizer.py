import pygame
import random

# initializing paygane
pygame.init()


WIDTH, HEIGHT = 800, 600
# creating the surface aka screen with the width and height we previously set
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# self explainatory
pygame.display.set_caption("Algorithm Visualizer")

# i generate random numbers we will sort and visualize later
numbers = [random.randint(10, 500) for _ in range(50)]

running = True

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

    # creating the numbers visual propereties
    for i, num in enumerate(numbers):
        x = i * bar_width
        y = HEIGHT - num

        # pygame.draw.rect(surface, color, (x, y, width, height)) drawing the numbers
        pygame.draw.rect(screen, (0, 255, 0), (x, y, bar_width, num))

    pygame.display.update()

pygame.quit()
