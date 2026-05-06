def bubble_sort_visual(numbers, i, j, idx, height, bar_width):
    num = numbers[idx]
    x = idx * bar_width
    y = height - num
    color = (60, 60, 80)
    if idx >= len(numbers) - i:
        color = (80, 220, 160)       # sorted — mint green
    elif idx == j or idx == j + 1:
        color = (255, 80, 100)       # comparing — coral red
    return x, y, color


def selection_sort_visual(numbers, i, j, min_idx, idx, height, bar_width):
    num = numbers[idx]
    x = idx * bar_width
    y = height - num
    color = (60, 60, 80)
    if idx < i:
        color = (80, 220, 160)       # sorted — mint green
    elif idx == min_idx:
        color = (255, 200, 50)       # current minimum — amber
    elif idx == j:
        color = (255, 80, 100)       # scanning — coral red
    return x, y, color


def insertation_sort_visual(numbers, i, j, idx, height, bar_width):
    num = numbers[idx]
    x = idx * bar_width
    y = height - num
    color = (60, 60, 80)
    if idx < i:
        color = (80, 220, 160)       # sorted — mint green
    elif idx == i:
        color = (255, 200, 50)       # key element — amber
    elif idx == j:
        color = (255, 80, 100)       # comparing — coral red
    return x, y, color


def merge_sort_visual(numbers, active_indices, ci, cj, idx, height, bar_width):
    num = numbers[idx]
    x = idx * bar_width
    y = height - num
    active_set = set(active_indices)
    color = (60, 60, 80)             # default — dark slate
    if idx in active_set:
        color = (100, 100, 180)      # active section — muted blue
    if idx == ci and ci != -1:
        color = (80, 220, 160)       # left candidate — mint green
    if idx == cj and cj != -1:
        color = (255, 80, 100)       # right candidate — coral red
    return x, y, color
