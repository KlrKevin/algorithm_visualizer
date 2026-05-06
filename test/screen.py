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

pygame.init()

# ── dimensions ────────────────────────────────────────────────
WIDTH, HEIGHT = 960, 620
TOPBAR_H = 64
BOTTOMBAR_H = 56
VIZ_TOP = TOPBAR_H
VIZ_BOTTOM = HEIGHT - BOTTOMBAR_H
VIZ_H = VIZ_BOTTOM - VIZ_TOP

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sort Lab")
clock = pygame.time.Clock()

# ── fonts ──────────────────────────────────────────────────────
font_large = pygame.font.SysFont("menlo", 15, bold=True)
font_small = pygame.font.SysFont("menlo", 12)

# ── palette ────────────────────────────────────────────────────
BG = (14, 14, 20)
TOPBAR_BG = (20, 20, 30)
BTN_IDLE = (30, 30, 45)
BTN_HOVER = (45, 45, 65)
BTN_ACTIVE = (80, 220, 160)
BTN_TEXT = (180, 180, 200)
BTN_ACTIVE_TEXT = (14, 14, 20)
ACCENT = (80, 220, 160)
DIM = (60, 60, 80)
WHITE = (220, 220, 235)
CORAL = (255, 80, 100)

# ── state ──────────────────────────────────────────────────────
N = 60
ALGOS = ["Bubble", "Selection", "Insertion", "Merge"]
current_algo = "Merge"
speeds = [2, 6, 15, 30, 60]
speed_labels = ["0.25x", "0.5x", "1x", "2x", "4x"]
speed_idx = 2
sorting = False
paused = False

# ── animation state ────────────────────────────────────────────
# tracks a swap animation between two bar indices
ANIM_FRAMES = 8  # how many frames the slide takes
anim_active = False  # is an animation currently playing?
anim_frame = 0  # current frame (0 → ANIM_FRAMES)
anim_idx_a = -1  # index of bar sliding right
anim_idx_b = -1  # index of bar sliding left
prev_numbers = []  # snapshot before the swap (so we can interpolate)


def fresh_numbers():
    return [random.randint(10, VIZ_H - 10) for _ in range(N)]


def reset_state(numbers):
    global i, j, min_idx, key, inserting
    global merge_steps, merge_step_index, active_indices, ci, cj
    global anim_active, anim_frame, anim_idx_a, anim_idx_b, prev_numbers
    i, j, min_idx, key, inserting = 1, 0, 0, 0, False
    active_indices, ci, cj = [], -1, -1
    anim_active = False
    anim_frame = 0
    anim_idx_a = -1
    anim_idx_b = -1
    prev_numbers = numbers[:]
    if current_algo == "Merge":
        merge_steps = merge_sort_prepare(numbers)
        merge_step_index = 0


numbers = fresh_numbers()
reset_state(numbers)


# ── easing ─────────────────────────────────────────────────────
def ease_in_out(t):
    # smooth cubic ease — t in [0,1]
    return t * t * (3 - 2 * t)


# ── button helpers ─────────────────────────────────────────────
def draw_pill(label, rect, active=False, hovered=False):
    bg = BTN_ACTIVE if active else (BTN_HOVER if hovered else BTN_IDLE)
    fg = BTN_ACTIVE_TEXT if active else BTN_TEXT
    radius = rect.height // 2
    pygame.draw.rect(screen, bg, rect, border_radius=radius)
    if not active:
        pygame.draw.rect(screen, (50, 50, 70), rect, width=1, border_radius=radius)
    text = font_large.render(label, True, fg)
    screen.blit(text, text.get_rect(center=rect.center))


def draw_icon_btn(symbol, rect, hovered=False, color=None):
    bg = BTN_HOVER if hovered else BTN_IDLE
    fg = color if color else BTN_TEXT
    pygame.draw.rect(screen, bg, rect, border_radius=8)
    pygame.draw.rect(screen, (50, 50, 70), rect, width=1, border_radius=8)
    text = font_large.render(symbol, True, fg)
    screen.blit(text, text.get_rect(center=rect.center))


