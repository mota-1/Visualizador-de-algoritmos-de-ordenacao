import random
import threading
import time

def radix_LSD_sort(arr):
    def rad_counting_sort(arr, exp):
        n = len(arr)
        output = [0] * n
        count = [0] * 10

        for i in arr:
            index = (i // exp) % 10
            count[index] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        for i in reversed(arr):
            index = (i // exp) % 10
            output[count[index] - 1] = i
            count[index] -= 1

        return output
    
    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        arr = rad_counting_sort(arr, exp)
        exp *= 10
    return arr

def counting_sort(arr):
    minimum = min(arr)
    aux = [0] * (max(arr) - minimum + 1)
    for n in arr:
        aux[n - minimum] += 1 
    
    sorted_array = []

    for i in range(0, len(aux)):
        sorted_array.extend([i + minimum] * aux[i])
    return sorted_array

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    aux = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            aux.append(left[i])
            i += 1
        else:
            aux.append(right[j])
            j += 1

    
    aux.extend(left[i:])
    aux.extend(right[j:])

    return aux

def insertion_sort(arr):
    for i in range(1, len(arr)):
        element = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > element:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = element
    return arr

def bubble_sort(arr):
    for i in range(0, len(arr)):
        for j in range(0, len(arr) - 1 - i):
            if (arr[j] > arr[j+1]):
                aux = arr[j]
                arr[j] = arr[j+1]
                arr[j+1] = aux
    return arr

def gravity_sort(arr):
    max_val = max(arr)
    beads = [[0] * len(arr) for _ in range(max_val)]

    for col, val in enumerate(arr):
        for row in range(val):
            beads[row][col] = 1

    for row in beads:
        count = sum(row)
        for i in range(len(arr)):
            row[i] = 1 if i < count else 0

    sorted_arr = [sum(row[i] for row in beads) for i in range(len(arr))]
    return sorted_arr[::-1]

def bogo_sort(arr):
    sorted = False
    while not sorted:
        sorted = True
        for i in range(1, len(arr)):
            if (arr[i] < arr[i - 1]):
                sorted = False
                random.shuffle(arr)
    return arr

def sleep_sort(arr):
    result = []

    def sleep(x):
        time.sleep(x)
        result.append(x)

    threads = []
    for num in arr:
        t = threading.Thread(target=sleep, args=(num,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    return result

def pigeonhole_sort(arr):
    minimum = min(arr)
    maximum = max(arr)
    size = maximum - minimum + 1
    holes = [[] for _ in range(size)]

    # Place elements into their pigeonholes
    for i, x in enumerate(arr):
        holes[x - minimum].append(x)

    # Reconstruct sorted array
    i = 0
    for hole_index, hole in enumerate(holes):
        for num in hole:
            arr[i] = num
            i += 1

    return arr

algorithms = [radix_LSD_sort, counting_sort, pigeonhole_sort, merge_sort, insertion_sort, bubble_sort, gravity_sort, sleep_sort, bogo_sort]
names = ['radix', 'counting', 'pigeonhole', 'merge', 'insertion', 'bubble', 'gravity', 'sleep', 'bogo']

selected = input('Escolha um algoritmo entre os a seguir:\nradix, counting, pigeonhole, merge, insertion, bubble, gravity, sleep, bogo:\n').strip().lower()

if selected in names:
    
    arr = [int(x) for x in input('Escreva os números da lista, separados por vírgula:\n').split(',')]
    i = names.index(selected)
    start = time.perf_counter_ns()
    res = algorithms[i](arr)
    end = time.perf_counter_ns()

    elapsed_ns = end - start

    # Determine the most appropriate unit
    if elapsed_ns < 1_000:
        display_time = f"{elapsed_ns} nanosegundos"
    elif elapsed_ns < 1_000_000:
        display_time = f"{elapsed_ns / 1_000:.2f} microsegundos"
    elif elapsed_ns < 1_000_000_000:
        display_time = f"{elapsed_ns / 1_000_000:.2f} milisegundos"
    else:
        display_time = f"{elapsed_ns / 1_000_000_000:.4f} segundos"

    print(f'Lista ordenada: {res}. \nLevou {display_time}')