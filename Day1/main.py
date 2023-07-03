import requests
import numpy as np

words = []


def download_dict():
    # Using a list sorted by frequency because I want more frequent stuff to be prioritized
    link = "https://raw.githubusercontent.com/david47k/top-english-wordlists/master/top_english_words_mixed_1000000.txt"
    r = requests.get(link).text
    for word in r.split("\n"):
        words.append(word.lower())


def levenshtein_distance(word1, word2):
    m = len(word1)
    n = len(word2)

    # Create a distance matrix
    dp = np.zeros((m + 1, n + 1))

    # Initialize the first row and column of the matrix
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Fill in the rest of the matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1

    return dp[m][n]


def correct_word(string):
    if string in words[:100000]:
        return string
    else:
        lowest_word = ""
        lowest_word_number = -1
        for word in words[:100000]:
            distance = levenshtein_distance(string, word)
            if distance < lowest_word_number or lowest_word_number == -1:
                lowest_word = word
                lowest_word_number = distance

        return lowest_word


download_dict()
print(correct_word("helo"))
