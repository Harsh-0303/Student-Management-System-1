from Model_layer.user_based import get_user_recommendations


recommendations = get_user_recommendations(1, top_n=10)


print("\nUser 1 Recommendations:")

print(recommendations)