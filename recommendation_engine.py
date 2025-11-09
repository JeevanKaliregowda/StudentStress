import json
import re
from typing import Dict, List, Tuple
import pandas as pd

class EmotionalAnalyzer:
    def __init__(self):
        # Emotion weights for stress calculation
        self.emotion_stress_weights = {
            'Very Happy': 0.1,
            'Happy': 0.2,
            'Content': 0.3,
            'Neutral': 0.4,
            'Slightly Stressed': 0.5,
            'Stressed': 0.7,
            'Very Stressed': 0.8,
            'Anxious': 0.8,
            'Depressed': 0.9,
            'Overwhelmed': 0.9,
            'Panicked': 1.0,
            'Hopeless': 1.0
        }
        
        # Trigger event severity weights
        self.trigger_event_weights = {
            'Academic pressure': 0.7,
            'Parent scolding/disappointment': 0.6,
            'Relationship issues/breakup': 0.8,
            'Financial problems': 0.8,
            'Family conflicts': 0.7,
            'Health issues': 0.9,
            'Career uncertainty': 0.7,
            'Social isolation': 0.6,
            'Exam failure': 0.8,
            'Peer pressure': 0.5,
            'Loss of loved one': 1.0,
            'Trauma/abuse': 1.0,
            'None/No specific trigger': 0.2
        }
        
        # Keywords for trauma detection in text
        self.trauma_keywords = [
            'childhood trauma', 'abuse', 'bullying', 'violence', 'assault',
            'neglect', 'divorce', 'death', 'accident', 'harassment',
            'discrimination', 'betrayal', 'abandonment', 'rejection'
        ]
    
    def analyze_emotional_state(self, emotion: str, trigger_events: List[str], context_text: str = "") -> Dict:
        """Analyze emotional state and return stress factors"""
        
        # Get emotion stress score
        emotion_score = self.emotion_stress_weights.get(emotion, 0.5)
        
        # Calculate trigger event score (average if multiple)
        trigger_scores = [self.trigger_event_weights.get(event, 0.5) for event in trigger_events]
        trigger_score = sum(trigger_scores) / len(trigger_scores) if trigger_scores else 0.3
        
        # Analyze context text for trauma indicators
        trauma_detected = self._detect_trauma_in_text(context_text)
        trauma_score = 0.9 if trauma_detected else 0.0
        
        # Sentiment analysis of context text
        sentiment_score = self._analyze_sentiment(context_text)
        
        return {
            'emotion_score': emotion_score,
            'trigger_score': trigger_score,
            'trauma_detected': trauma_detected,
            'trauma_score': trauma_score,
            'sentiment_score': sentiment_score,
            'analysis_summary': {
                'primary_emotion': emotion,
                'trigger_events': trigger_events,
                'trauma_indicators': trauma_detected,
                'context_sentiment': 'negative' if sentiment_score > 0.6 else 'neutral' if sentiment_score > 0.4 else 'positive'
            }
        }
    
    def _detect_trauma_in_text(self, text: str) -> bool:
        """Detect trauma-related keywords in context text"""
        if not text:
            return False
        
        text_lower = text.lower()
        for keyword in self.trauma_keywords:
            if keyword in text_lower:
                return True
        return False
    
    def _analyze_sentiment(self, text: str) -> float:
        """Simple sentiment analysis - returns score between 0 (positive) and 1 (negative)"""
        if not text:
            return 0.5
        
        negative_words = [
            'sad', 'angry', 'frustrated', 'terrible', 'awful', 'hate', 'angry',
            'depressed', 'hopeless', 'worthless', 'failure', 'disappointed',
            'stressed', 'overwhelmed', 'exhausted', 'tired', 'worried', 'scared'
        ]
        
        positive_words = [
            'happy', 'good', 'great', 'excellent', 'wonderful', 'amazing',
            'love', 'excited', 'confident', 'optimistic', 'hopeful', 'peaceful'
        ]
        
        text_lower = text.lower()
        negative_count = sum(1 for word in negative_words if word in text_lower)
        positive_count = sum(1 for word in positive_words if word in text_lower)
        
        total_words = len(text.split())
        if total_words == 0:
            return 0.5
        
        # Calculate sentiment score (higher = more negative)
        sentiment_score = (negative_count - positive_count + total_words * 0.5) / total_words
        return max(0.0, min(1.0, sentiment_score))

