# bubble sort algorithm function
# takes the array and 2 integers as the input wich constantly change each time the function runs
def bubble_sort_step(numbers, i, j):

    # checks if there are unsorted items left to sort
    if i < len(numbers):
        # checks if there are any numbers next to the current one wich arent sorted yet
        if j < len(numbers) - i - 1:
            # if there are and they arent in the right order they get flipped
            if numbers[j] > numbers[j + 1]:
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
            # increments J to the the largest unsorted number we met at this point
            j += 1
            # returns the infos to create visuals with(these infos will get past back as sorting will still be true)
            return numbers, i, j, True
        # this happens if the next largest number has been sorted
        else:
            # increment i as one more element has been sorted
            i += 1
            # sets j to 0 because we start over
            j = 0
            return numbers, i, j, True
    # this happens if everything has been sorted
    else:
        return numbers, i, j, False


def selection_sort_step(numbers, i, j, min_index):
    if i < len(numbers):
        if j < len(numbers):
            if numbers[j] < numbers[min_index]:
                min_index = j

            j += 1
            return numbers, i, j, min_index, True

        else:
            # swap the smaller number with the current one
            numbers[i], numbers[min_index] = numbers[min_index], numbers[i]

            i += 1
            j = i + 1
            min_index = i

            return numbers, i, j, min_index, True

    return numbers, i, j, min_index, False


def insertion_sort_step(numbers, i, j, key, inserting):

    if i < len(numbers):
        # Step 1: pick the element
        if not inserting:
            key = numbers[i]
            j = i - 1
            inserting = True

        # Step 2: shift elements to the right
        if j >= 0 and numbers[j] > key:
            numbers[j + 1] = numbers[j]
            j -= 1
            return numbers, i, j, key, inserting, True

        # Step 3: insert key
        else:
            numbers[j + 1] = key
            i += 1
            inserting = False
            return numbers, i, j, key, inserting, True

    return numbers, i, j, key, inserting, False


def merge_sort_prepare(numbers):
    # mergesort is recursive so we can't pause it mid-way like the others
    # instead we run the whole thing upfront and record every step as a snapshot
    # screen.py then plays those snapshots back one by one, just like the other sorts
    steps = []

    def record(arr, active_indices, ci, cj):
        # save a copy of the array and which indices are currently being touched
        steps.append((arr[:], active_indices[:], ci, cj))

    def merge(arr, lo, mid, hi):
        left = arr[lo : mid + 1]
        right = arr[mid + 1 : hi + 1]

        i = 0
        j = 0
        k = lo
        comparing_i = -1
        comparing_j = -1

        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                arr[k] = left[i]
                comparing_i = lo + i
                comparing_j = mid + 1 + j
                i += 1
            else:
                comparing_i = lo + i
                comparing_j = mid + 1 + j
                arr[k] = right[j]
                j += 1
            # record after each placement so the visualizer shows the merge happening
            record(arr, list(range(lo, hi + 1)), comparing_i, comparing_j)
            k += 1

        while i < len(left):
            arr[k] = left[i]
            comparing_i = lo + i
            comparing_j = mid + 1 + j
            record(arr, list(range(lo, hi + 1)), comparing_i, comparing_j)
            i += 1
            k += 1

        while j < len(right):
            arr[k] = right[j]
            comparing_i = lo + i
            comparing_j = mid + 1 + j
            record(arr, list(range(lo, hi + 1)), comparing_i, comparing_j)
            j += 1
            k += 1

    def merge_sort(arr, lo, hi):
        if lo >= hi:
            return

        mid = (lo + hi) // 2

        # record the split so the visualizer shows which section we're working on
        record(arr, list(range(lo, hi + 1)), -1, -1)

        merge_sort(arr, lo, mid)
        merge_sort(arr, mid + 1, hi)
        merge(arr, lo, mid, hi)

    arr_copy = numbers[:]
    merge_sort(arr_copy, 0, len(arr_copy) - 1)

    return steps


def merge_sort_steps_unpacking(steps, step_index):
    # same pattern as the other sort functions — call this each frame
    if step_index < len(steps):
        numbers, active_indices, ci, cj = steps[step_index]
        return numbers, active_indices, ci, cj, step_index + 1, True

    # past the end — sorting is done
    numbers, active_indices, ci, cj = steps[-1]
    return numbers, [], ci, cj, step_index, False