# ── layout rects ───────────────────────────────────────────────
def build_rects():
    rects = {}
    btn_w, btn_h = 96, 32
    gap = 8
    start_x = 16
    cy = TOPBAR_H // 2
    for idx, name in enumerate(ALGOS):
        x = start_x + idx * (btn_w + gap)
        rects[f"algo_{name}"] = pygame.Rect(x, cy - btn_h // 2, btn_w, btn_h)
    right_x = WIDTH - 16
    icon_w, icon_h = 40, 32
    rects["speed"] = pygame.Rect(right_x - icon_w, cy - icon_h // 2, icon_w, icon_h)
    right_x -= icon_w + gap
    rects["playpause"] = pygame.Rect(right_x - icon_w, cy - icon_h // 2, icon_w, icon_h)
    right_x -= icon_w + gap
    rects["reset"] = pygame.Rect(right_x - icon_w, cy - icon_h // 2, icon_w, icon_h)
    return rects


rects = build_rects()


# ── detect swap between two array states ───────────────────────
def find_swap(old, new):
    # returns (a, b) if exactly two indices differ and their values crossed, else (-1, -1)
    diffs = [i for i in range(len(old)) if old[i] != new[i]]
    if len(diffs) == 2:
        a, b = diffs
        if old[a] == new[b] and old[b] == new[a]:
            return a, b
    return -1, -1


# ── main loop ──────────────────────────────────────────────────
running = True
while running:
    mx, my = pygame.mouse.get_pos()
    bar_width = WIDTH // N

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for name in ALGOS:
                if rects[f"algo_{name}"].collidepoint(mx, my):
                    current_algo = name
                    sorting = False
                    paused = False
                    numbers = fresh_numbers()
                    reset_state(numbers)

            if rects["reset"].collidepoint(mx, my):
                sorting = False
                paused = False
                numbers = fresh_numbers()
                reset_state(numbers)

            if rects["playpause"].collidepoint(mx, my):
                if not sorting:
                    sorting = True
                    paused = False
                else:
                    paused = not paused

            if rects["speed"].collidepoint(mx, my):
                speed_idx = (speed_idx + 1) % len(speeds)

    # ── animation tick ─────────────────────────────────────────
    if anim_active:
        anim_frame += 1
        if anim_frame >= ANIM_FRAMES:
            # animation done — commit the swap into numbers
            anim_active = False
            anim_frame = 0

    # ── sorting step (only when no animation playing) ──────────
    elif sorting and not paused:
        old = numbers[:]

        if current_algo == "Bubble":
            numbers, i, j, sorting = bubble_sort_step(numbers, i, j)
        elif current_algo == "Selection":
            numbers, i, j, min_idx, sorting = selection_sort_step(
                numbers, i, j, min_idx
            )
        elif current_algo == "Insertion":
            numbers, i, j, key, inserting, sorting = insertion_sort_step(
                numbers, i, j, key, inserting
            )
        elif current_algo == "Merge":
            numbers, active_indices, ci, cj, merge_step_index, sorting = (
                merge_sort_steps_unpacking(merge_steps, merge_step_index)
            )

        # check if a swap just happened and kick off animation
        a, b = find_swap(old, numbers)
        if a != -1:
            anim_active = True
            anim_frame = 0
            anim_idx_a = a
            anim_idx_b = b
            prev_numbers = old  # draw from old positions during animation

    # ── draw background ────────────────────────────────────────
    screen.fill(BG)
    pygame.draw.rect(screen, TOPBAR_BG, (0, 0, WIDTH, TOPBAR_H))
    pygame.draw.line(screen, (35, 35, 50), (0, TOPBAR_H), (WIDTH, TOPBAR_H), 1)
    pygame.draw.rect(screen, TOPBAR_BG, (0, VIZ_BOTTOM, WIDTH, BOTTOMBAR_H))
    pygame.draw.line(screen, (35, 35, 50), (0, VIZ_BOTTOM), (WIDTH, VIZ_BOTTOM), 1)

    # ── draw buttons ───────────────────────────────────────────
    for name in ALGOS:
        r = rects[f"algo_{name}"]
        draw_pill(
            name, r, active=(name == current_algo), hovered=r.collidepoint(mx, my)
        )

    draw_icon_btn("↺", rects["reset"], hovered=rects["reset"].collidepoint(mx, my))
    if not sorting or paused:
        draw_icon_btn(
            "▶",
            rects["playpause"],
            hovered=rects["playpause"].collidepoint(mx, my),
            color=ACCENT,
        )
    else:
        draw_icon_btn(
            "⏸",
            rects["playpause"],
            hovered=rects["playpause"].collidepoint(mx, my),
            color=CORAL,
        )
    draw_pill(
        speed_labels[speed_idx],
        rects["speed"],
        hovered=rects["speed"].collidepoint(mx, my),
    )

    # ── status label ───────────────────────────────────────────
    if not sorting and not paused:
        status = "press ▶ to start"
    elif paused:
        status = "paused"
    else:
        status = f"sorting — {current_algo.lower()}sort"
    label = font_small.render(status, True, (100, 100, 130))
    screen.blit(label, (16, VIZ_BOTTOM + (BOTTOMBAR_H - label.get_height()) // 2))
    step_label = font_small.render(
        f"n = {N}  ·  speed {speed_labels[speed_idx]}", True, (70, 70, 90)
    )
    screen.blit(
        step_label,
        (
            WIDTH - step_label.get_width() - 16,
            VIZ_BOTTOM + (BOTTOMBAR_H - step_label.get_height()) // 2,
        ),
    )

    # ── draw bars ──────────────────────────────────────────────
    t = ease_in_out(anim_frame / ANIM_FRAMES) if anim_active else 0.0

    for idx in range(N):
        # choose which array to read height/color from
        display_numbers = prev_numbers if anim_active else numbers

        if current_algo == "Bubble":
            x, y, color = bubble_sort_visual(
                display_numbers, i, j, idx, VIZ_BOTTOM, bar_width
            )
        elif current_algo == "Selection":
            x, y, color = selection_sort_visual(
                display_numbers, i, j, min_idx, idx, VIZ_BOTTOM, bar_width
            )
        elif current_algo == "Insertion":
            x, y, color = insertation_sort_visual(
                display_numbers, i, j, idx, VIZ_BOTTOM, bar_width
            )
        elif current_algo == "Merge":
            x, y, color = merge_sort_visual(
                display_numbers, active_indices, ci, cj, idx, VIZ_BOTTOM, bar_width
            )

        # interpolate x position for the two swapping bars
        if anim_active:
            if idx == anim_idx_a:
                # sliding rightward toward b's slot
                target_x = anim_idx_b * bar_width
                x = int(x + (target_x - x) * t)
                color = CORAL
            elif idx == anim_idx_b:
                # sliding leftward toward a's slot
                target_x = anim_idx_a * bar_width
                x = int(x + (target_x - x) * t)
                color = ACCENT

        pygame.draw.rect(
            screen,
            color,
            pygame.Rect(x + 1, y, bar_width - 1, display_numbers[idx]),
            border_radius=2,
        )

    pygame.display.update()
    clock.tick(60)  # always 60fps — speed only controls how often we take a sort step

pygame.quit()
