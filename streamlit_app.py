import streamlit as st
import json
import numpy as np
from emotional_analysis import EmotionalAnalyzer
from recommendation_engine import RecommendationEngine

# Page configuration
st.set_page_config(
    page_title="Student Stress Analysis System",
    page_icon="🧠",
    layout="wide"
)

# Initialize analyzers
@st.cache_resource
def load_analyzers():
    return EmotionalAnalyzer(), RecommendationEngine()

emotional_analyzer, recommendation_engine = load_analyzers()

# Load state-city data
@st.cache_data
def load_location_data():
    try:
        with open('state_city_data.json', 'r') as f:
            return json.load(f)
    except:
        return {}

state_city_data = load_location_data()

# Title and description
st.title("🧠 Enhanced Student Stress Analysis System")
st.markdown("""
This comprehensive system analyzes your stress levels by considering multiple factors including:
- Your academic course and its typical stress patterns
- Current emotional state and triggering events
- Personal context and circumstances
- Location-based mental health resources
""")

st.divider()

# Create two columns for the main form
col1, col2 = st.columns(2)

with col1:
    st.subheader("📚 Academic Information")
    
    # Professional Course Selection
    professional_course = st.selectbox(
        "Select your Professional Course",
        [
            "Engineering",
            "Medical",
            "Law",
            "Commerce/CA",
            "Arts/Humanities",
            "Science",
            "MBA/Management",
            "Architecture",
            "Other"
        ],
        help="Your field of study affects typical stress patterns"
    )
    
    st.subheader("😊 Emotional State")
    
    # Current Emotion Selection
    current_emotion = st.selectbox(
        "How are you feeling right now?",
        [
            "Calm",
            "Happy",
            "Content",
            "Worried",
            "Anxious",
            "Stressed",
            "Depressed",
            "Overwhelmed",
            "Panic"
        ]
    )
    
    # Trigger Events Selection
    trigger_events = st.multiselect(
        "What events have contributed to your current state? (Select all that apply)",
        [
            "Academic pressure",
            "Exam stress",
            "Parent scolding",
            "Love failure",
            "Relationship issues",
            "Divorce (family)",
            "Financial problems",
            "Health issues",
            "Bullying",
            "Academic failure",
            "Career uncertainty",
            "Social isolation",
            "Family conflict",
            "Loss of loved one",
            "Other"
        ]
    )

with col2:
    st.subheader("📝 Context & Background")
    
    # Context Text Area
    personal_context = st.text_area(
        "Please describe your situation in detail (optional but recommended)",
        height=150,
        placeholder="Share any additional information about your stress, challenges, or specific concerns. This helps us provide more personalized recommendations.",
        help="Your input is confidential and used only to provide better recommendations"
    )
    
    st.subheader("📍 Location (for local resources)")
    
    # State Selection
    selected_state = st.selectbox(
        "Select your State",
        ["Select State"] + sorted(list(state_city_data.keys()))
    )
    
    # City Selection (dynamic based on state)
    if selected_state != "Select State" and selected_state in state_city_data:
        selected_city = st.selectbox(
            "Select your City",
            ["Select City"] + state_city_data[selected_state]
        )
    else:
        selected_city = "Select City"
        st.info("Please select a state first to see available cities")

st.divider()

# Traditional ML Model Inputs (simplified - you'll integrate with your actual model)
st.subheader("📊 Additional Stress Indicators")

col3, col4, col5 = st.columns(3)

with col3:
    sleep_hours = st.slider("Hours of sleep per night", 0, 12, 7)
    study_hours = st.slider("Study hours per day", 0, 16, 6)

with col4:
    social_activities = st.slider("Social activities per week", 0, 20, 5)
    anxiety_level = st.slider("Self-rated anxiety (1-10)", 1, 10, 5)

with col5:
    academic_pressure = st.slider("Academic pressure (1-10)", 1, 10, 5)
    family_support = st.slider("Family support (1-10)", 1, 10, 5)

st.divider()

