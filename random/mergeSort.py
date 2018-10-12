def merge_sort(array):

    if len(array) == 1:
        return array
    length = len(array)
    sorted_array_1 = merge_sort(array[:length/2])
    sorted_array_2 = merge_sort(array[length/2:])

    sorted_array = []
    i, j = 0, 0
    for n in range(length):
        if (i < len(sorted_array_1) or j == len(sorted_array_2)) and sorted_array_1[i] <= sorted_array_2[j]:
            sorted_array.append(sorted_array_1[i])
            i += 1
        else:
            sorted_array.append(sorted_array_2[j])
            j += 1

    return sorted_array

print merge_sort([2,3,5,4])





