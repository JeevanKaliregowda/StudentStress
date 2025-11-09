import json
from typing import Dict, List, Tuple
from textblob import TextBlob

class EmotionalAnalyzer:
    def __init__(self):
        # Emotion to stress score mapping (0-1 scale)
        self.emotion_stress_weights = {
            "Calm": 0.1,
            "Happy": 0.1,
            "Content": 0.2,
            "Worried": 0.5,
            "Anxious": 0.7,
            "Stressed": 0.8,
            "Depressed": 0.9,
            "Overwhelmed": 0.95,
            "Panic": 1.0
        }
        
        # Trigger event severity scores (0-1 scale)
        self.trigger_severity = {
            "Academic pressure": 0.6,
            "Exam stress": 0.7,
            "Parent scolding": 0.5,
            "Love failure": 0.7,
            "Relationship issues": 0.6,
            "Divorce (family)": 0.9,
            "Financial problems": 0.8,
            "Health issues": 0.8,
            "Bullying": 0.85,
            "Academic failure": 0.8,
            "Career uncertainty": 0.7,
            "Social isolation": 0.65,
            "Family conflict": 0.7,
            "Loss of loved one": 0.95,
            "Other": 0.5
        }
    
    def analyze_emotion(self, emotion: str) -> float:
        """Convert selected emotion to stress score"""
        return self.emotion_stress_weights.get(emotion, 0.5)
    
    def analyze_triggers(self, triggers: List[str]) -> float:
        """Calculate average severity of selected trigger events"""
        if not triggers:
            return 0.0
        
        scores = [self.trigger_severity.get(trigger, 0.5) for trigger in triggers]
        return sum(scores) / len(scores)
    
    def analyze_context(self, context_text: str) -> Dict[str, any]:
        """Analyze the text context for sentiment and keywords"""
        if not context_text or len(context_text.strip()) < 10:
            return {
                "sentiment": 0.0,
                "trauma_indicators": False,
                "urgency_level": "low"
            }
        
        # Sentiment analysis
        blob = TextBlob(context_text)
        sentiment = blob.sentiment.polarity
        
        # Check for trauma/crisis indicators
        crisis_keywords = [
            "suicide", "self-harm", "hurt myself", "end it all", 
            "no point", "give up", "can't take it", "trauma",
            "abuse", "violent", "hopeless"
        ]
        
        trauma_indicators = any(keyword in context_text.lower() for keyword in crisis_keywords)
        
        # Determine urgency
        if trauma_indicators or sentiment < -0.5:
            urgency_level = "high"
        elif sentiment < -0.2:
            urgency_level = "medium"
        else:
            urgency_level = "low"
        
        return {
            "sentiment": sentiment,
            "trauma_indicators": trauma_indicators,
            "urgency_level": urgency_level
        }
    
    def get_comprehensive_analysis(self, emotion: str, triggers: List[str], context: str) -> Dict:
        """Get complete emotional analysis"""
        emotion_score = self.analyze_emotion(emotion)
        trigger_score = self.analyze_triggers(triggers)
        context_analysis = self.analyze_context(context)
        
        # Calculate overall emotional stress factor
        emotional_stress_score = (
            0.4 * emotion_score +
            0.4 * trigger_score +
            0.2 * (1 - (context_analysis["sentiment"] + 1) / 2)  # Convert sentiment to stress
        )
        
        return {
            "emotion_score": emotion_score,
            "trigger_score": trigger_score,
            "context_analysis": context_analysis,
            "overall_emotional_stress": emotional_stress_score,
            "requires_immediate_attention": context_analysis["trauma_indicators"]
        }
