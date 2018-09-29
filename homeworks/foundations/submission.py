import collections
import math

############################################################
# Problem 3a

def findAlphabeticallyLastWord(text):
    """
    Given a string |text|, return the word in |text| that comes last
    alphabetically (that is, the word that would appear last in a dictionary).
    A word is defined by a maximal sequence of characters without whitespaces.
    You might find max() and list comprehensions handy here.
    """
    # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
    return max(text.lower().split())
    # END_YOUR_CODE

############################################################
# Problem 3b

def euclideanDistance(loc1, loc2):
    """
    Return the Euclidean distance between two locations, where the locations
    are pairs of numbers (e.g., (3, 5)).
    """
    # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
    return math.sqrt(sum((x - y) ** 2 for (x, y) in [(loc1[0], loc2[0]), (loc1[1], loc2[1])]))
    # END_YOUR_CODE

############################################################
# Problem 3c

def mutateSentences(sentence):
    """
    Given a sentence (sequence of words), return a list of all "similar"
    sentences.
    We define a sentence to be similar to the original sentence if
      - it as the same number of words, and
      - each pair of adjacent words in the new sentence also occurs in the original sentence
        (the words within each pair should appear in the same order in the output sentence
         as they did in the orignal sentence.)
    Notes:
      - The order of the sentences you output doesn't matter.
      - You must not output duplicates.
      - Your generated sentence can use a word in the original sentence more than
        once.
    Example:
      - Input: 'the cat and the mouse'
      - Output: ['and the cat and the', 'the cat and the mouse', 'the cat and the cat', 'cat and the cat and']
                (reordered versions of this list are allowed)
    """
    # BEGIN_YOUR_CODE (our solution is 20 lines of code, but don't worry if you deviate from this)
    def appended_options(a, options):
        return [a + [option] for option in options]
    words = sentence.split()
    next_options_map = {}
    for index, word in enumerate(words):
        if word not in next_options_map:
            next_options_map[word] = []
        if index + 1 < len(words):
            next_options_map[word].append(words[index + 1])
    results = []
    for key in next_options_map:
        results.append([key])
        i = 0
        while i < len(results):
            if len(results[i]) < len(words) and len(next_options_map[results[i][-1]]) > 0:
                results += appended_options(results[i], next_options_map[results[i][-1]])
                del results[i]
            else:
                i += 1
    return list(set([' '.join(result) for result in results if len(result) == len(words)]))

    # END_YOUR_CODE

############################################################
# Problem 3d

def sparseVectorDotProduct(v1, v2):
    """
    Given two sparse vectors |v1| and |v2|, each represented as collections.defaultdict(float), return
    their dot product.
    You might find it useful to use sum() and a list comprehension.
    This function will be useful later for linear classifiers.
    """
    # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)
    return sum(value*v2[index] for index, value in v1.iteritems())
    # END_YOUR_CODE

############################################################
# Problem 3e

def incrementSparseVector(v1, scale, v2):
    """
    Given two sparse vectors |v1| and |v2|, perform v1 += scale * v2.
    This function will be useful later for linear classifiers.
    """
    # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
    v = collections.defaultdict(float, [(index, value + v1[index]) for index, value in [(index, value*scale) for index, value in v2.iteritems()]])
    v1.update(v)
    # END_YOUR_CODE

############################################################
# Problem 3f

def findSingletonWords(text):
    """
    Splits the string |text| by whitespace and returns the set of words that
    occur exactly once.
    You might find it useful to use collections.defaultdict(int).
    """
    # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)
    count_map = collections.defaultdict(int)
    for word in text.split():
        count_map[word] += 1
    return set([v for v in count_map if count_map[v] == 1])
    # END_YOUR_CODE

############################################################
# Problem 3g

def computeLongestPalindromeLength(text):
    """
    A palindrome is a string that is equal to its reverse (e.g., 'ana').
    Compute the length of the longest palindrome that can be obtained by deleting
    letters from |text|.
    For example: the longest palindrome in 'animal' is 'ama'.
    Your algorithm should run in O(len(text)^2) time.
    You should first define a recurrence before you start coding.
    """
    # BEGIN_YOUR_CODE (our solution is 19 lines of code, but don't worry if you deviate from this)
    def last_index(string, character): return len(string) - 1 - string[::-1].index(character)

    def find_palindromes(string, side):
        possibilities = []
        for c in string:
            if string.index(c) is not last_index(string, c):
                sub_possibilities = find_palindromes(string[string.index(c) + 1: last_index(string, c)], side + c)
                if len(sub_possibilities) == 0:
                    possibilities.append(side + c + c + side[::-1])
                else:
                    possibilities += sub_possibilities
                break
            else:
                possibilities.append(side + c + side[::-1])
        return possibilities
    palindromes = find_palindromes(text, '')
    return len(max(palindromes, key=len)) if len(palindromes) > 0 else 0
    # END_YOUR_CODE
