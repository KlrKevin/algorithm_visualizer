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
i = 0
j = 0
sorting = True
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

    if sorting:
        if i < len(numbers):
            if j < len(numbers) - i - 1:
                if numbers[j] > numbers[j + 1]:
                    numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]

                j += 1

            else:
                j = 0
                i += 1
    else:
        sorting = False

    # creating the numbers visual propereties
    for idx, num in enumerate(numbers):
        x = idx * bar_width
        y = HEIGHT - num

        color = (0, 255, 0)

        if idx == j or idx == j + 1:
            color = (255, 0, 0)  # red for comparison

        # pygame.draw.rect(surface, color, (x, y, width, height)) drawing the numbers
        pygame.draw.rect(screen, color, (x, y, bar_width, num))

    pygame.display.update()
    pygame.time.delay(20)

pygame.quit()
