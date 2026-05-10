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

# ── variables─────────────────────────────────────────
WIDTH = 960
HEIGHT = 650
TOPBAR_H = 64
BOTTOMBAR_H = 56
BOTTOMBAR_Y = HEIGHT - BOTTOMBAR_H  # y where the bottom bar starts
N = 50  # number of bars
ALGOS = ["Bubble", "Selection", "Insertation", "Merge"]
speed = [30, 20, 10, 5, 1]
speed_labels = ["0.25", "0.5", "1", "2", "4"]
speed_idx = 0
current_algo = ""
btn_h = 32
btn_w = 92
gap = 8
smallbtn_w = 32
smallbtn_h = 28

# ── constants — colors ────────────────────────────────────────
BG = (14, 14, 20)
BAR_BG = (20, 20, 30)
SEPARATOR = (40, 40, 55)
TEXT_PRIMARY = (225, 225, 225)
BTN_BG = (30, 30, 30)
BTN_HOVER = (40, 40, 55)
BTN_ACTIVE = (120, 65, 0)

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
resetbtn = pygame.Rect(
    WIDTH - 16 - smallbtn_w, (TOPBAR_H - smallbtn_h) // 2, smallbtn_w, smallbtn_h
)
playbtn = pygame.Rect(
    WIDTH - 16 - smallbtn_w * 2 - gap,
    (TOPBAR_H - smallbtn_h) // 2,
    smallbtn_w,
    smallbtn_h,
)
reset_text = btn_font.render("↺", True, TEXT_PRIMARY)
play_text = btn_font.render("▶", True, TEXT_PRIMARY)
speedbtn = pygame.Rect(
    WIDTH - 16 - smallbtn_w * 2 - gap,
    BOTTOMBAR_Y + smallbtn_h // 2,
    smallbtn_w * 2 + gap,
    smallbtn_h,
)
speed_text = btn_font.render(speed_labels[speed_idx], True, TEXT_PRIMARY)


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
sorting = False
running = True
current_algo = "Bubble"
frame_count = 0
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


# –––––—————————————reset function———————————————————————————
def reset():
    global \
        numbers, \
        i, \
        j, \
        key, \
        min_idx, \
        merge_step_index, \
        merge_steps, \
        active_indices, \
        cj, \
        ci, \
        sorting, \
        inserting
    numbers = [random.randint(10, BOTTOMBAR_Y - TOPBAR_H) for _ in range(N)]
    i = 0
    j = 0
    key = 0
    min_idx = 0
    merge_step_index = 0
    merge_steps = merge_sort_prepare(numbers)
    active_indices = []
    cj, ci = -1, -1
    sorting = False
    inserting = False


reset()
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
                    reset()
            if resetbtn.collidepoint(mx, my):
                reset()
            elif playbtn.collidepoint(mx, my):
                sorting = False if sorting == True else True
            elif speedbtn.collidepoint(mx, my):
                speed_idx = speed_idx + 1 if speed_idx < 4 else 0
                speed_text = btn_font.render(
                    speed_labels[speed_idx], True, TEXT_PRIMARY
                )
                screen.blit(speed_text, speed_text.get_rect(center=speedbtn.center))

    # ── sorting step ──────────────────────────────────────────
    bar_width = WIDTH // N

    if sorting and frame_count % speed[speed_idx] == 0:
        if current_algo == "Merge":
            numbers, active_indices, ci, cj, merge_step_index, sorting = (
                merge_sort_steps_unpacking(merge_steps, merge_step_index)
            )
        elif current_algo == "Bubble":
            numbers, i, j, sorting = bubble_sort_step(numbers, i, j)
        elif current_algo == "Selection":
            numbers, i, j, min_idx, sorting = selection_sort_step(
                numbers, i, j, min_idx
            )
        elif current_algo == "Insertation":
            numbers, i, j, key, inserting, sorting = insertion_sort_step(
                numbers, i, j, key, inserting
            )
    # ── draw bars ─────────────────────────────────────────────
    for idx, num in enumerate(numbers):
        color = (20, 20, 20)
        x, y = 0, 0

        if current_algo == "Merge":
            x, y, color = merge_sort_visual(
                numbers, active_indices, ci, cj, idx, BOTTOMBAR_Y, bar_width
            )
        elif current_algo == "Bubble":
            x, y, color = bubble_sort_visual(numbers, i, j, idx, BOTTOMBAR_Y, bar_width)
        elif current_algo == "Selection":
            x, y, color = selection_sort_visual(
                numbers, i, j, min_idx, idx, BOTTOMBAR_Y, bar_width
            )
        elif current_algo == "Insertation":
            x, y, color = insertation_sort_visual(
                numbers, i, j, idx, BOTTOMBAR_Y, bar_width
            )
        else:
            x = idx * bar_width
            y = BOTTOMBAR_Y - num

        pygame.draw.rect(screen, color, (x, y, bar_width, num), border_radius=2)

    # ── draw ui panels (drawn after bars so they sit on top) ──
    pygame.draw.rect(screen, BAR_BG, topbar)
    pygame.draw.line(screen, SEPARATOR, (0, TOPBAR_H), (WIDTH, TOPBAR_H), 1)

    pygame.draw.rect(screen, BAR_BG, bottombar)
    pygame.draw.line(screen, SEPARATOR, (0, BOTTOMBAR_Y), (WIDTH, BOTTOMBAR_Y), 1)

    # —————————————————draw algorithm buttons—————————————————————————————————————————
    for algo in ALGOS:
        color = (
            BTN_ACTIVE
            if algo == current_algo
            else (BTN_HOVER if btn_rects[algo].collidepoint(mx, my) else BTN_BG)
        )
        pygame.draw.rect(screen, color, btn_rects[algo])
        btn_text = btn_font.render(algo, True, TEXT_PRIMARY)
        screen.blit(btn_text, btn_text.get_rect(center=btn_rects[algo].center))

    # ————————————draw controll buttons————————————————————————————————————————————————————————
    color = BTN_HOVER if resetbtn.collidepoint(mx, my) else BTN_BG
    pygame.draw.rect(screen, color, resetbtn)
    color = BTN_HOVER if playbtn.collidepoint(mx, my) else BTN_BG
    pygame.draw.rect(screen, color, playbtn)
    screen.blit(reset_text, reset_text.get_rect(center=resetbtn.center))
    screen.blit(play_text, play_text.get_rect(center=playbtn.center))

    color = BTN_HOVER if speedbtn.collidepoint(mx, my) else BTN_BG
    pygame.draw.rect(screen, color, speedbtn)
    screen.blit(speed_text, speed_text.get_rect(center=speedbtn.center))

    # ── draw title ────────────────────────────────────────────
    screen.blit(title_surface, title_pos)

    pygame.display.update()
    clock.tick(60)
    frame_count += 1

pygame.quit()
