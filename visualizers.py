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