class CourseAnalyzer:
    def __init__(self):
        with open('course_stress_patterns.json', 'r') as f:
            self.course_patterns = json.load(f)
    
    def get_course_stress_factor(self, course: str) -> float:
        """Get stress factor for a specific course"""
        return self.course_patterns.get(course, {}).get('base_stress_factor', 0.5)
    
    def get_course_specific_advice(self, course: str, stress_level: str) -> List[str]:
        """Get course-specific coping strategies"""
        course_data = self.course_patterns.get(course, {})
        strategies = course_data.get('coping_strategies', [
            'Develop effective study habits',
            'Seek help from professors and peers',
            'Maintain work-life balance'
        ])
        
        if stress_level in ['Bad', 'Awful']:
            # Add more intensive strategies for high stress
            strategies.extend([
                f'Consider academic counseling for {course} students',
                'Explore stress management workshops specific to your field',
                'Connect with senior students in {course} for guidance'
            ])
        
        return strategies

class LocationBasedRecommendations:
    def __init__(self):
        with open('india_mental_health_facilities.json', 'r') as f:
            self.facilities = json.load(f)
        
        # State capital mapping for fallback
        self.state_capitals = {
            'Andhra Pradesh': 'Amaravati',
            'Arunachal Pradesh': 'Itanagar',
            'Assam': 'Dispur',
            'Bihar': 'Patna',
            'Chhattisgarh': 'Raipur',
            'Goa': 'Panaji',
            'Gujarat': 'Gandhinagar',
            'Haryana': 'Chandigarh',
            'Himachal Pradesh': 'Shimla',
            'Jharkhand': 'Ranchi',
            'Karnataka': 'Bangalore',
            'Kerala': 'Thiruvananthapuram',
            'Madhya Pradesh': 'Bhopal',
            'Maharashtra': 'Mumbai',
            'Manipur': 'Imphal',
            'Meghalaya': 'Shillong',
            'Mizoram': 'Aizawl',
            'Nagaland': 'Kohima',
            'Odisha': 'Bhubaneswar',
            'Punjab': 'Chandigarh',
            'Rajasthan': 'Jaipur',
            'Sikkim': 'Gangtok',
            'Tamil Nadu': 'Chennai',
            'Telangana': 'Hyderabad',
            'Tripura': 'Agartala',
            'Uttar Pradesh': 'Lucknow',
            'Uttarakhand': 'Dehradun',
            'West Bengal': 'Kolkata',
            'Andaman and Nicobar Islands': 'Port Blair',
            'Chandigarh': 'Chandigarh',
            'Dadra and Nagar Haveli and Daman and Diu': 'Daman',
            'Delhi': 'New Delhi',
            'Jammu and Kashmir': 'Srinagar',
            'Ladakh': 'Leh',
            'Lakshadweep': 'Kavaratti',
            'Puducherry': 'Puducherry'
        }
    
    def get_nearby_facilities(self, state: str, city: str) -> Dict:
        """Get mental health facilities near the user's location with state capital fallback"""
        state_data = self.facilities.get(state, {})
        city_data = state_data.get(city, {})
        
        # If exact city not found, try state capital as fallback
        if not city_data and state in self.state_capitals:
            capital_city = self.state_capitals[state]
            city_data = state_data.get(capital_city, {})
            if city_data:
                # Add note about fallback to capital
                fallback_note = f"Mental health facilities from {capital_city} (state capital) as {city} information not available"
                city_data = city_data.copy()  # Don't modify original data
                city_data['fallback_note'] = fallback_note
        
        # If still no data, try to find any available city in the state
        if not city_data:
            available_cities = list(state_data.keys())
            if available_cities:
                fallback_city = available_cities[0]
                city_data = state_data[fallback_city].copy()
                city_data['fallback_note'] = f"Mental health facilities from {fallback_city} (nearest major city with data) as {city} information not available"
        
        # If still no data, provide generic emergency contacts
        if not city_data:
            city_data = {
                'hospitals': [],
                'counseling_centers': [],
                'support_groups': [],
                'fallback_note': f"No specific facility data available for {city}, {state}. Please contact state health department or search online for local mental health services."
            }
        
        # Always include emergency numbers
        emergency_numbers = [
            {
                'name': 'AASRA (24/7 Crisis Helpline)',
                'number': '9820466726',
                'description': 'Suicide prevention and crisis intervention'
            },
            {
                'name': 'Vandrevala Foundation',
                'number': '9999666555',
                'description': '24/7 mental health support'
            },
            {
                'name': 'Sneha India',
                'number': '044-24640050',
                'description': 'Emotional support and suicide prevention'
            },
            {
                'name': 'iCall (TISS)',
                'number': '9152987821',
                'description': 'Psychosocial helpline (Mon-Sat, 8AM-10PM)'
            },
            {
                'name': 'Kiran Mental Health Helpline',
                'number': '1800-599-0019',
                'description': 'Government of India 24/7 mental health support'
            }
        ]
        
        result = {
            'hospitals': city_data.get('hospitals', []),
            'counseling_centers': city_data.get('counseling_centers', []),
            'support_groups': city_data.get('support_groups', []),
            'emergency_numbers': emergency_numbers
        }
        
        # Add fallback note if present
        if 'fallback_note' in city_data:
            result['fallback_note'] = city_data['fallback_note']
        
        return result

