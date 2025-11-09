import streamlit as st
import pandas as pd
from emotional_analysis import analyze_emotion
from recommendation_engine import get_recommendations

# Set page title and layout
def main():
    st.title('Student Stress Analysis Application')

    # Input for the original dataset
    certifications = st.selectbox('Certifications', ['Yes', 'No'])
    gender = st.selectbox('Gender', ['Male', 'Female', 'Other'])
    department = st.text_input('Department')
    height = st.number_input('Height (cm)', min_value=0)
    weight = st.number_input('Weight (kg)', min_value=0)
    marks_10 = st.number_input('10th Marks (%)', min_value=0, max_value=100)
    marks_12 = st.number_input('12th Marks (%)', min_value=0, max_value=100)
    marks_grad = st.number_input('Graduation Marks (%)', min_value=0, max_value=100)
    hobbies = st.text_input('Hobbies')
    study_time = st.number_input('Study Time (hours/week)', min_value=0)
    preferred_time = st.selectbox('Preferred Study Time', ['Morning', 'Afternoon', 'Evening'])
    sal_expect = st.number_input('Expected Salary', min_value=0)
    like_degree = st.selectbox('Like the Degree?', ['Yes', 'No'])
    career_pursue = st.text_input('Career Pursue')
    watch_time = st.number_input('Watch Time (hours/week)', min_value=0)
    travel_time = st.number_input('Travel Time (minutes/day)', min_value=0)
    money_status = st.selectbox('Money Status', ['Good', 'Average', 'Poor'])
    part_time_job = st.selectbox('Part-time Job', ['Yes', 'No'])

    # Enhanced features
    professional_course = st.selectbox('Professional Course', ['Yes', 'No'])
    current_emotion = st.text_input('Current Emotion')
    trigger_events = st.text_area('Trigger Events')
    personal_context = st.text_area('Personal Context')
    state = st.text_input('State')
    city = st.text_input('City')

    if st.button('Analyze Stress Level'):
        features = pd.DataFrame({
            'certifications': [certifications],
            'gender': [gender],
            'department': [department],
            'height': [height],
            'weight': [weight],
            'marks_10': [marks_10],
            'marks_12': [marks_12],
            'marks_grad': [marks_grad],
            'hobbies': [hobbies],
            'study_time': [study_time],
            'preferred_time': [preferred_time],
            'sal_expect': [sal_expect],
            'like_degree': [like_degree],
            'career_pursue': [career_pursue],
            'watch_time': [watch_time],
            'travel_time': [travel_time],
            'money_status': [money_status],
            'part_time_job': [part_time_job],
            'professional_course': [professional_course],
            'current_emotion': [current_emotion],
            'trigger_events': [trigger_events],
            'personal_context': [personal_context],
            'state': [state],
            'city': [city]
        })

        # Call ML model for prediction
        ml_model_score = predict_stress(features)  # hypothetical ML model function
        emotion_score = analyze_emotion(current_emotion)
        triggers_score = analyze_triggers(trigger_events)

        # Calculate final stress score
        final_stress_score = 0.7 * ml_model_score + 0.1 * professional_course + 0.1 * emotion_score + 0.1 * triggers_score

        st.write(f'Stress Score: {final_stress_score}')

        # Display recommendations based on analysis
        recommendations = get_recommendations(state, city)
        st.write('Recommended Mental Health Resources:')
        for rec in recommendations:
            st.write(f'- {rec}')

if __name__ == '__main__':
    main()