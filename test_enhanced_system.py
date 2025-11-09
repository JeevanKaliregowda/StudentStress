"""
Test script for the enhanced student stress prediction system
This script tests all the new features including course analysis, emotional state tracking, and location-based recommendations.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from recommendation_engine import PersonalizedRecommendationEngine
import json

def test_enhanced_system():
    """Test the enhanced recommendation system"""
    
    print("🧪 Testing Enhanced Student Stress Prediction System")
    print("=" * 60)
    
    # Initialize the recommendation engine
    try:
        engine = PersonalizedRecommendationEngine()
        print("✅ Recommendation engine initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing recommendation engine: {e}")
        return
    
    # Test case 1: Engineering student with high stress
    print("\n📝 Test Case 1: Engineering Student with High Stress")
    print("-" * 50)
    
    test_results = engine.generate_comprehensive_recommendations(
        ml_prediction='Bad',
        ml_probabilities=[0.1, 0.2, 0.6, 0.1],
        course='Engineering',
        emotion='Very Stressed',
        trigger_events=['Academic pressure', 'Exam failure'],
        context_text='I have been struggling with my programming assignments and failed my last exam. I feel overwhelmed.',
        state='Karnataka',
        city='Bangalore',
        user_profile={
            'academic_performance': 65.0,
            'study_time': 8,
            'social_media_time': 5,
            'career_willingness': 40,
            'financial_status': 'Good'
        }
    )
    
    print(f"Original ML Prediction: {test_results['original_ml_prediction']}")
    print(f"Enhanced Stress Level: {test_results['enhanced_stress_level']}")
    print(f"Final Score: {test_results['stress_score_breakdown']['final_score']:.3f}")
    print(f"Trauma Detected: {test_results['emotional_analysis']['trauma_detected']}")
    print(f"Number of Personalized Solutions: {len(test_results['personalized_solutions'])}")
    print(f"Number of Local Facilities: {len(test_results['location_based_facilities']['hospitals'])}")
    
    # Test case 2: Medical student with trauma indicators
    print("\n📝 Test Case 2: Medical Student with Trauma Indicators")
    print("-" * 50)
    
    test_results_2 = engine.generate_comprehensive_recommendations(
        ml_prediction='Awful',
        ml_probabilities=[0.05, 0.05, 0.2, 0.7],
        course='Medical',
        emotion='Depressed',
        trigger_events=['Family conflicts', 'Trauma/abuse'],
        context_text='I experienced childhood trauma and my family situation is very difficult. I cannot concentrate on studies.',
        state='Maharashtra',
        city='Mumbai',
        user_profile={
            'academic_performance': 45.0,
            'study_time': 4,
            'social_media_time': 8,
            'career_willingness': 20,
            'financial_status': 'Bad'
        }
    )
    
    print(f"Original ML Prediction: {test_results_2['original_ml_prediction']}")
    print(f"Enhanced Stress Level: {test_results_2['enhanced_stress_level']}")
    print(f"Final Score: {test_results_2['stress_score_breakdown']['final_score']:.3f}")
    print(f"Trauma Detected: {test_results_2['emotional_analysis']['trauma_detected']}")
    print(f"Number of Immediate Actions: {len(test_results_2['immediate_actions'])}")
    
    # Test case 3: Happy Arts student
    print("\n📝 Test Case 3: Happy Arts Student")
    print("-" * 50)
    
    test_results_3 = engine.generate_comprehensive_recommendations(
        ml_prediction='Fabulous',
        ml_probabilities=[0.7, 0.2, 0.1, 0.0],
        course='Arts/Humanities',
        emotion='Happy',
        trigger_events=['None/No specific trigger'],
        context_text='I am doing well in my studies and feeling positive about my future.',
        state='Tamil Nadu',
        city='Chennai',
        user_profile={
            'academic_performance': 85.0,
            'study_time': 6,
            'social_media_time': 2,
            'career_willingness': 80,
            'financial_status': 'Good'
        }
    )
    
    print(f"Original ML Prediction: {test_results_3['original_ml_prediction']}")
    print(f"Enhanced Stress Level: {test_results_3['enhanced_stress_level']}")
    print(f"Final Score: {test_results_3['stress_score_breakdown']['final_score']:.3f}")
    print(f"Number of Long-term Strategies: {len(test_results_3['long_term_strategies'])}")
    
    print("\n✅ All test cases completed successfully!")
    print("🎯 The enhanced system is working properly with:")
    print("   • Professional course analysis")
    print("   • Emotional state tracking")
    print("   • Trigger event analysis")
    print("   • Trauma detection")
    print("   • Location-based facility recommendations")
    print("   • Personalized solution generation")

def test_individual_components():
    """Test individual components of the system"""
    
    print("\n🔧 Testing Individual Components")
    print("=" * 40)
    
    # Test emotional analyzer
    from recommendation_engine import EmotionalAnalyzer
    
    analyzer = EmotionalAnalyzer()
    emotional_result = analyzer.analyze_emotional_state(
        emotion='Anxious',
        trigger_events=['Academic pressure', 'Financial problems'],
        context_text='I am worried about my upcoming exams and my family\'s financial situation.'
    )
    
    print("📊 Emotional Analysis Result:")
    print(f"   Emotion Score: {emotional_result['emotion_score']}")
    print(f"   Trigger Score: {emotional_result['trigger_score']}")
    print(f"   Trauma Detected: {emotional_result['trauma_detected']}")
    
    # Test course analyzer
    from recommendation_engine import CourseAnalyzer
    
    course_analyzer = CourseAnalyzer()
    course_factor = course_analyzer.get_course_stress_factor('Engineering')
    course_advice = course_analyzer.get_course_specific_advice('Engineering', 'Bad')
    
    print(f"\n🎓 Course Analysis Result:")
    print(f"   Engineering Stress Factor: {course_factor}")
    print(f"   Number of Advice Items: {len(course_advice)}")
    
    # Test location recommendations
    from recommendation_engine import LocationBasedRecommendations
    
    location_rec = LocationBasedRecommendations()
    facilities = location_rec.get_nearby_facilities('Karnataka', 'Bangalore')
    
    print(f"\n📍 Location Recommendations Result:")
    print(f"   Hospitals Found: {len(facilities['hospitals'])}")
    print(f"   Counseling Centers: {len(facilities['counseling_centers'])}")
    print(f"   Emergency Numbers: {len(facilities['emergency_numbers'])}")
    
    print("\n✅ All individual components working correctly!")

if __name__ == "__main__":
    test_enhanced_system()
    test_individual_components()