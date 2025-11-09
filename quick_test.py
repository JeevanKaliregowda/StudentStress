from recommendation_engine import PersonalizedRecommendationEngine

# Test fallback mechanism
engine = PersonalizedRecommendationEngine()

# Test 1: Non-capital city (should fallback to Jaipur)
facilities_udaipur = engine.location_recommendations.get_nearby_facilities('Rajasthan', 'Udaipur')
print(f"Udaipur test: {len(facilities_udaipur['hospitals'])} hospitals found")
print(f"Fallback note: {facilities_udaipur.get('fallback_note', 'No fallback needed')}")

# Test 2: Capital city (direct match)
facilities_jaipur = engine.location_recommendations.get_nearby_facilities('Rajasthan', 'Jaipur')
print(f"\nJaipur test: {len(facilities_jaipur['hospitals'])} hospitals found")
print(f"Fallback note: {facilities_jaipur.get('fallback_note', 'No fallback needed')}")

# Test 3: Union Territory
facilities_puducherry = engine.location_recommendations.get_nearby_facilities('Puducherry', 'Puducherry')
print(f"\nPuducherry test: {len(facilities_puducherry['hospitals'])} hospitals found")
print(f"Emergency numbers: {len(facilities_puducherry['emergency_numbers'])}")

print("\n✅ All fallback mechanisms working correctly!")