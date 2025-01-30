from fuzzywuzzy import fuzz
import textdistance
from jiwer import cer

def lcs_length_optimized(A, B):
    m = len(A)
    n = len(B)

    if m < n:
        A, B = B, A
        m, n = n, m

    # Use two rows instead of a full 2D array
    previous = [0] * (n + 1)
    current = [0] * (n + 1)

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if A[i - 1] == B[j - 1]:
                current[j] = previous[j - 1] + 1
            else:
                current[j] = max(previous[j], current[j - 1])
        previous, current = current, previous

    return previous[n]


def similarity_rate_lcs(A, B):
    lcs_len = lcs_length_optimized(A, B)
    max_len = max(len(A), len(B))
    return (lcs_len / max_len) * 100

def jaccard_coefficient_lcs(A, B):

    lcs_len = lcs_length_optimized(A, B)
    len_A = len(A)
    len_B = len(B)
    return lcs_len / (len_A + len_B - lcs_len)

def moyenne_erreur(ref, hyp):

    val_cer = cer(ref, hyp)
    val_smili = 1-(similarity_rate_lcs(ref, hyp) / 100)
    val_jaccard_lcs = 1-jaccard_coefficient_lcs(ref, hyp)
    fuzzy_ratio = 1-(fuzz.ratio(ref, hyp) / 100)
    sorensen_dice_sim =1- textdistance.sorensen_dice(ref, hyp)

    # Calcul de la moyenne des valeurs
    moyenne = (val_cer + val_smili + val_jaccard_lcs + fuzzy_ratio + sorensen_dice_sim) / 5

    return moyenne

def sorensen_dice(ref, hyp):
    ref_bigrams = set([tuple(ref[i:i + 2]) for i in range(len(ref) - 1)])
    hyp_bigrams = set([tuple(hyp[i:i + 2]) for i in range(len(hyp) - 1)])
    intersection = ref_bigrams.intersection(hyp_bigrams)
    similarity_score = 2 * len(intersection) / (len(ref_bigrams) + len(hyp_bigrams)) if (len(ref_bigrams) + len(hyp_bigrams)) else 1
    return 1 -similarity_score

def jaro(s, t):
    '''
    Calculate the Jaro distance between two strings.

    Parameters:
        s (str): First string.
        t (str): Second string.

    Returns:
        float: Jaro distance between s and t.
    '''

    # Length of the input strings
    s_len = len(s)
    t_len = len(t)

    # If both strings are empty, return 1 (identical)
    if s_len == 0 and t_len == 0:
        return 1.0

    # Maximum distance for matching characters
    match_distance = (max(s_len, t_len) // 2) - 1

    # Lists to keep track of matched characters
    s_matches = [False] * s_len
    t_matches = [False] * t_len

    matches = 0
    transpositions = 0

    # Find matching characters
    for i in range(s_len):
        start = max(0, i - match_distance)
        end = min(i + match_distance + 1, t_len)

        for j in range(start, end):
            if t_matches[j]:
                continue
            if s[i] != t[j]:
                continue
            s_matches[i] = True
            t_matches[j] = True
            matches += 1
            break

    # If no characters match, return 0 (completely dissimilar)
    if matches == 0:
        return 0.0

    # Count transpositions
    k = 0
    for i in range(s_len):
        if not s_matches[i]:
            continue
        while not t_matches[k]:
            k += 1
        if s[i] != t[k]:
            transpositions += 1
        k += 1

    transpositions //= 2

    # Calculate Jaro distance
    return ((matches / s_len) +
            (matches / t_len) +
            ((matches - transpositions) / matches)) / 3.0

def sorensen_dice_pos(ref, hyp):
    ref_bigrams = set([tuple(ref[i:i + 2]) for i in range(len(ref) - 1)])
    hyp_bigrams = set([tuple(hyp[i:i + 2]) for i in range(len(hyp) - 1)])
    intersection = ref_bigrams.intersection(hyp_bigrams)
    similarity_score = 2 * len(intersection) / (len(ref_bigrams) + len(hyp_bigrams)) if (len(ref_bigrams) + len(hyp_bigrams)) else 1
    return similarity_score