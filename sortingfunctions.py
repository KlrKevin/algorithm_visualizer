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
