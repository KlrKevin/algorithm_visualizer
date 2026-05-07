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

# ── init ──────────────────────────────────────────────────────
pygame.init()

# ── constants─────────────────────────────────────────
WIDTH = 960
HEIGHT = 650
TOPBAR_H = 64
BOTTOMBAR_H = 56
BOTTOMBAR_Y = HEIGHT - BOTTOMBAR_H  # y where the bottom bar starts
N = 50  # number of bars
ALGOS = ["Bubble", "Selection", "Insertation", "Merge"]
btn_h = 32
btn_w = 92
gap = 8

# ── constants — colors ────────────────────────────────────────
BG = (14, 14, 20)
BAR_BG = (20, 20, 30)
SEPARATOR = (40, 40, 55)
TEXT_PRIMARY = (225, 225, 225)
BTN_BG = (30, 30, 30)
BTN_HOVER = (40, 40, 55)

# ── screen ────────────────────────────────────────────────────
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sort Lab")
clock = pygame.time.Clock()

# ── fonts ─────────────────────────────────────────────────────
font_title = pygame.font.SysFont("menlo", 14, bold=True)
btn_font = pygame.font.SysFont("menlo", 12, bold=False)

# ── ui elements — computed once, not every frame ───────────────
topbar = pygame.Rect(0, 0, WIDTH, TOPBAR_H)
bottombar = pygame.Rect(0, BOTTOMBAR_Y, WIDTH, BOTTOMBAR_H)

title_surface = font_title.render("Sort Lab", True, TEXT_PRIMARY)
title_pos = title_surface.get_rect(center=(WIDTH // 2, TOPBAR_H // 2))
btn_rects = {}

# ── sorting state ─────────────────────────────────────────────
numbers = [random.randint(10, BOTTOMBAR_Y - TOPBAR_H - 10) for _ in range(N)]
i = 1
j = 0
min_idx = 0
key = 0
inserting = False
sorting = True
running = True

# ── merge sort state ──────────────────────────────────────────
merge_steps = merge_sort_prepare(numbers)
merge_step_index = 0
active_indices = []
ci = -1
cj = -1

# -----------creating button rects---------------------------
for idx, algo in enumerate(ALGOS):
    left = 16 + idx * (gap + btn_w)
    btn_rects[algo] = pygame.Rect(left, (TOPBAR_H - btn_h) // 2, btn_w, btn_h)

# ── main loop ─────────────────────────────────────────────────
while running:
    screen.fill(BG)
    mx, my = pygame.mouse.get_pos()

    # ── events ────────────────────────────────────────────────
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for algo in ALGOS:
                if btn_rects[algo].collidepoint(mx, my):
                    current_algo = algo

    # ── sorting step ──────────────────────────────────────────
    bar_width = WIDTH // N

    if sorting:
        numbers, active_indices, ci, cj, merge_step_index, sorting = (
            merge_sort_steps_unpacking(merge_steps, merge_step_index)
        )

    # ── draw bars ─────────────────────────────────────────────
    for idx, num in enumerate(numbers):
        x, y, color = merge_sort_visual(
            numbers, active_indices, ci, cj, idx, BOTTOMBAR_Y, bar_width
        )
        pygame.draw.rect(screen, color, (x, y, bar_width, num), border_radius=2)

    # ── draw ui panels (drawn after bars so they sit on top) ──
    pygame.draw.rect(screen, BAR_BG, topbar)
    pygame.draw.line(screen, SEPARATOR, (0, TOPBAR_H), (WIDTH, TOPBAR_H), 1)

    pygame.draw.rect(screen, BAR_BG, bottombar)
    pygame.draw.line(screen, SEPARATOR, (0, BOTTOMBAR_Y), (WIDTH, BOTTOMBAR_Y), 1)
    for algo in ALGOS:
        color = BTN_HOVER if btn_rects[algo].collidepoint(mx, my) else BTN_BG
        pygame.draw.rect(screen, color, btn_rects[algo])
        btn_text = btn_font.render(algo, True, TEXT_PRIMARY)
        screen.blit(btn_text, btn_text.get_rect(center=btn_rects[algo].center))

    # ── draw title ────────────────────────────────────────────
    screen.blit(title_surface, title_pos)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
