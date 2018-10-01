def min_cost(i, j, cost_matrix):

    # iterating over first column and computing cost
    # for traversing till the element (i, 0)
    for m in range(1, i + 1):
        cost_matrix[m][0] = cost_matrix[m - 1][0] + cost_matrix[m][0]

    # iterating over first row and computing cost
    # for traversing till the element (j, 0)
    for n in range(1, j + 1):
        cost_matrix[0][n] = cost_matrix[0][n - 1] + cost_matrix[0][n]

    # iterating over remaining entries for which the
    # cost for top and left elements have already
    # been computed
    for m in range(1, i + 1):
        for n in range(1, j + 1):
            cost_matrix[m][n] = min(cost_matrix[m - 1][n],
                                    cost_matrix[m][n - 1]) \
                                      + cost_matrix[m][n]

    return cost_matrix[i][j]


def longestPalSubstr(string):
    maxLength = 1

    start = 0
    length = len(string)

    low = 0
    high = 0

    # One by one consider every character as center point of
    # even and length palindromes
    for i in xrange(1, length):
        # Find the longest even length palindrome with center
        # points as i-1 and i.
        low = i - 1
        high = i
        while low >= 0 and high < length and string[low] == string[high]:
            if high - low + 1 > maxLength:
                start = low
                maxLength = high - low + 1
            low -= 1
            high += 1

        # Find the longest odd length palindrome with center
        # point as i
        low = i - 1
        high = i + 1
        while low >= 0 and high < length and string[low] == string[high]:
            if high - low + 1 > maxLength:
                start = low
                maxLength = high - low + 1
            low -= 1
            high += 1

    print "Longest palindrome substring is:",
    print string[start:start + maxLength]

    return maxLength

cache = {}

def longest_pallindrome(input_string):
    if input_string in cache:
        return cache[input_string]
    if len(input_string) == 0:
        longest_length = 0
    elif len(input_string) == 1:
        longest_length = 1
    else:
        if input_string[0] is input_string[-1]:
            longest_length = 2 + longest_pallindrome(input_string[1:-1])
        else:
            longest_length = max(longest_pallindrome(input_string[1:]), longest_pallindrome(input_string[:-1]))
    cache[input_string] = longest_length
    return longest_length

# print(longest_pallindrome('animal'))
print(min_cost(1,2, [[1,1,1],[1,1,3]]))
# print(longestPalSubstr('d a b b d d e a c a b c a a d c b c e a e d b a e b a a e d e d c e b c e d e c d a b b a b a b d b b b b e d d a d a b e d c d e d b a b b b e e b d b e c b b c b c e b b e c a a a d d c a b e c e e a d d c b d a c c e e b c a e e b d d a d c d c a b a e e e b a e e a c a d d a c c b e c b c d b b e d c c a b b c b b a d b e e a b d b a e c c d e a a c c c d d e a c b e b a c c b b e c e c a e e e e e a c b c a b e b d c c e e c d a b e c c d a c c e a e a a c d b a e b c d c c c e b d b b d b b d a c e e a b b e e e b a e d d e d a e b d e a a a c b d d b d b c e e a c b a d d b d c c a a e e c e c a a b e d e e b b a d e c d a e e e e e a d b e e e e b d a e e b e c b d b a a b e e b d b e c e a e a e b a c d b d c b c b d a e c d d d b a d b b e d b b c c b a c e d e d b c a b c c d c'))