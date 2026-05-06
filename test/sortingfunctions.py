def bubble_sort_step(numbers, i, j):
    if i < len(numbers):
        if j < len(numbers) - i - 1:
            if numbers[j] > numbers[j + 1]:
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
            j += 1
            return numbers, i, j, True
        else:
            i += 1
            j = 0
            return numbers, i, j, True
    return numbers, i, j, False


def selection_sort_step(numbers, i, j, min_index):
    if i < len(numbers):
        if j < len(numbers):
            if numbers[j] < numbers[min_index]:
                min_index = j
            j += 1
            return numbers, i, j, min_index, True
        else:
            numbers[i], numbers[min_index] = numbers[min_index], numbers[i]
            i += 1
            j = i + 1
            min_index = i
            return numbers, i, j, min_index, True
    return numbers, i, j, min_index, False


def insertion_sort_step(numbers, i, j, key, inserting):
    if i < len(numbers):
        if not inserting:
            key = numbers[i]
            j = i - 1
            inserting = True
        if j >= 0 and numbers[j] > key:
            numbers[j + 1] = numbers[j]
            j -= 1
            return numbers, i, j, key, inserting, True
        else:
            numbers[j + 1] = key
            i += 1
            inserting = False
            return numbers, i, j, key, inserting, True
    return numbers, i, j, key, inserting, False


def merge_sort_prepare(numbers):
    steps = []

    def record(arr, active_indices, ci, cj):
        steps.append((arr[:], active_indices[:], ci, cj))

    def merge(arr, lo, mid, hi):
        left = arr[lo: mid + 1]
        right = arr[mid + 1: hi + 1]
        i = j = 0
        k = lo
        comparing_i = comparing_j = -1

        while i < len(left) and j < len(right):
            comparing_i = lo + i
            comparing_j = mid + 1 + j
            if left[i] <= right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            record(arr, list(range(lo, hi + 1)), comparing_i, comparing_j)
            k += 1

        while i < len(left):
            comparing_i = lo + i
            comparing_j = mid + 1 + j
            arr[k] = left[i]
            record(arr, list(range(lo, hi + 1)), comparing_i, comparing_j)
            i += 1
            k += 1

        while j < len(right):
            comparing_i = lo + i
            comparing_j = mid + 1 + j
            arr[k] = right[j]
            record(arr, list(range(lo, hi + 1)), comparing_i, comparing_j)
            j += 1
            k += 1

    def merge_sort(arr, lo, hi):
        if lo >= hi:
            return
        mid = (lo + hi) // 2
        record(arr, list(range(lo, hi + 1)), -1, -1)
        merge_sort(arr, lo, mid)
        merge_sort(arr, mid + 1, hi)
        merge(arr, lo, mid, hi)

    arr_copy = numbers[:]
    merge_sort(arr_copy, 0, len(arr_copy) - 1)
    return steps


def merge_sort_steps_unpacking(steps, step_index):
    if step_index < len(steps):
        numbers, active_indices, ci, cj = steps[step_index]
        return numbers, active_indices, ci, cj, step_index + 1, True
    numbers, active_indices, ci, cj = steps[-1]
    return numbers, [], ci, cj, step_index, False
