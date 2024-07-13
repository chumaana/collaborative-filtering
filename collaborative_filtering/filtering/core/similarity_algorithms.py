import numpy as np

def cosine_similarity(book_ratings1, book_ratings2):
    ratings1 = np.array([rating for _, rating in book_ratings1])
    ratings2 = np.array([rating for _, rating in book_ratings2])
    
    dot_product = np.dot(ratings1, ratings2)
    norm_ratings1 = np.linalg.norm(ratings1)
    norm_ratings2 = np.linalg.norm(ratings2)
    
    similarity = dot_product / (norm_ratings1 * norm_ratings2)
    
    return similarity

def pearson_correlation(book_ratings1, book_ratings2):
    ratings1 = np.array([rating for _, rating in book_ratings1])
    ratings2 = np.array([rating for _, rating in book_ratings2])
    
    mean_ratings1 = np.mean(ratings1)
    mean_ratings2 = np.mean(ratings2)
    
    std_ratings1 = np.std(ratings1)
    std_ratings2 = np.std(ratings2)
    
    covariance = np.mean((ratings1 - mean_ratings1) * (ratings2 - mean_ratings2))
    
    correlation = covariance / (std_ratings1 * std_ratings2)
    
    return correlation

def spearman_rank_correlation(book_ratings1, book_ratings2):
    ratings1 = np.array([rating for _, rating in book_ratings1])
    ratings2 = np.array([rating for _, rating in book_ratings2])
    
    rank_ratings1 = np.argsort(ratings1)
    rank_ratings2 = np.argsort(ratings2)
    
    ranked_ratings1 = np.empty(len(ratings1))
    ranked_ratings2 = np.empty(len(ratings2))
    
    for i, idx in enumerate(rank_ratings1):
        ranked_ratings1[idx] = i
        
    for i, idx in enumerate(rank_ratings2):
        ranked_ratings2[idx] = i
        
    squared_diff = np.sum(np.square(ranked_ratings1 - ranked_ratings2))
    correlation = 1 - (6 * squared_diff) / (len(ratings1) * (len(ratings1)**2 - 1))
    
    return correlation

book_ratings1 = [(1, 4), (2, 4), (3, 3), (4, 2), (5, 5)]
book_ratings2 = [(1, 4), (2, 4), (3, 3), (4, 2), (5, 5)]

cosine_sim = cosine_similarity(book_ratings1, book_ratings2)
print("Cosine Similarity:", cosine_sim)

pearson_corr = pearson_correlation(book_ratings1, book_ratings2)
print("Pearson Correlation Coefficient:", pearson_corr)

spearman_corr = spearman_rank_correlation(book_ratings1, book_ratings2)
print("Spearman Rank Correlation Coefficient:", spearman_corr)

def predict_ratings(new_user_ratings, existing_users_ratings, similarity_function):
    predicted_ratings = []
    
    for book_id, _ in new_user_ratings:
        numerator = 0
        denominator = 0
        
        for existing_user_ratings in existing_users_ratings:
            similarity = similarity_function(new_user_ratings, existing_user_ratings)
            existing_rating = next((rating for book_id_existing, rating in existing_user_ratings if book_id_existing == book_id), None)
            if existing_rating is not None:
                numerator += similarity * existing_rating
                denominator += similarity
        
        if denominator != 0:
            predicted_rating = numerator / denominator
            predicted_ratings.append((book_id, predicted_rating))
        else:
            predicted_ratings.append((book_id, None))
                
    return predicted_ratings

user1_ratings = [(1, 4), (4, 2), (5, 4)]
user2_ratings = [(1, 5),  (4, 2), (5, 5)]
new_user_ratings = [(1, 5), (4, 4), (5, 3)]

existing_users_ratings = [user1_ratings, user2_ratings]

predicted_ratings = predict_ratings(new_user_ratings, existing_users_ratings, cosine_similarity)

print("Predicted ratings for new user:", predicted_ratings)
