import time
import queue
import random
import threading

def bubble_sort_visu(arr):
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                yield arr, j, j + 1
    yield arr, None, None

def bogo_sort_visu(arr):
    sorted = False
    while not sorted:
        sorted = True
        for i in range(1, len(arr)):
            if (arr[i] < arr[i - 1]):
                sorted = False
                random.shuffle(arr)
                yield arr, i, None
    yield arr, None, None


def sleep_sort_visu(arr):
    arr = arr.copy()
    result = []
    q = queue.Queue()

    def sleeper(x, index):
        time.sleep(x * 0.05)  # Scale down sleep for practical visualization
        q.put((x, index))     # Send value and original index to queue

    threads = []
    for i, num in enumerate(arr):
        t = threading.Thread(target=sleeper, args=(num, i))
        t.start()
        threads.append(t)

    # Wait for all items to be "sorted" via sleeping
    sorted_count = 0
    sorted_arr = []
    highlight_idx = None

    while sorted_count < len(arr):
        x, original_index = q.get()
        sorted_arr.append(x)
        sorted_count += 1
        highlight_idx = len(sorted_arr) - 1
        yield sorted_arr, highlight_idx, None

    for t in threads:
        t.join()

    yield sorted_arr, None, None

def counting_sort_visu(arr):

    arr = arr.copy()
    minimum = min(arr)
    aux = [0] * (max(arr) - minimum + 1)
    for i, n in enumerate(arr):
        aux[n - minimum] += 1
        yield arr, i, None
    
    sorted_array = []

    for i in range(len(aux)):
        for _ in range(aux[i]):
            sorted_array.append(i + minimum)
            yield sorted_array + arr[len(sorted_array):], len(sorted_array) - 1, None

    yield sorted_array, None, None

def merge_sort_visu(arr):
    arr = arr.copy()
    aux = [0] * len(arr)
    yield from _merge_sort(arr, aux, 0, len(arr) - 1)
    yield arr, None, None  # Final state

def _merge_sort(arr, aux, left, right):
    if left >= right:
        return

    mid = (left + right) // 2
    yield from _merge_sort(arr, aux, left, mid)
    yield from _merge_sort(arr, aux, mid + 1, right)
    yield from _merge(arr, aux, left, mid, right)

def _merge(arr, aux, left, mid, right):
    i, j, k = left, mid + 1, left

    while i <= mid and j <= right:
        # Highlight the elements being compared
        yield arr, i, j
        if arr[i] <= arr[j]:
            aux[k] = arr[i]
            i += 1
        else:
            aux[k] = arr[j]
            j += 1
        k += 1

    while i <= mid:
        yield arr, i, i
        aux[k] = arr[i]
        i += 1
        k += 1

    while j <= right:
        yield arr, j, j
        aux[k] = arr[j]
        j += 1
        k += 1

    for l in range(left, right + 1):
        arr[l] = aux[l]
        yield arr, l, l  # Yield after placing back to arr

def insertion_sort_visu(arr):
    arr = arr.copy()
    for i in range(1, len(arr)):
        element = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > element:
            arr[j + 1] = arr[j]
            yield arr, i, j
            j -= 1
            
        arr[j + 1] = element
        yield arr, i, j
    yield arr, None, None

def gravity_sort_visu(arr): # algoritmo em reverso porque o gravity sort é naturalmente decrescente.
    arr = arr.copy()
    length = len(arr)

    for i in range(len(arr)):
        yield arr, i, None

    max_val = max(arr)
    beads = [[0] * length for _ in range(max_val)]

    # Drop beads (simulate "floating" upward from bottom)
    for col, val in enumerate(arr):
        for row in range(max_val - 1, max_val - val - 1, -1):
            beads[row][col] = 1

    # Let the beads float (settle to top)
    for row in range(max_val - 1, -1, -1):
        count = sum(beads[row])
        for col in range(length):
            beads[row][col] = 1 if col >= length - count else 0
        # Visualize after row "settles"
        current_heights = [sum(beads[row][col] for row in range(max_val)) for col in range(length)]
        yield current_heights, None, None

    # Final sorted array (ascending)
    sorted_arr = [sum(beads[row][i] for row in range(max_val)) for i in range(length)]
    yield sorted_arr, None, None

def radix_LSD_sort_visu(arr):
    arr = arr.copy()
    n = len(arr)

    def rad_counting_sort(arr, exp):
        output = [0] * n
        count = [0] * 10

        # Count digit frequencies
        for i, num in enumerate(arr):
            digit = (num // exp) % 10
            count[digit] += 1
            yield arr, i, None  # Highlight current digit being counted

        # Cumulative count
        for i in range(1, 10):
            count[i] += count[i - 1]

        # Build output (stable)
        for i in reversed(range(n)):
            digit = (arr[i] // exp) % 10
            pos = count[digit] - 1
            output[pos] = arr[i]
            count[digit] -= 1
            # Yield with highlight on the source and target positions
            # yield output.copy(), i, pos # This causes it to look chaotic if uncommented

        # Copy output back to arr
        for i in range(n):
            arr[i] = output[i]
            yield arr.copy(), i, None  # Highlight as it’s written back

        return arr

    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        # Step through counting sort with yields
        sorter = rad_counting_sort(arr, exp)
        for state in sorter:
            yield state
        exp *= 10

    yield arr, None, None  # Final yield for completion

def pigeonhole_sort_visu(arr):
    arr = arr.copy()
    minimum = min(arr)
    maximum = max(arr)
    size = maximum - minimum + 1
    holes = [[] for _ in range(size)]

    # Place elements into their pigeonholes
    for i, x in enumerate(arr):
        holes[x - minimum].append(x)
        yield arr, i, None

    # Reconstruct sorted array
    i = 0
    for hole_index, hole in enumerate(holes):
        for num in hole:
            arr[i] = num
            yield arr, i, hole_index
            i += 1

    yield arr, None, None
