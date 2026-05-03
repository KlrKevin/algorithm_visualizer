def bubble_sort_visual(numbers, i, j, idx, height, bar_width):
    num = numbers[idx]
    x = idx * bar_width
    y = height - num

    color = (0, 200, 0)

    if idx >= len(numbers) - i:
        color = (0, 0, 200)

    elif idx == j or idx == j + 1:
        color = (200, 0, 0)  # red for comparison

    return x, y, color


def selection_sort_visual(numbers, i, j, min_idx, idx, height, bar_width):
    num = numbers[idx]
    x = idx * bar_width
    y = height - num

    color = (0, 255, 0)

    if idx < i:
        color = (0, 0, 255)  # sorted

    elif idx == j:
        color = (255, 0, 0)  # scanning

    elif idx == min_idx:
        color = (255, 255, 0)  # current minimum

    return x, y, color


def insertation_sort_visual(numbers, i, j, idx, height, bar_width):
    num = numbers[idx]
    x = idx * bar_width
    y = height - num

    color = (0, 255, 0)

    if idx < i:
        color = (0, 0, 255)  # sorted

    elif idx == j:
        color = (255, 0, 0)  # scanning

    elif idx == i:
        color = (255, 255, 0)  # current minimum

    return x, y, color


def merge_sort_visual(numbers, active_indices, ci, cj, idx, height, bar_width):
    num = numbers[idx]
    x = idx * bar_width
    y = height - num
    active_set = set(active_indices)

    # default: white — not currently being touched
    color = (255, 255, 255)

    if idx in active_set:
        # red — this bar is in the section currently being merged or split
        color = (200, 0, 0)

    if idx == ci and ci != -1:
        color = (0, 255, 0)

    if idx == cj and cj != -1:
        color = (0, 255, 255)

    return x, y, color
