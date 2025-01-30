from functools import singledispatch
from .utils import moyenne_erreur, sorensen_dice

def levenshtein_with_union(ref, hyp, cost_func=None, u_cost=None):
    """
    Compute a modified Levenshtein distance with union and split operations.

    Parameters:
    - ref (str): Reference string.
    - hyp (str): Hypothesis string.
    - cost_func (callable, optional): Custom substitution cost function.
    - u_cost (float, optional): Cost for union and split operations.

    Returns:
    - int: Levenshtein distance with union and split costs.
    """

    if not ref.strip() or not hyp.strip():
        raise ValueError("Reference or hypothesis string is empty or contains only whitespace.")

    ref_words = ref.split()
    hyp_words = hyp.split()
    n = len(ref_words)
    m = len(hyp_words)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    # Verify and assign substitution cost function
    if isinstance(cost_func, str) and cost_func == "moyenne":
        cost_func = moyenne_erreur
    elif cost_func is None or not callable(cost_func):
        cost_func = sorensen_dice

    for i in range(n + 1):
        for j in range(m + 1):
            if i == 0:
                dp[i][j] = j  # insertion
            elif j == 0:
                dp[i][j] = i  # deletion
            else:
                sub_cost = cost_func(ref_words[i - 1], hyp_words[j - 1])
                dp[i][j] = min(dp[i - 1][j] + 1,  # deletion
                               dp[i][j - 1] + 1,  # insertion
                               dp[i - 1][j - 1] + sub_cost)  # substitution

                # Define union_cost by default if not provided
                if u_cost is None:
                    union_cost_value = 1 / len(ref_words[i - 1])
                    split_cost_value = 1 / len(hyp_words[j - 1])
                else:
                    union_cost_value = u_cost
                    split_cost_value = u_cost

                # Union operation (merge two words into one)
                if j > 1 and (hyp_words[j - 2] + hyp_words[j - 1]) == ref_words[i - 1]:
                    dp[i][j] = min(dp[i][j], dp[i - 1][j - 2] + union_cost_value)

                # Split operation (split one word into two)
                if i > 1 and (ref_words[i - 2] + ref_words[i - 1]) == hyp_words[j - 1]:
                    dp[i][j] = min(dp[i][j], dp[i - 2][j - 1] + split_cost_value)

    distance = dp[n][m]
    return distance



@singledispatch
def uwer(ref, hyp, cost_func=None, u_cost=None):
    raise NotImplementedError("Type not supported for 'uwer'")


@uwer.register(str)
def _(ref: str, hyp: str, cost_func=None, u_cost=None):
    distance = levenshtein_with_union(ref, hyp, cost_func=cost_func, u_cost=u_cost)
    len_ref = len(ref.split())
    if len_ref == 0:
        raise ValueError("One or more references are empty strings")
    wer_value = distance / len_ref
    return wer_value


@uwer.register(list)
def _(ref_list: list, hyp_list: list, cost_func=None, u_cost=None):
    if not ref_list or not hyp_list:
        raise ValueError("Reference or hypothesis list is empty.")
    if len(ref_list) != len(hyp_list):
        raise ValueError("Reference and hypothesis lists must be the same length")

    total_errors = 0
    total_words = 0

    for ref, hyp in zip(ref_list, hyp_list):
        distance = levenshtein_with_union(ref, hyp, cost_func=cost_func, u_cost=u_cost)
        total_errors += distance
        total_words += len(ref.split())

    if total_words == 0:
        return 0

    total_wer = total_errors / total_words
    return total_wer