# Analysis Button
if st.button("🔍 Analyze My Stress Level", type="primary", use_container_width=True):
    
    # Validate inputs
    if selected_state == "Select State" or selected_city == "Select City":
        st.warning("⚠️ Please select both State and City to get location-based recommendations.")
    
    with st.spinner("Analyzing your stress levels..."): 
        
        # Step 1: Get emotional analysis
        emotional_analysis = emotional_analyzer.get_comprehensive_analysis(
            emotion=current_emotion,
            triggers=trigger_events,
            context=personal_context
        )
        
        # Step 2: Get course stress factor
        course_stress_factor = recommendation_engine.get_course_stress_factor(professional_course)
        
        # Step 3: Calculate ML model prediction (simplified - integrate your actual model here)
        # For now, using a weighted average of the input indicators
        ml_prediction = (
            (1 - sleep_hours/12) * 0.2 +
            (study_hours/16) * 0.15 +
            (1 - social_activities/20) * 0.1 +
            (anxiety_level/10) * 0.25 +
            (academic_pressure/10) * 0.2 +
            (1 - family_support/10) * 0.1
        )
        
        # Step 4: Calculate final stress score
        final_stress_score = recommendation_engine.calculate_final_stress_score(
            ml_prediction=ml_prediction,
            course_factor=course_stress_factor,
            emotional_score=emotional_analysis["overall_emotional_stress"],
            trigger_score=emotional_analysis["trigger_score"]
        )
        
        # Step 5: Get stress category
        stress_category = recommendation_engine.get_stress_level_category(final_stress_score)
        
        # Display Results
        st.divider()
        st.header("📊 Analysis Results")
        
        # Stress Score Display
        col_result1, col_result2, col_result3 = st.columns([1, 2, 1])
        
        with col_result2:
            # Color coding based on stress level
            if final_stress_score < 0.3:
                score_color = "green"
            elif final_stress_score < 0.5:
                score_color = "blue"
            elif final_stress_score < 0.7:
                score_color = "orange"
            else:
                score_color = "red"
            
            st.markdown(f"### Overall Stress Level: <span style='color:{score_color}'>{stress_category}</span>", unsafe_allow_html=True)
            st.progress(final_stress_score)
            st.metric("Stress Score", f"{final_stress_score*100:.1f}%")
        
        # Score Breakdown
        st.subheader("📈 Stress Score Breakdown")
        
        breakdown_col1, breakdown_col2, breakdown_col3, breakdown_col4 = st.columns(4)
        
        with breakdown_col1:
            st.metric("ML Model Score", f"{ml_prediction*100:.1f}%.", help="Based on sleep, study hours, etc.")
        
        with breakdown_col2:
            st.metric("Course Stress Factor", f"{course_stress_factor*100:.1f}%", help=f"{professional_course} typical stress level")
        
        with breakdown_col3:
            st.metric("Emotional Stress", f"{emotional_analysis['overall_emotional_stress']*100:.1f}%", help="Based on emotions and triggers")
        
        with breakdown_col4:
            st.metric("Trigger Severity", f"{emotional_analysis['trigger_score']*100:.1f}%", help="Average severity of selected triggers")
        
        # Critical Alert
        if emotional_analysis["requires_immediate_attention"]:
            st.error("🚨 **URGENT ATTENTION REQUIRED**: Your responses indicate you may be in crisis. Please seek immediate help from the resources below.")
        
        # Get Personalized Recommendations
        recommendations = recommendation_engine.generate_personalized_recommendations(
            stress_score=final_stress_score,
            course=professional_course,
            emotion=current_emotion,
            triggers=trigger_events,
            context_analysis=emotional_analysis["context_analysis"],
            state=selected_state if selected_state != "Select State" else "",
            city=selected_city if selected_city != "Select City" else ""
        )
        
        st.divider()
        st.header("💡 Personalized Recommendations")
        
        # Display recommendations in tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🚨 Immediate Actions",
            "📚 Course-Specific",
            "😌 Emotional Coping",
            "🎯 Trigger-Specific",
            "📅 Long-term Strategies",
            "🏥 Professional Help"
        ])
        
        with tab1:
            st.subheader("Immediate Actions to Take")
            for action in recommendations["immediate_actions"]:
                st.markdown(f"- {action}")
        
        with tab2:
            st.subheader(f"Strategies for {professional_course} Students")
            if recommendations["course_specific"]:
                for strategy in recommendations["course_specific"]:
                    st.markdown(f"- {strategy}")
            else:
                st.info("General academic stress management strategies apply")
        
        with tab3:
            st.subheader("Emotional Coping Techniques")
            if recommendations["emotional_coping"]:
                for technique in recommendations["emotional_coping"]:
                    st.markdown(f"- {technique}")
            else:
                st.info("Continue maintaining your current emotional balance")
        
        with tab4:
            st.subheader("Addressing Your Specific Triggers")
            if recommendations["trigger_specific"]:
                for advice in recommendations["trigger_specific"]:
                    st.markdown(f"- {advice}")
            else:
                st.info("No specific trigger-based recommendations at this time")
        
        with tab5:
            st.subheader("Long-term Wellness Strategies")
            for strategy in recommendations["long_term_strategies"]:
                st.markdown(f"- {strategy}")
        
        with tab6:
            st.subheader("Professional Mental Health Resources")
            if recommendations["professional_help"]:
                for resource in recommendations["professional_help"]:
                    st.markdown(resource)
            else:
                st.info("Please select your state and city to see local mental health resources")
                st.markdown("### National Mental Health Helplines:")
                st.markdown("- **Vandrevala Foundation**: 1860-2662-345")
                st.markdown("- **AASRA**: 91-22-27546669")
                st.markdown("- **iCall**: 022-25521111")

# Footer
st.divider()
st.markdown("""
---
**Disclaimer**: This tool provides general guidance and should not replace professional mental health services. 
If you're experiencing a mental health crisis, please contact emergency services or a crisis helpline immediately.

**Privacy**: Your responses are not stored and remain confidential.
""")