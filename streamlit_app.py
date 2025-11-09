import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import datetime
import json
from recommendation_engine import PersonalizedRecommendationEngine

# Load the trained model and mappings
@st.cache_resource
def load_model():
    try:
        model = joblib.load('stress_prediction_models.pkl')
        st.success('Model loaded successfully!')
        return model
    except Exception as e:
        st.error(f'Could not load model: {e}')
        return None

@st.cache_resource
def load_location_data():
    """Load state and city data"""
    try:
        with open('state_city_data.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f'Could not load location data: {e}')
        return {}

@st.cache_resource
def initialize_recommendation_engine():
    """Initialize the recommendation engine"""
    try:
        return PersonalizedRecommendationEngine()
    except Exception as e:
        st.error(f'Could not initialize recommendation engine: {e}')
        return None

def get_psychological_risks_and_actions(stress_level):
    """Get psychological risks and recommended actions based on stress level"""
    
    guidance = {
        'Fabulous': {
            'status': '🌟 Excellent Mental Health!',
            'risks': [
                '✅ Minimal psychological risk',
                '✅ Strong emotional resilience',
                '✅ Healthy coping mechanisms in place',
                '✅ Good work-life balance'
            ],
            'actions': [
                '🧘 Continue current stress management practices',
                '🏃 Maintain regular physical activity',
                '😴 Keep healthy sleep schedule (7-9 hours)',
                '🤝 Nurture social connections',
                '📚 Consider mentoring others with stress management'
            ]
        },
        'Good': {
            'status': '😊 Good Mental Health with Minor Concerns',
            'risks': [
                '⚠️ Mild anxiety during exams',
                '⚠️ Occasional sleep disruption',
                '⚠️ Risk of perfectionism creating pressure',
                '⚠️ Tendency to compare with peers'
            ],
            'actions': [
                '🧘 Practice 15 minutes daily meditation',
                '📝 Start a stress journal',
                '🏃 Exercise 30 minutes daily',
                '😴 Establish consistent sleep routine',
                '📱 Limit social media before bed',
                '💬 Talk to counselor if overwhelmed'
            ]
        },
        'Bad': {
            'status': '😰 Elevated Stress - Action Needed',
            'risks': [
                '🚨 Risk of anxiety disorders',
                '🚨 Potential depression symptoms',
                '🚨 Academic burnout possible',
                '🚨 Physical health issues (headaches, fatigue)',
                '🚨 Social withdrawal tendencies',
                '🚨 Concentration and memory problems'
            ],
            'actions': [
                '🏥 **SEEK PROFESSIONAL COUNSELING** - Don\'t wait',
                '😴 **Prioritize sleep** - 7-9 hours mandatory',
                '🧘 **Daily stress relief** - Meditation/yoga required',
                '🏃 **Physical activity** - 20+ minutes daily',
                '🤝 **Reach out** - Talk to friends, family, counselors',
                '📵 **Digital detox** - Reduce screen time',
                '📚 **Academic support** - Tutoring, study groups',
                '🏥 **Campus counseling center** - Free services available'
            ]
        },
        'Awful': {
            'status': '🚨 CRITICAL - Immediate Help Required',
            'risks': [
                '🚨 SEVERE: Major depression risk',
                '🚨 SEVERE: Anxiety and panic disorders',
                '🚨 SEVERE: Suicidal ideation possible',
                '🚨 SEVERE: Complete academic failure',
                '🚨 SEVERE: Physical health crisis',
                '🚨 SEVERE: Social isolation',
                '🚨 SEVERE: Substance abuse risk'
            ],
            'actions': [
                '🆘 **EMERGENCY: Call crisis hotline immediately**',
                '📞 **India - AASRA**: 9820466726 (24/7)',
                '📞 **India - Vandrevala**: 9999666555',
                '📞 **India - Sneha**: 044-24640050',
                '🏥 **Visit Emergency Room** if having suicidal thoughts',
                '🤝 **Don\'t be alone** - Stay with trusted person',
                '💊 **Avoid alcohol/drugs**',
                '👨‍⚕️ **See psychiatrist** for medication evaluation',
                '🧠 **Intensive therapy** required immediately',
                '🏥 **Campus health services** - Seek help today'
            ]
        }
    }
    
    return guidance.get(stress_level, guidance['Good'])

def predict_stress_level(mark10th, mark12th, collegemark, carrer_willing, smtime, financial):
    """Simple rule-based prediction"""
    
    academic_avg = (mark10th + mark12th + collegemark) / 3
    risk_score = 0
    
    # Academic factors
    if academic_avg < 50:
        risk_score += 3
    elif academic_avg < 70:
        risk_score += 1
    
    # Career factors
    if carrer_willing < 30:
        risk_score += 2
    elif carrer_willing < 60:
        risk_score += 1
    
    # Social media
    if smtime > 8:
        risk_score += 2
    elif smtime > 5:
        risk_score += 1
    
    # Financial
    if financial == 'Awful':
        risk_score += 2
    elif financial == 'Bad':
        risk_score += 1
    
    # Map to stress level
    if risk_score >= 6:
        return 'Awful', [0.1, 0.1, 0.2, 0.6]
    elif risk_score >= 4:
        return 'Bad', [0.1, 0.2, 0.6, 0.1]
    elif risk_score >= 2:
        return 'Good', [0.2, 0.6, 0.1, 0.1]
    else:
        return 'Fabulous', [0.6, 0.3, 0.1, 0.0]

# App title
st.title('🎓 Enhanced Student Stress Level Predictor')
st.markdown('### AI-Powered Mental Health Assessment with Personalized Recommendations')

# Load model and data
model_data = load_model()
location_data = load_location_data()
recommendation_engine = initialize_recommendation_engine()

# Create three columns for input
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader('📚 Academic Information')
    mark10th = st.slider('10th Grade Marks (%)', 30, 100, 75)
    mark12th = st.slider('12th Grade Marks (%)', 30, 100, 75)
    collegemark = st.slider('College Marks (%)', 30, 100, 75)
    
    # Professional Course Selection
    st.subheader('🎯 Professional Course')
    course_options = [
        'Engineering', 'Medical', 'Law', 'Commerce', 'Arts/Humanities', 
        'Science', 'MBA', 'Computer Science'
    ]
    professional_course = st.selectbox('Select your professional course:', course_options)
    
    st.subheader('👤 Personal Information')
    gender = st.selectbox('Gender', ['Male', 'Female'])
    height = st.slider('Height (cm)', 140, 200, 170)
    weight = st.slider('Weight (kg)', 30, 120, 65)

with col2:
    st.subheader('🏃 Lifestyle & Career')
    studytime = st.slider('Study Time (hours/day)', 0, 12, 6)
    smtime = st.slider('Social Media Time (hours/day)', 0, 24, 3)
    travel = st.slider('Travel Time (minutes)', 0, 180, 30)
    
    st.subheader('💰 Expectations & Status')
    salexpect = st.number_input('Salary Expectation (₹)', 10000, 2000000, 50000)
    carrer_willing = st.slider('Career Willingness (%)', 0, 100, 50)
    financial = st.selectbox('Financial Status', ['Awful', 'Bad', 'Good', 'Fabulous'])

with col3:
    st.subheader('😊 Current Emotional State')
    emotion_options = [
        'Very Happy', 'Happy', 'Content', 'Neutral', 'Slightly Stressed',
        'Stressed', 'Very Stressed', 'Anxious', 'Depressed', 'Overwhelmed',
        'Panicked', 'Hopeless'
    ]
    current_emotion = st.selectbox('How are you feeling right now?', emotion_options, index=3)
    
    st.subheader('⚡ Trigger Events')
    trigger_options = [
        'Academic pressure', 'Parent scolding/disappointment', 'Relationship issues/breakup',
        'Financial problems', 'Family conflicts', 'Health issues', 'Career uncertainty',
        'Social isolation', 'Exam failure', 'Peer pressure', 'Loss of loved one',
        'Trauma/abuse', 'None/No specific trigger'
    ]
    trigger_events = st.multiselect(
        'What events might have contributed to your current emotional state?',
        trigger_options,
        default=['None/No specific trigger']
    )
    
    st.subheader('📝 Additional Context')
    context_description = st.text_area(
        'Describe your current situation or any additional context:',
        placeholder='Optional: Share any additional details about your current emotional state, recent events, or concerns...',
        height=100
    )

# Location Section
st.subheader('📍 Your Location (for local mental health resources)')
loc_col1, loc_col2 = st.columns(2)

with loc_col1:
    states = list(location_data.keys()) if location_data else ['Karnataka', 'Maharashtra', 'Tamil Nadu', 'Delhi']
    selected_state = st.selectbox('Select your state:', states)

with loc_col2:
    cities = location_data.get(selected_state, ['Bangalore', 'Mumbai', 'Chennai', 'New Delhi'])
    selected_city = st.selectbox('Select your city:', cities)

# Predict button
if st.button('🔮 Predict Stress Level & Get Recommendations', type='primary'):
    if recommendation_engine is None:
        st.error('Recommendation engine not available. Using basic prediction.')
        # Fallback to original prediction method
        predicted_level, probabilities = predict_stress_level(
            mark10th, mark12th, collegemark, carrer_willing, smtime, financial
        )
        
        # Display basic results
        st.success('✅ Basic Prediction Completed!')
        col1, col2 = st.columns(2)
        with col1:
            st.metric('🎯 Predicted Stress Level', predicted_level)
        with col2:
            confidence = max(probabilities) * 100
            st.metric('🎚️ Confidence', f'{confidence:.1f}%')
    else:
        # Use enhanced prediction system
        with st.spinner('🔄 Analyzing your profile and generating personalized recommendations...'):
            # Get basic ML prediction first
            predicted_level, probabilities = predict_stress_level(
                mark10th, mark12th, collegemark, carrer_willing, smtime, financial
            )
            
            # Create user profile
            user_profile = {
                'academic_performance': (mark10th + mark12th + collegemark) / 3,
                'study_time': studytime,
                'social_media_time': smtime,
                'career_willingness': carrer_willing,
                'financial_status': financial,
                'gender': gender,
                'travel_time': travel
            }
            
            # Generate comprehensive recommendations
            comprehensive_results = recommendation_engine.generate_comprehensive_recommendations(
                ml_prediction=predicted_level,
                ml_probabilities=probabilities,
                course=professional_course,
                emotion=current_emotion,
                trigger_events=trigger_events,
                context_text=context_description,
                state=selected_state,
                city=selected_city,
                user_profile=user_profile
            )
            
            # Display enhanced results
            st.success('✅ Enhanced Analysis Completed!')
            
            # Main metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric('🎯 Original ML Prediction', comprehensive_results['original_ml_prediction'])
            with col2:
                st.metric('🔬 Enhanced Stress Level', comprehensive_results['enhanced_stress_level'])
            with col3:
                confidence = max(probabilities) * 100
                st.metric('🎚️ Confidence', f'{confidence:.1f}%')
            
            # Enhanced profile summary
            academic_avg = user_profile['academic_performance']
            st.info(f'📊 **Enhanced Profile**: Course: {professional_course} | Academic: {academic_avg:.1f}% | Emotion: {current_emotion} | Career: {carrer_willing}% | Financial: {financial}')
            
            # Stress score breakdown
            st.subheader('📊 Enhanced Stress Score Breakdown')
            breakdown = comprehensive_results['stress_score_breakdown']
            
            breakdown_col1, breakdown_col2 = st.columns(2)
            with breakdown_col1:
                st.write('**Factor Contributions:**')
                st.write(f'• ML Model Prediction: {breakdown["ml_model_contribution"]*100:.0f}%')
                st.write(f'• Professional Course Factor: {breakdown["course_factor_contribution"]*100:.0f}%')
                st.write(f'• Emotional State: {breakdown["emotional_state_contribution"]*100:.0f}%')
                st.write(f'• Trigger Events: {breakdown["trigger_events_contribution"]*100:.0f}%')
            
            with breakdown_col2:
                st.metric('🎯 Final Enhanced Score', f'{breakdown["final_score"]:.2f}')
                # Show probability chart
                prob_df = pd.DataFrame({
                    'Stress Level': ['Fabulous', 'Good', 'Bad', 'Awful'],
                    'Probability': probabilities
                })
                st.bar_chart(prob_df.set_index('Stress Level'))
            
            # Emotional Analysis Results
            emotional_analysis = comprehensive_results['emotional_analysis']
            if emotional_analysis['trauma_detected']:
                st.warning('⚠️ **Trauma indicators detected in your description.** Specialized support recommendations have been included.')
            
            # Display status with appropriate color
            enhanced_level = comprehensive_results['enhanced_stress_level']
            if enhanced_level == 'Fabulous':
                st.success(f'🌟 Enhanced Assessment: {enhanced_level}')
            elif enhanced_level == 'Good':
                st.info(f'😊 Enhanced Assessment: {enhanced_level}')
            elif enhanced_level == 'Bad':
                st.warning(f'😰 Enhanced Assessment: {enhanced_level}')
            else:
                st.error(f'🚨 Enhanced Assessment: {enhanced_level}')
            
            # Immediate Actions Section
            st.markdown('---')
            st.header('🚨 Immediate Actions Required')
            immediate_actions = comprehensive_results['immediate_actions']
            for action in immediate_actions:
                st.markdown(f'• {action}')
            
            # Personalized Solutions Section
            st.markdown('---')
            st.header('💡 Personalized Solutions')
            
            solution_col1, solution_col2 = st.columns(2)
            
            with solution_col1:
                st.subheader('🎯 Customized Recommendations')
                personalized_solutions = comprehensive_results['personalized_solutions']
                for i, solution in enumerate(personalized_solutions[:len(personalized_solutions)//2 + 1]):
                    st.markdown(f'• {solution}')
            
            with solution_col2:
                st.subheader('📚 Course-Specific Strategies')
                course_advice = comprehensive_results['course_specific_advice']
                for advice in course_advice:
                    st.markdown(f'• {advice}')
                
                if len(personalized_solutions) > len(personalized_solutions)//2 + 1:
                    st.subheader('🔄 Additional Recommendations')
                    for solution in personalized_solutions[len(personalized_solutions)//2 + 1:]:
                        st.markdown(f'• {solution}')
            
            # Long-term Strategies
            st.markdown('---')
            st.header('📈 Long-term Mental Health Strategies')
            long_term_strategies = comprehensive_results['long_term_strategies']
            
            # Display in two columns
            strategy_col1, strategy_col2 = st.columns(2)
            mid_point = len(long_term_strategies) // 2
            
            with strategy_col1:
                for strategy in long_term_strategies[:mid_point]:
                    st.markdown(f'• {strategy}')
            
            with strategy_col2:
                for strategy in long_term_strategies[mid_point:]:
                    st.markdown(f'• {strategy}')
            
            # Location-Based Mental Health Facilities
            st.markdown('---')
            st.header(f'🏥 Mental Health Resources in {selected_city}, {selected_state}')
            
            location_facilities = comprehensive_results['location_based_facilities']
            
            # Show fallback note if present
            if 'fallback_note' in location_facilities:
                st.info(f"ℹ️ **Note**: {location_facilities['fallback_note']}")
            
            # Emergency Numbers
            st.subheader('🚨 Emergency Crisis Helplines (24/7)')
            emergency_numbers = location_facilities.get('emergency_numbers', [])
            for emergency in emergency_numbers:
                st.error(f"📞 **{emergency['name']}**: {emergency['number']} - {emergency['description']}")
            
            # Local Facilities
            facility_col1, facility_col2, facility_col3 = st.columns(3)
            
            with facility_col1:
                st.subheader('🏥 Hospitals')
                hospitals = location_facilities.get('hospitals', [])
                if hospitals:
                    for hospital in hospitals[:3]:  # Show first 3
                        with st.expander(f"{hospital['name']} ({hospital['type']})"):
                            st.write(f"📍 {hospital['address']}")
                            st.write(f"📞 {hospital['phone']}")
                            st.write(f"🏥 Services: {', '.join(hospital['services'])}")
                            if hospital.get('emergency'):
                                st.write("🚨 Emergency services available")
                else:
                    st.info(f'No hospital data available for {selected_city}. Please check the state capital or nearby major cities.')
            
            with facility_col2:
                st.subheader('🧠 Counseling Centers')
                counseling_centers = location_facilities.get('counseling_centers', [])
                if counseling_centers:
                    for center in counseling_centers:
                        with st.expander(f"{center['name']}"):
                            st.write(f"📍 {center['address']}")
                            st.write(f"📞 {center['phone']}")
                            st.write(f"💰 Cost: {center['cost']}")
                            st.write(f"🛠️ Services: {', '.join(center['services'])}")
                else:
                    st.info('Contact nearby cities for counseling center information.')
            
            with facility_col3:
                st.subheader('🤝 Support Groups')
                support_groups = location_facilities.get('support_groups', [])
                if support_groups:
                    for group in support_groups:
                        with st.expander(f"{group['name']}"):
                            st.write(f"📧 Contact: {group['contact']}")
                            st.write(f"📅 Meeting: {group['meeting']}")
                else:
                    st.info('Check online for virtual support groups or local community centers.')
            
            # Additional Resources
            st.markdown('---')
            st.header('📚 Additional Mental Health Resources')
            
            resource_col1, resource_col2 = st.columns(2)
            
            with resource_col1:
                st.subheader('📱 Mobile Apps')
                st.markdown("""
                • **Headspace** - Meditation and mindfulness
                • **Calm** - Sleep stories and relaxation
                • **Sanvello** - Anxiety and mood tracking
                • **Youper** - AI emotional health assistant
                """)
                
                st.subheader('🌐 Online Resources')
                st.markdown("""
                • **Mind.org.uk** - Mental health information
                • **Psychology Today** - Find therapists
                • **NAMI.org** - Mental health support
                • **Crisis Text Line** - Text HOME to 741741
                """)
            
            with resource_col2:
                st.subheader('📖 Self-Help Techniques')
                st.markdown("""
                • **Deep Breathing**: 4-7-8 technique
                • **Progressive Muscle Relaxation**
                • **Mindfulness Meditation**: 10 minutes daily
                • **Journaling**: Reflect on thoughts and feelings
                • **Exercise**: 30 minutes daily
                """)
                
                st.subheader('🎓 Student-Specific Resources')
                st.markdown("""
                • Campus counseling centers
                • Student support services
                • Academic advisors
                • Peer support groups
                • Mental health accommodations
                """)
    
    # Crisis disclaimer for critical cases
    if 'comprehensive_results' in locals() and comprehensive_results['enhanced_stress_level'] == 'Awful':
        st.markdown('---')
        st.error('🚨 **CRISIS DISCLAIMER**: This is an automated assessment. If you are having thoughts of self-harm or suicide, please seek immediate professional help or call emergency services. Your life matters and help is available 24/7.')
    elif 'predicted_level' in locals() and predicted_level == 'Awful':
        st.markdown('---')
        st.error('🚨 **CRISIS DISCLAIMER**: This is an automated assessment. If you are having thoughts of self-harm or suicide, please seek immediate professional help or call emergency services. Your life matters and help is available 24/7.')

st.markdown('---')
st.caption('Enhanced Student Stress Prediction System v2.0 | Includes Professional Course Analysis, Emotional State Tracking, and Location-Based Mental Health Resources')
st.caption('⚠️ Disclaimer: This tool is for informational purposes only and should not replace professional medical advice.')
