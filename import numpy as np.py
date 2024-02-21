import random
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity

# Function to create a profile for a given user
def create_profile(username):
    print(f"Creating profile for {username}:")
    interests = input("Enter your interests (separated by commas): ").split(',')
    age = int(input("Enter your age: "))
    return {'username': username, 'interests': interests, 'age': age}

# Function to create user interactions
def create_user_interactions(users):
    interactions = {}
    for user in users:
        interactions[user] = {}
        for other_user in users:
            if other_user != user:
                interaction = random.choice([0, 1])  # Simulate random interaction
                interactions[user][other_user] = interaction
    return interactions

# Function to compute similarity scores between profiles (content-based)
def compute_similarity(user_profile, all_profiles):
    mlb = MultiLabelBinarizer()
    user_interests = mlb.fit_transform([user_profile['interests']])
    similarities = {}
    for profile in all_profiles:
        profile_interests = mlb.transform([profile['interests']])
        cosine_sim = cosine_similarity(user_interests, profile_interests)[0][0]
        age_diff = abs(user_profile['age'] - profile['age']) / 100.0  # Normalize age difference
        total_similarity = cosine_sim + (1 - age_diff)  # Combine interests similarity and age similarity
        similarities[profile['username']] = total_similarity
    return similarities

# Function to recommend people using content-based filtering
def recommendation(user, user_profiles):
    user_profile = next(profile for profile in user_profiles if profile['username'] == user)
    content_similarity = compute_similarity(user_profile, user_profiles)
    sorted_recommendations = sorted(content_similarity.items(), key=lambda x: x[1], reverse=True)
    return [username for username, _ in sorted_recommendations if username != user]

# Function to recommend people using collaborative filtering
def collaborative_recommendation(user, user_interactions):
    sorted_interactions = sorted(user_interactions[user].items(), key=lambda x: x[1], reverse=True)
    return [other_user for other_user, interaction in sorted_interactions if interaction == 1]

# Main function
def main():
    # Sample data (user profiles)
    users = ['Alice', 'Bob', 'Charlie', 'David']
    user_profiles = [create_profile(user) for user in users]
    user_interactions = create_user_interactions(users)
    
    # Generate recommendations for each user
    for user in users:
        print(f"\nContent-based Recommendations for {user}: {recommendation(user, user_profiles)}")
        print(f"Collaborative Recommendations for {user}: {collaborative_recommendation(user, user_interactions)}")

# Execute the main function
main()