class PersonalizedRecommendationEngine:
    def __init__(self):
        self.emotional_analyzer = EmotionalAnalyzer()
        self.course_analyzer = CourseAnalyzer()
        self.location_recommendations = LocationBasedRecommendations()
    
    def generate_comprehensive_recommendations(
        self, 
        ml_prediction: str,
        ml_probabilities: List[float],
        course: str,
        emotion: str,
        trigger_events: List[str],
        context_text: str,
        state: str,
        city: str,
        user_profile: Dict
    ) -> Dict:
        """Generate comprehensive personalized recommendations"""
        
        # Analyze emotional state
        emotional_analysis = self.emotional_analyzer.analyze_emotional_state(
            emotion, trigger_events, context_text
        )
        
        # Get course stress factor
        course_stress_factor = self.course_analyzer.get_course_stress_factor(course)
        
        # Calculate enhanced stress score
        enhanced_stress_score = self._calculate_enhanced_stress_score(
            ml_probabilities, course_stress_factor, emotional_analysis
        )
        
        # Determine final stress level
        final_stress_level = self._determine_stress_level(enhanced_stress_score)
        
        # Generate personalized solutions
        personalized_solutions = self._generate_personalized_solutions(
            final_stress_level, course, emotional_analysis, context_text, user_profile
        )
        
        # Get location-based recommendations
        location_facilities = self.location_recommendations.get_nearby_facilities(state, city)
        
        # Get course-specific advice
        course_advice = self.course_analyzer.get_course_specific_advice(course, final_stress_level)
        
        return {
            'original_ml_prediction': ml_prediction,
            'enhanced_stress_level': final_stress_level,
            'stress_score_breakdown': {
                'ml_model_contribution': 0.70,
                'course_factor_contribution': 0.10,
                'emotional_state_contribution': 0.10,
                'trigger_events_contribution': 0.10,
                'final_score': enhanced_stress_score
            },
            'emotional_analysis': emotional_analysis,
            'personalized_solutions': personalized_solutions,
            'course_specific_advice': course_advice,
            'location_based_facilities': location_facilities,
            'immediate_actions': self._get_immediate_actions(final_stress_level, emotional_analysis),
            'long_term_strategies': self._get_long_term_strategies(final_stress_level, course)
        }
    
    def _calculate_enhanced_stress_score(
        self, 
        ml_probabilities: List[float], 
        course_factor: float, 
        emotional_analysis: Dict
    ) -> float:
        """Calculate the enhanced stress score using weighted factors"""
        
        # Convert ML probabilities to stress score (higher index = higher stress)
        ml_stress_score = sum(i * prob for i, prob in enumerate(ml_probabilities)) / (len(ml_probabilities) - 1)
        
        # Combine all factors
        final_score = (
            0.70 * ml_stress_score +
            0.10 * course_factor +
            0.10 * emotional_analysis['emotion_score'] +
            0.10 * emotional_analysis['trigger_score']
        )
        
        # Add trauma bonus if detected
        if emotional_analysis['trauma_detected']:
            final_score = min(1.0, final_score + 0.1)
        
        return final_score
    
    def _determine_stress_level(self, score: float) -> str:
        """Determine stress level based on enhanced score"""
        if score >= 0.8:
            return 'Awful'
        elif score >= 0.6:
            return 'Bad'
        elif score >= 0.4:
            return 'Good'
        else:
            return 'Fabulous'
    
    def _generate_personalized_solutions(
        self, 
        stress_level: str, 
        course: str, 
        emotional_analysis: Dict, 
        context_text: str,
        user_profile: Dict
    ) -> List[str]:
        """Generate personalized solutions based on all input factors"""
        
        solutions = []
        
        # Base solutions based on stress level
        base_solutions = {
            'Fabulous': [
                'Continue your excellent stress management practices',
                'Consider mentoring peers who might be struggling',
                'Maintain your current healthy routines'
            ],
            'Good': [
                'Implement daily 10-minute mindfulness sessions',
                'Create a structured study schedule',
                'Join study groups for peer support'
            ],
            'Bad': [
                'Seek immediate counseling support',
                'Reduce academic workload if possible',
                'Practice daily stress relief techniques',
                'Connect with campus mental health services'
            ],
            'Awful': [
                'URGENT: Seek immediate professional mental health support',
                'Contact crisis helpline numbers provided',
                'Inform trusted family member or friend about your situation',
                'Consider temporary academic leave if recommended by counselor'
            ]
        }
        
        solutions.extend(base_solutions.get(stress_level, base_solutions['Good']))
        
        # Add emotion-specific solutions
        emotion = emotional_analysis['analysis_summary']['primary_emotion']
        if emotion in ['Anxious', 'Panicked']:
            solutions.extend([
                'Practice deep breathing exercises (4-7-8 technique)',
                'Try progressive muscle relaxation',
                'Limit caffeine intake which can worsen anxiety'
            ])
        elif emotion in ['Depressed', 'Hopeless']:
            solutions.extend([
                'Establish daily sunlight exposure routine',
                'Engage in physical activity, even light walking',
                'Reach out to support network regularly'
            ])
        elif emotion in ['Overwhelmed']:
            solutions.extend([
                'Break large tasks into smaller, manageable steps',
                'Use time-blocking technique for better organization',
                'Practice saying "no" to non-essential commitments'
            ])
        
        # Add trigger-specific solutions
        trigger_events = emotional_analysis['analysis_summary']['trigger_events']
        for trigger in trigger_events:
            if 'Academic pressure' in trigger:
                solutions.append('Discuss academic expectations with professors or academic advisor')
            elif 'Financial problems' in trigger:
                solutions.append('Explore financial aid options and scholarship opportunities')
            elif 'Relationship issues' in trigger:
                solutions.append('Consider relationship counseling or focus on self-care during this transition')
            elif 'Family conflicts' in trigger:
                solutions.append('Practice setting healthy boundaries with family members')
        
        # Add trauma-informed solutions if trauma detected
        if emotional_analysis['trauma_detected']:
            solutions.extend([
                'Consider trauma-informed therapy (EMDR, CBT)',
                'Explore support groups for trauma survivors',
                'Practice grounding techniques during flashbacks or triggers',
                'Create a safety plan with trusted individuals'
            ])
        
        # Add context-specific solutions based on text analysis
        if context_text and len(context_text) > 20:
            context_lower = context_text.lower()
            if 'sleep' in context_lower or 'tired' in context_lower:
                solutions.append('Prioritize sleep hygiene - aim for 7-9 hours nightly')
            if 'study' in context_lower or 'exam' in context_lower:
                solutions.append('Implement active study techniques like spaced repetition')
            if 'friend' in context_lower or 'social' in context_lower:
                solutions.append('Nurture existing friendships and consider joining social activities')
        
        return list(set(solutions))  # Remove duplicates
    
    def _get_immediate_actions(self, stress_level: str, emotional_analysis: Dict) -> List[str]:
        """Get immediate actions based on stress level and emotional state"""
        
        immediate_actions = []
        
        if stress_level == 'Awful':
            immediate_actions = [
                '🚨 Call emergency mental health helpline immediately',
                '🏥 Visit nearest hospital emergency room if having suicidal thoughts',
                '📞 Contact trusted friend or family member to stay with you',
                '💊 Avoid alcohol, drugs, or any impulsive decisions'
            ]
        elif stress_level == 'Bad':
            immediate_actions = [
                '📞 Schedule appointment with counselor within 24-48 hours',
                '🧘 Practice 5-minute breathing exercise right now',
                '💧 Drink water and ensure you\'ve eaten today',
                '📱 Limit social media and news consumption today'
            ]
        elif stress_level == 'Good':
            immediate_actions = [
                '🧘 Take 5 deep breaths and practice mindfulness',
                '🚶 Go for a 10-minute walk outside',
                '📝 Write down three things you\'re grateful for',
                '💬 Reach out to a friend or family member'
            ]
        else:
            immediate_actions = [
                '✨ Celebrate your good mental health',
                '🤝 Consider supporting a friend who might be struggling',
                '📚 Continue your healthy habits',
                '🧘 Practice maintenance mindfulness'
            ]
        
        # Add trauma-specific immediate actions if trauma detected
        if emotional_analysis.get('trauma_detected'):
            immediate_actions.insert(0, '🛡️ Use grounding techniques: 5 things you can see, 4 you can hear, 3 you can touch')
        
        return immediate_actions
    
    def _get_long_term_strategies(self, stress_level: str, course: str) -> List[str]:
        """Get long-term strategies for sustained mental health"""
        
        strategies = [
            'Develop a consistent daily routine',
            'Build a strong support network of friends and mentors',
            'Practice regular physical exercise (30+ minutes, 3x week)',
            'Learn and practice stress management techniques',
            'Maintain healthy sleep schedule (7-9 hours nightly)',
            'Consider regular therapy or counseling sessions',
            'Engage in hobbies and activities outside academics'
        ]
        
        # Add course-specific long-term strategies
        if course == 'Engineering':
            strategies.append('Join technical communities and coding groups for peer support')
        elif course == 'Medical':
            strategies.append('Practice self-care techniques to prevent burnout in healthcare career')
        elif course == 'MBA':
            strategies.append('Develop emotional intelligence and leadership skills')
        
        # Add stress-level specific strategies
        if stress_level in ['Bad', 'Awful']:
            strategies.extend([
                'Regular psychiatric evaluation if recommended',
                'Medication management if prescribed',
                'Intensive therapy sessions (weekly or bi-weekly)',
                'Academic accommodations if needed'
            ])
        
        return strategies