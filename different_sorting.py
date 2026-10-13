import math

arr = list(map(int, input("Enter array: ").split()))
n = len(arr)

def bubble_sort(ar, n):
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if ar[j] > ar[j + 1]:
                tmp = ar[j]
                ar[j] = ar[j + 1]
                ar[j + 1] = tmp
                swapped = True
        if swapped == False:
            break
    return ar

def insertion_sort(ar, n):
    for i in range(1, n - 1):
        key = ar[i]
        j = i - 1
        while (j >= 0) and (ar[j] > key):
            #tmp = ar[j + 1]
            ar[j + 1] = a[j]
            j -= 1
        ar[j + 1] = key
    return ar

def selection_sort(ar, n):
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if ar[j] < min_idx:
                min_idx = j
        if min_idx != i:
            tmp = ar[i]
            ar[i] = ar[min_idx]
            ar[min_idx] = tmp
    return ar

def shell_sort(ar, n):
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            tmp = ar[i]
            j = i
            while (j >= gap) and (ar[j - gap] > tmp):
                ar[j] = ar[j - gap]
                j -= gap
            ar[j] = tmp
        gap = gap // 2
    return ar

def gnome_sort(ar, n):
    i = 0
    while i < n:
        if i == 0 or (ar[i - 1] <= ar[i]):
            i += 1
        else:
            tmp = ar[i - 1]
            ar[i - 1] = ar[i]
            ar[i] = tmp
    return ar

def comb_sort(ar, n):
    gap = n
    swapped = True
    while gap > 1 or swapped == True:
        gap = max(1, math.floor(gap / 1.3))
        swapped = False
        for i in range(n - gap):
            if ar[i] > ar[i + gap]:
                tmp = ar[i]
                ar[i] = ar[i + gap]
                ar[i + gap] = tmp
                swapped = True
    return ar

def quick_sort(ar, n):
    if n <= 1:
        return ar
    pivot = ar[n // 2]
    left = []
    mid = []
    right = []
    for x in ar:
        if x < pivot:
            left.append(x)
        elif x == pivot:
            mid.append(x)
        else:
            right.append(x)
    return quick_sort(left, len(left)) + mid + quick_sort(right, len(right))

def merge(a, b):
    res = []
    i, j = 0, 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            res.append(a[i])
            i += 1
        else:
            res.append(b[j])
            j += 1
    res.extend(a[i:])
    res.extend(b[j:])
    return res

def merge_sort(ar, n):
    if n <= 1:
        return ar
    mid = n // 2
    left = merge_sort(ar[:mid], mid)
    right = merge_sort(ar[mid:], (n - mid))
    return merge(left, right)

def heapify(ar, s, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < s and ar[l] > ar[largest]:
        largest = l
    if r < s and ar[r] > ar[largest]:
        largest = r
    if largest != i:
        tmp = ar[largest]
        ar[largest] = ar[i]
        ar[i] = tmp
        heapify(ar, s, largest)

def heap_sort(ar, n):
    for i in range((n // 2 - 1), 0):
        heapify(ar, n, i)
    for i in range((n - 1), 1):
        tmp = ar[i]
        ar[i] = ar[0]
        ar[0] = tmp
    return ar

def counting_sort(ar, n):
    if n == 0:
        return ar
    count = []
    res = []
    min_v = min(ar)
    max_v = max(ar)
    s = max_v - min_v + 1
    count = [0] * s
    for x in ar:
        count[x - min_v] += 1
    for v, c in enumerate(count):
        res.extend([v + min_v] * c)
    return res
