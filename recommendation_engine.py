import json
from typing import Dict, List, Tuple

class RecommendationEngine:
    def __init__(self):
        # Load course stress patterns
        try:
            with open('course_stress_patterns.json', 'r') as f:
                self.course_patterns = json.load(f)
        except:
            self.course_patterns = {}
        
        # Load mental health facilities
        try:
            with open('india_mental_health_facilities.json', 'r') as f:
                self.facilities = json.load(f)
        except:
            self.facilities = {}
    
    def get_course_stress_factor(self, course: str) -> float:
        """Get stress factor for selected professional course"""
        if course in self.course_patterns:
            return self.course_patterns[course].get("base_stress_factor", 0.5)
        return 0.5
    
    def calculate_final_stress_score(
        self, 
        ml_prediction: float,
        course_factor: float,
        emotional_score: float,
        trigger_score: float
    ) -> float:
        """Calculate weighted final stress score"""
        final_score = (
            0.70 * ml_prediction +
            0.10 * course_factor +
            0.10 * emotional_score +
            0.10 * trigger_score
        )
        return min(max(final_score, 0), 1)  # Clamp between 0 and 1
    
    def get_stress_level_category(self, score: float) -> str:
        """Convert stress score to category"""
        if score < 0.3:
            return "Low Stress"
        elif score < 0.5:
            return "Moderate Stress"
        elif score < 0.7:
            return "High Stress"
        else:
            return "Critical Stress"
    
    def generate_personalized_recommendations(
        self,
        stress_score: float,
        course: str,
        emotion: str,
        triggers: List[str],
        context_analysis: Dict,
        state: str,
        city: str
    ) -> Dict[str, List[str]]:
        """Generate comprehensive personalized recommendations"""
        
        recommendations = {
            "immediate_actions": [],
            "course_specific": [],
            "emotional_coping": [],
            "trigger_specific": [],
            "long_term_strategies": [],
            "professional_help": []
        }
        
        # Immediate actions based on stress level
        if stress_score >= 0.7 or context_analysis.get("trauma_indicators", False):
            recommendations["immediate_actions"].extend([
                "🚨 URGENT: Consider speaking with a mental health professional immediately",
                "📞 Contact a crisis helpline (numbers provided below)",
                "👥 Reach out to a trusted friend or family member NOW",
                "⏸️ Take a break from stressful activities today"
            ])
        elif stress_score >= 0.5:
            recommendations["immediate_actions"].extend([
                "🧘 Practice deep breathing exercises for 10 minutes",
                "🚶 Take a 15-minute walk outside",
                "💧 Ensure you're staying hydrated",
                "📱 Limit social media use today"
            ])
        else:
            recommendations["immediate_actions"].extend([
                "✅ Continue your current stress management practices",
                "📝 Maintain a daily gratitude journal",
                "🎯 Set small achievable goals for today"
            ])
        
        # Course-specific recommendations
        if course in self.course_patterns:
            course_data = self.course_patterns[course]
            recommendations["course_specific"].extend(course_data.get("coping_strategies", []))
        
        # Emotional coping strategies
        emotion_strategies = {
            "Anxious": [
                "Practice the 5-4-3-2-1 grounding technique",
                "Try progressive muscle relaxation",
                "Use guided meditation apps like Headspace or Calm"
            ],
            "Depressed": [
                "Maintain a regular sleep schedule",
                "Engage in light physical activity",
                "Consider talking to a counselor"
            ],
            "Overwhelmed": [
                "Break tasks into smaller, manageable steps",
                "Use the Pomodoro technique for studying",
                "Learn to say 'no' to additional commitments"
            ],
            "Stressed": [
                "Practice time management techniques",
                "Create a structured daily routine",
                "Schedule regular breaks"
            ]
        }
        
        if emotion in emotion_strategies:
            recommendations["emotional_coping"].extend(emotion_strategies[emotion])
        
        # Trigger-specific recommendations
        trigger_advice = {
            "Parent scolding": [
                "Practice assertive communication with family",
                "Set healthy boundaries",
                "Consider family counseling if issues persist"
            ],
            "Love failure": [
                "Allow yourself time to grieve",
                "Focus on self-care and personal growth",
                "Reconnect with supportive friends"
            ],
            "Divorce (family)": [
                "Seek trauma-informed counseling",
                "Join support groups for children of divorce",
                "Remember this is not your fault"
            ],
            "Academic failure": [
                "Meet with academic advisors",
                "Form study groups with peers",
                "Consider tutoring services"
            ],
            "Financial problems": [
                "Explore scholarship opportunities",
                "Look into student financial aid",
                "Consider part-time work options"
            ],
            "Bullying": [
                "Report to college authorities immediately",
                "Document incidents",
                "Seek support from anti-bullying resources"
            ]
        }
        
        for trigger in triggers:
            if trigger in trigger_advice:
                recommendations["trigger_specific"].extend(trigger_advice[trigger])
        
        # Long-term strategies
        recommendations["long_term_strategies"].extend([
            "📚 Develop consistent study habits",
            "🏃 Maintain regular physical exercise (30 min daily)",
            "😴 Prioritize 7-8 hours of sleep",
            "🥗 Maintain balanced nutrition",
            "🤝 Build a support network",
            "🎨 Engage in hobbies and creative activities"
        ])
        
        # Professional help - location-based
        if state in self.facilities and city in self.facilities[state]:
            city_facilities = self.facilities[state][city]
            
            recommendations["professional_help"].append(f"\n📍 Mental Health Resources in {city}, {state}:")
            
            # Hospitals
            if "hospitals" in city_facilities:
                recommendations["professional_help"].append("\n🏥 Hospitals & Medical Centers:")
                for hospital in city_facilities["hospitals"][:3]:
                    recommendations["professional_help"].append(
                        f"  • {hospital['name']} - {hospital['type']}\n    📞 {hospital.get('phone', 'N/A')}"
                    )
            
            # Therapy centers
            if "therapy_centers" in city_facilities:
                recommendations["professional_help"].append("\n🧠 Therapy & Counseling Centers:")
                for center in city_facilities["therapy_centers"][:3]:
                    recommendations["professional_help"].append(
                        f"  • {center['name']}\n    📞 {center.get('phone', 'N/A')}"
                    )
            
            # Helplines
            if "helplines" in city_facilities:
                recommendations["professional_help"].append("\n📞 24/7 Crisis Helplines:")
                for helpline in city_facilities["helplines"]:
                    recommendations["professional_help"].append(
                        f"  • {helpline['name']}: {helpline['number']}"
                    )
        
        # National helplines (always included)
        recommendations["professional_help"].extend([
            "\n📞 National Mental Health Helplines:",
            "  • Vandrevala Foundation: 1860-2662-345",
            "  • AASRA: 91-22-27546669",
            "  • iCall: 022-25521111",
            "  • Snehi: 91-22-27546669"
        ])
        
        return recommendations
    
    def get_facility_details(self, state: str, city: str) -> Dict:
        """Get detailed facility information for a location"""
        if state in self.facilities and city in self.facilities[state]:
            return self.facilities[state][city]
        return {}
