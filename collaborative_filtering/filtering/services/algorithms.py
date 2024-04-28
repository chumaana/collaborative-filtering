import math

import numpy as np
import pandas as pd


def cosine_similarity(book_ratings1, book_ratings2):
    ratings1 = np.array(book_ratings1)
    ratings2 = np.array(book_ratings2)

    dot_product = np.dot(ratings1, ratings2)
    norm_ratings1 = np.linalg.norm(ratings1)
    norm_ratings2 = np.linalg.norm(ratings2)

    if dot_product == (norm_ratings1 * norm_ratings2):
        return 1.0
    else:
        return dot_product / (norm_ratings1 * norm_ratings2)


def pearson_correlation(book_ratings1, book_ratings2):
    ratings1 = np.array(book_ratings1)
    ratings2 = np.array(book_ratings2)
    n = ratings1.shape[0]

    sum_product = np.sum(ratings1 * ratings2)
    sum_1 = np.sum(ratings1)
    sum_2 = np.sum(ratings2)
    sum_squared_1 = np.sum(ratings1 * ratings1)
    sum_squared_2 = np.sum(ratings2 * ratings2)
    coef = (n * sum_product - sum_1 * sum_2) / (
        math.sqrt((n * sum_squared_1 - math.pow(sum_1, 2)))
        * math.sqrt((n * sum_squared_2 - math.pow(sum_2, 2)))
    )
    return coef


def spearman_rank_correlation(book_ratings1, book_ratings2):
    n = len(book_ratings1)
    # if n < 5:
    #     return False
    ratings1 = np.array(book_ratings1)
    ratings2 = np.array(book_ratings2)

    table = pd.DataFrame(data={"book_ratings1": ratings1, "book_ratings2": ratings2})
    # print(table)

    ranked_ratings1 = table["book_ratings1"].rank()
    ranked_ratings2 = table["book_ratings2"].rank()
    ranked_ratings1 = pd.DataFrame(ranked_ratings1).to_numpy()
    ranked_ratings2 = pd.DataFrame(ranked_ratings2).to_numpy()

    squared_diff = np.sum(np.square(ranked_ratings1 - ranked_ratings2))

    correlation = 1 - (6 * squared_diff) / (n * (n**2 - 1))
    return correlation
