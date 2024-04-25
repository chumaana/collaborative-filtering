import numpy as np


def cosine_similarity(book_ratings1, book_ratings2):
    ratings1 = np.array(book_ratings1)
    ratings2 = np.array(book_ratings2)

    dot_product = np.dot(ratings1, ratings2)
    norm_ratings1 = np.linalg.norm(ratings1)
    norm_ratings2 = np.linalg.norm(ratings2)

    similarity = dot_product / (norm_ratings1 * norm_ratings2)

    return similarity


def pearson_correlation(book_ratings1, book_ratings2):
    ratings1 = np.array(book_ratings1)
    ratings2 = np.array(book_ratings2)

    mean_ratings1 = np.mean(ratings1)
    mean_ratings2 = np.mean(ratings2)

    std_ratings1 = np.std(ratings1)
    std_ratings2 = np.std(ratings2)

    covariance = np.mean((ratings1 - mean_ratings1) * (ratings2 - mean_ratings2))

    correlation = covariance / (std_ratings1 * std_ratings2)

    return correlation


def spearman_rank_correlation(book_ratings1, book_ratings2):
    ratings1 = np.array(book_ratings1)
    ratings2 = np.array(book_ratings2)

    rank_ratings1 = np.argsort(ratings1)
    rank_ratings2 = np.argsort(ratings2)

    ranked_ratings1 = np.empty(len(ratings1))
    ranked_ratings2 = np.empty(len(ratings2))

    for i, idx in enumerate(rank_ratings1):
        ranked_ratings1[idx] = i

    for i, idx in enumerate(rank_ratings2):
        ranked_ratings2[idx] = i

    squared_diff = np.sum(np.square(ranked_ratings1 - ranked_ratings2))
    correlation = 1 - (6 * squared_diff) / (len(ratings1) * (len(ratings1) ** 2 - 1))

    return correlation
