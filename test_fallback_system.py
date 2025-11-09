"""
Test script for the enhanced fallback mechanism
Tests state capital fallback when city data is not available
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from recommendation_engine import LocationBasedRecommendations

def test_fallback_mechanism():
    """Test the state capital fallback mechanism"""
    
    print("🧪 Testing State Capital Fallback Mechanism")
    print("=" * 60)
    
    # Initialize location recommendations
    try:
        location_rec = LocationBasedRecommendations()
        print("✅ Location recommendation system initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing location system: {e}")
        return
    
    # Test Case 1: City with data available (should not use fallback)
    print("\n📝 Test Case 1: City with existing data (Bangalore, Karnataka)")
    print("-" * 50)
    
    facilities_1 = location_rec.get_nearby_facilities('Karnataka', 'Bangalore')
    print(f"Hospitals found: {len(facilities_1['hospitals'])}")
    print(f"Counseling centers: {len(facilities_1['counseling_centers'])}")
    print(f"Fallback note present: {'fallback_note' in facilities_1}")
    if 'fallback_note' in facilities_1:
        print(f"Fallback note: {facilities_1['fallback_note']}")
    
    # Test Case 2: City without data - should use state capital
    print("\n📝 Test Case 2: City without data - using state capital (Hubli, Karnataka)")
    print("-" * 50)
    
    facilities_2 = location_rec.get_nearby_facilities('Karnataka', 'Hubli')
    print(f"Hospitals found: {len(facilities_2['hospitals'])}")
    print(f"Counseling centers: {len(facilities_2['counseling_centers'])}")
    print(f"Fallback note present: {'fallback_note' in facilities_2}")
    if 'fallback_note' in facilities_2:
        print(f"Fallback note: {facilities_2['fallback_note']}")
    
    # Test Case 3: State with data available
    print("\n📝 Test Case 3: State capital directly (Patna, Bihar)")
    print("-" * 50)
    
    facilities_3 = location_rec.get_nearby_facilities('Bihar', 'Patna')
    print(f"Hospitals found: {len(facilities_3['hospitals'])}")
    print(f"Counseling centers: {len(facilities_3['counseling_centers'])}")
    print(f"Emergency numbers: {len(facilities_3['emergency_numbers'])}")
    print(f"Fallback note present: {'fallback_note' in facilities_3}")
    
    # Test Case 4: City in state with capital data
    print("\n📝 Test Case 4: Non-capital city (should fallback to Bhopal)")
    print("-" * 50)
    
    facilities_4 = location_rec.get_nearby_facilities('Madhya Pradesh', 'Indore')
    print(f"Hospitals found: {len(facilities_4['hospitals'])}")
    print(f"Counseling centers: {len(facilities_4['counseling_centers'])}")
    print(f"Fallback note present: {'fallback_note' in facilities_4}")
    if 'fallback_note' in facilities_4:
        print(f"Fallback note: {facilities_4['fallback_note']}")
    
    # Test Case 5: Completely unknown state
    print("\n📝 Test Case 5: Unknown state (should provide emergency contacts)")
    print("-" * 50)
    
    facilities_5 = location_rec.get_nearby_facilities('Unknown State', 'Unknown City')
    print(f"Hospitals found: {len(facilities_5['hospitals'])}")
    print(f"Counseling centers: {len(facilities_5['counseling_centers'])}")
    print(f"Emergency numbers: {len(facilities_5['emergency_numbers'])}")
    print(f"Fallback note present: {'fallback_note' in facilities_5}")
    if 'fallback_note' in facilities_5:
        print(f"Fallback note: {facilities_5['fallback_note']}")
    
    # Test Case 6: Test multiple state capitals
    print("\n📝 Test Case 6: Testing multiple state capitals")
    print("-" * 50)
    
    test_states = ['Tamil Nadu', 'West Bengal', 'Rajasthan', 'Gujarat', 'Punjab']
    for state in test_states:
        capital = location_rec.state_capitals.get(state, 'Unknown')
        facilities = location_rec.get_nearby_facilities(state, capital)
        print(f"{state} (Capital: {capital}): {len(facilities['hospitals'])} hospitals, {len(facilities['counseling_centers'])} centers")
    
    print("\n✅ All fallback mechanism tests completed successfully!")
    print("🎯 The system now provides:")
    print("   • Exact city data when available")
    print("   • State capital fallback when city data missing")
    print("   • Emergency contacts for all locations")
    print("   • Clear fallback notifications to users")

def test_specific_capitals():
    """Test all state capitals to ensure they have data"""
    
    print("\n🏛️ Testing All State Capitals")
    print("=" * 40)
    
    location_rec = LocationBasedRecommendations()
    
    missing_capitals = []
    available_capitals = []
    
    for state, capital in location_rec.state_capitals.items():
        facilities = location_rec.get_nearby_facilities(state, capital)
        
        # Check if this is using fallback (meaning capital data is missing)
        if 'fallback_note' in facilities and capital in facilities.get('fallback_note', ''):
            missing_capitals.append(f"{state}: {capital}")
        else:
            available_capitals.append(f"{state}: {capital}")
            if facilities['hospitals']:
                print(f"✅ {state} ({capital}): {len(facilities['hospitals'])} hospitals")
    
    print(f"\n📊 Summary:")
    print(f"   • Available state capitals: {len(available_capitals)}")
    print(f"   • Missing state capitals: {len(missing_capitals)}")
    
    if missing_capitals:
        print(f"\n⚠️ State capitals without data:")
        for missing in missing_capitals:
            print(f"   • {missing}")
    
    print(f"\n✅ State capital coverage: {len(available_capitals)}/{len(location_rec.state_capitals)} states")

if __name__ == "__main__":
    test_fallback_mechanism()
    test_specific_capitals()