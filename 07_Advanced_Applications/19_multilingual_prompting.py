"""
19: Multilingual and Cross-lingual Prompting (LangChain Implementation)

This module demonstrates comprehensive multilingual prompting techniques that work
across languages and cultures, enhanced with cultural adaptation strategies and
global accessibility optimization.

Key concepts:
- Language detection and automatic adaptation
- Cross-lingual consistency validation
- Cultural context preservation and adaptation
- Non-Latin script handling with transliteration
- Global accessibility and inclusive design
- Communication barrier breakdown

"""

import os
import sys
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import re

# Add shared_utils to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared_utils import LangChainClient, setup_logger, OutputManager
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Optional imports with graceful fallbacks
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False


class LanguageScript(Enum):
    """Enumeration of different writing systems."""
    LATIN = "latin"
    CYRILLIC = "cyrillic"
    ARABIC = "arabic"
    CHINESE = "chinese"
    JAPANESE = "japanese"
    HINDI = "hindi"
    TAMIL = "tamil"
    HEBREW = "hebrew"


@dataclass
class LanguageDetection:
    """Results of language detection analysis."""
    detected_language: str
    confidence_score: float
    script_type: LanguageScript
    cultural_context: str


@dataclass
class CrossLingualConsistency:
    """Consistency analysis across languages."""
    source_language: str
    target_language: str
    semantic_similarity: float
    cultural_adaptation_score: float
    message_preservation: float


class LanguageDetector:
    """Advanced language detection and cultural context analyzer."""
    
    def __init__(self):
        self.language_indicators = {
            "english": {"keywords": ["the", "and", "is", "in", "to"], "script": LanguageScript.LATIN},
            "spanish": {"keywords": ["el", "la", "es", "en", "de"], "script": LanguageScript.LATIN},
            "french": {"keywords": ["le", "de", "et", "à", "un"], "script": LanguageScript.LATIN},
            "hindi": {"keywords": ["का", "की", "के", "में", "से"], "script": LanguageScript.HINDI},
            "russian": {"keywords": ["в", "и", "не", "на", "с"], "script": LanguageScript.CYRILLIC},
            "chinese": {"keywords": ["的", "是", "在", "有", "我"], "script": LanguageScript.CHINESE},
            "tamil": {"keywords": ["அது", "இது", "என்", "ஒரு", "மற்றும்"], "script": LanguageScript.TAMIL},
            "arabic": {"keywords": ["في", "من", "إلى", "على", "أن"], "script": LanguageScript.ARABIC}
        }
        
        self.cultural_contexts = {
            "english": "Direct, individualistic communication style",
            "spanish": "Warm, relationship-focused communication",
            "french": "Formal, structured communication with attention to protocol",
            "hindi": "Respectful, hierarchical communication with cultural sensitivity",
            "russian": "Formal, hierarchical communication style",
            "chinese": "Harmony-preserving, context-rich communication",
            "tamil": "Traditional, respectful communication with cultural reverence",
            "arabic": "Elaborate, hospitality-focused communication"
        }
    
    def detect_language(self, text: str) -> LanguageDetection:
        """Detect language and provide cultural context."""
        text_lower = text.lower()
        scores = {}
        
        for language, info in self.language_indicators.items():
            score = sum(1 for keyword in info["keywords"] if keyword in text_lower)
            scores[language] = score
        
        if not scores or max(scores.values()) == 0:
            # Fallback detection based on character patterns
            if re.search(r'[а-яё]', text, re.IGNORECASE):
                detected_lang = "russian"
            elif re.search(r'[一-龯]', text):
                detected_lang = "chinese"
            elif re.search(r'[ऀ-ॿ]', text):
                detected_lang = "hindi"
            elif re.search(r'[஀-௿]', text):
                detected_lang = "tamil"
            elif re.search(r'[؀-ۿ]', text):
                detected_lang = "arabic"
            else:
                detected_lang = "english"
        else:
            detected_lang = max(scores, key=scores.get)
        
        confidence = min(1.0, scores.get(detected_lang, 0) / 5)  # Normalize to 0-1
        script_type = self.language_indicators.get(detected_lang, {}).get("script", LanguageScript.LATIN)
        cultural_context = self.cultural_contexts.get(detected_lang, "Universal communication style")
        
        return LanguageDetection(
            detected_language=detected_lang,
            confidence_score=confidence,
            script_type=script_type,
            cultural_context=cultural_context
        )


class CulturalAdapter:
    """Advanced cultural adaptation engine for global accessibility."""
    
    def __init__(self):
        self.cultural_adaptations = {
            "collectivist": {
                "languages": ["chinese", "hindi", "tamil"],
                "communication_style": "Emphasize group harmony, consensus, and collective benefit",
                "adaptations": [
                    "Use 'we' instead of 'you' when possible",
                    "Emphasize community impact and shared values",
                    "Avoid direct confrontation or criticism",
                    "Include context about group consensus"
                ]
            },
            "individualist": {
                "languages": ["english", "french", "dutch"],
                "communication_style": "Focus on personal choice, individual benefit, and direct communication",
                "adaptations": [
                    "Emphasize personal control and choice",
                    "Highlight individual benefits and outcomes",
                    "Use direct, clear language",
                    "Provide actionable personal steps"
                ]
            },
            "high_context": {
                "languages": ["hindi", "arabic", "chinese", "tamil"],
                "communication_style": "Rich context, implicit meaning, relationship-focused",
                "adaptations": [
                    "Provide extensive background context",
                    "Use respectful, formal language",
                    "Include relationship and hierarchy considerations",
                    "Allow for indirect communication patterns"
                ]
            },
            "low_context": {
                "languages": ["english", "french", "spanish"],
                "communication_style": "Direct, explicit, task-focused communication",
                "adaptations": [
                    "Be explicit and direct",
                    "Focus on facts and logical progression",
                    "Minimize contextual assumptions",
                    "Provide clear, actionable information"
                ]
            }
        }
    
    def get_cultural_adaptations(self, language: str) -> List[str]:
        """Get cultural adaptations for a specific language."""
        adaptations = []
        
        for culture_type, info in self.cultural_adaptations.items():
            if language in info["languages"]:
                adaptations.extend(info["adaptations"])
        
        return adaptations if adaptations else ["Use clear, respectful communication"]


class MultilingualPrompting:
    """Multilingual and Cross-lingual Prompting: Global communication using LangChain."""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        """Initialize with LangChain client and components."""
        self.logger = setup_logger("multilingual_prompting")
        self.client = LangChainClient(
            model=model,
            temperature=0.4,
            max_tokens=500,
            session_name="multilingual_prompting"
        )
        self.llm = self.client.get_llm()
        self.parser = StrOutputParser()
        self.detector = LanguageDetector()
        self.cultural_adapter = CulturalAdapter()
        
        # Initialize sentence transformer if available
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
            except Exception as e:
                self.logger.warning(f"Could not load sentence transformer: {e}")
                self.sentence_model = None
        else:
            self.sentence_model = None
            self.logger.warning("sentence-transformers not available, using fallback similarity")
    
    def language_detection_adaptation(self) -> Dict[str, Any]:
        """
        Demonstrate intermediate language detection with cultural adaptation.
        Shows automatic language identification and culturally-aware responses.
        """
        self.logger.info("Running language detection and adaptation")
        
        # Sample texts in different languages
        multilingual_inputs = [
            {
                "text": "Hello, could you explain how machine learning works?",
                "expected_language": "english"
            },
            {
                "text": "Bonjour, pouvez-vous expliquer comment fonctionne l'apprentissage automatique?",
                "expected_language": "french"
            },
            {
                "text": "Hola, ¿podrías explicar cómo funciona el aprendizaje automático?",
                "expected_language": "spanish"
            },
            {
                "text": "Привет, можете ли вы объяснить, как работает машинное обучение?",
                "expected_language": "russian"
            },
            {
                "text": "नमस्ते, क्या आप मशीन लर्निंग के काम करने के तरीके के बारे में बता सकते हैं?",
                "expected_language": "hindi"
            },
            {
                "text": "வணக்கம், இயந்திர கற்றல் எவ்வாறு செயல்படுகிறது என்பதை விளக்க முடியுமா?",
                "expected_language": "tamil"
            }
        ]
        
        results = []
        
        for input_data in multilingual_inputs:
            # Detect language and cultural context
            detection = self.detector.detect_language(input_data["text"])
            
            # Get cultural adaptations
            cultural_adaptations = self.cultural_adapter.get_cultural_adaptations(detection.detected_language)
            
            # Create culturally-adapted response prompt
            adaptation_instructions = "\n".join([f"- {adaptation}" for adaptation in cultural_adaptations])
            
            prompt = ChatPromptTemplate.from_template(
                """You are a helpful AI assistant that adapts communication style to different cultures.

Language detected: {language}
Cultural context: {cultural_context}
Script type: {script_type}

Cultural adaptations to apply:
{adaptations}

User input: {user_input}

Please respond to the user's question in their language ({language}), incorporating the appropriate cultural communication style. Provide a helpful explanation about machine learning that fits their cultural context."""
            )
            
            chain = prompt | self.llm | self.parser
            response = chain.invoke(
                {
                    "language": detection.detected_language,
                    "cultural_context": detection.cultural_context,
                    "script_type": detection.script_type.value,
                    "adaptations": adaptation_instructions,
                    "user_input": input_data["text"]
                },
                config={"tags": [f"detection_{detection.detected_language}"]}
            )
            
            results.append({
                "input_text": input_data["text"],
                "expected_language": input_data["expected_language"],
                "detection": {
                    "detected_language": detection.detected_language,
                    "confidence": detection.confidence_score,
                    "script_type": detection.script_type.value,
                    "cultural_context": detection.cultural_context
                },
                "cultural_adaptations": cultural_adaptations,
                "response": response,  # Changed from "adapted_response" to "response" for OutputManager compatibility
                "detection_accuracy": detection.detected_language == input_data["expected_language"]
            })
        
        return {
            "technique": "Language Detection and Cultural Adaptation",
            "description": "Automatic language detection with culturally-aware response generation",
            "why_this_works": "Different cultures have distinct communication styles and expectations. By detecting the user's language and applying appropriate cultural adaptations, we can provide more effective, respectful, and accessible communication that resonates with users from diverse backgrounds.",
            "examples": results,
            "overall_accuracy": sum(r["detection_accuracy"] for r in results) / len(results)
        }
    
    def cross_lingual_consistency_optimization(self) -> Dict[str, Any]:
        """
        Demonstrate advanced cross-lingual consistency validation and optimization.
        Shows sophisticated message preservation across languages and cultures.
        """
        self.logger.info("Running cross-lingual consistency optimization")
        
        # Complex scenarios requiring consistent messaging across languages
        consistency_scenarios = [
            {
                "scenario": "Global Product Launch",
                "base_message": "Introducing our revolutionary AI-powered productivity tool that transforms how teams collaborate.",
                "target_languages": ["spanish", "french", "hindi", "tamil"],
                "consistency_requirements": [
                    "Maintain excitement and innovation emphasis",
                    "Preserve technical accuracy",
                    "Adapt to local business culture",
                    "Ensure call-to-action effectiveness"
                ]
            },
            {
                "scenario": "Medical Information Dissemination",
                "base_message": "It's important to consult with a healthcare professional before making any changes to your medication routine.",
                "target_languages": ["spanish", "chinese", "arabic", "tamil"],
                "consistency_requirements": [
                    "Maintain medical accuracy and caution",
                    "Preserve legal disclaimers appropriately",
                    "Adapt to healthcare system contexts",
                    "Respect cultural attitudes toward medical advice"
                ]
            }
        ]
        
        results = []
        
        for scenario in consistency_scenarios:
            scenario_results = {
                "scenario": scenario["scenario"],
                "base_message": scenario["base_message"],
                "translations": [],
                "consistency_analysis": {}
            }
            
            translated_messages = {}
            
            # Generate culturally-adapted translations
            for target_lang in scenario["target_languages"]:
                cultural_adaptations = self.cultural_adapter.get_cultural_adaptations(target_lang)
                requirements_text = "\n".join([f"- {req}" for req in scenario["consistency_requirements"]])
                adaptations_text = "\n".join([f"- {adapt}" for adapt in cultural_adaptations])
                
                translation_prompt = ChatPromptTemplate.from_template(
                    """You are a professional translator specializing in cross-cultural communication.

Task: Translate and culturally adapt the following message for {target_language} speakers.

Original message: {base_message}

Consistency requirements:
{requirements}

Cultural adaptations for {target_language}:
{adaptations}

Instructions:
1. Translate the message accurately to {target_language}
2. Apply appropriate cultural adaptations
3. Maintain the core message and intent
4. Ensure natural, native-speaker quality
5. Preserve any important technical or legal nuances

Culturally-adapted translation:"""
                )
                
                chain = translation_prompt | self.llm | self.parser
                translation = chain.invoke(
                    {
                        "target_language": target_lang,
                        "base_message": scenario["base_message"],
                        "requirements": requirements_text,
                        "adaptations": adaptations_text
                    },
                    config={"tags": [f"translation_{scenario['scenario'].lower().replace(' ', '_')}_{target_lang}"]}
                )
                
                translated_messages[target_lang] = translation
                
                scenario_results["translations"].append({
                    "language": target_lang,
                    "translation": translation,
                    "cultural_adaptations_applied": cultural_adaptations
                })
            
            # Analyze cross-lingual consistency
            consistency_scores = {}
            
            for lang, translation in translated_messages.items():
                # Evaluate consistency (using semantic similarity if available, else heuristic)
                semantic_similarity = self._calculate_semantic_similarity(
                    scenario["base_message"], 
                    translation
                )
                
                cultural_adaptation_score = self._evaluate_cultural_adaptation(lang, translation)
                message_preservation = self._evaluate_message_preservation(scenario["base_message"], translation)
                
                consistency = CrossLingualConsistency(
                    source_language="english",
                    target_language=lang,
                    semantic_similarity=semantic_similarity,
                    cultural_adaptation_score=cultural_adaptation_score,
                    message_preservation=message_preservation
                )
                
                consistency_scores[lang] = {
                    "semantic_similarity": consistency.semantic_similarity,
                    "cultural_adaptation": consistency.cultural_adaptation_score,
                    "message_preservation": consistency.message_preservation,
                    "overall_consistency": (consistency.semantic_similarity + consistency.cultural_adaptation_score + consistency.message_preservation) / 3
                }
            
            scenario_results["consistency_analysis"] = consistency_scores
            
            # Calculate overall scenario consistency
            overall_consistency = sum(scores["overall_consistency"] for scores in consistency_scores.values()) / len(consistency_scores)
            scenario_results["overall_consistency"] = overall_consistency
            
            # Add a response field for OutputManager compatibility
            response_summary = f"Successfully translated base message to {len(translated_messages)} languages:\n"
            for lang, translation in translated_messages.items():
                response_summary += f"- {lang.title()}: {translation[:100]}{'...' if len(translation) > 100 else ''}\n"
            response_summary += f"\nOverall consistency score: {overall_consistency:.3f}"
            
            scenario_results["response"] = response_summary
            
            results.append(scenario_results)
        
        return {
            "technique": "Cross-Lingual Consistency Optimization",
            "description": "Advanced consistency validation and cultural adaptation across multiple languages",
            "why_this_works": "Global communication requires more than literal translation - it demands cultural intelligence. By systematically validating semantic consistency, cultural appropriateness, and message preservation across languages, we ensure that core messages resonate effectively with diverse audiences while respecting cultural nuances and communication preferences.",
            "examples": results
        }
    
    def _calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts."""
        if self.sentence_model:
            try:
                embeddings = self.sentence_model.encode([text1, text2])
                from sklearn.metrics.pairwise import cosine_similarity
                similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
                return float(similarity)
            except Exception as e:
                self.logger.warning(f"Semantic similarity calculation failed: {e}")
        
        # Fallback: simple word overlap similarity
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _evaluate_cultural_adaptation(self, language: str, text: str) -> float:
        """Evaluate how well text is adapted to target culture."""
        adaptations = self.cultural_adapter.get_cultural_adaptations(language)
        text_lower = text.lower()
        
        # Check for adaptation indicators
        adaptation_score = 0.0
        
        if language in ["hindi", "tamil", "chinese"]:
            # High-context cultures - check for respectful, formal language
            respectful_indicators = ["please", "kindly", "respectfully", "honor"]
            adaptation_score += sum(1 for indicator in respectful_indicators if indicator in text_lower) / len(respectful_indicators)
        
        elif language in ["english", "french", "spanish"]:
            # Low-context cultures - check for direct, clear language
            direct_indicators = ["clearly", "directly", "specifically", "exactly"]
            adaptation_score += sum(1 for indicator in direct_indicators if indicator in text_lower) / len(direct_indicators)
        
        # General cultural sensitivity score
        cultural_sensitivity = 0.5  # Base score
        if "culture" in text_lower or "cultural" in text_lower:
            cultural_sensitivity += 0.2
        if "respect" in text_lower or "appropriate" in text_lower:
            cultural_sensitivity += 0.2
        
        return min(1.0, (adaptation_score + cultural_sensitivity) / 2)
    
    def _evaluate_message_preservation(self, original: str, translated: str) -> float:
        """Evaluate how well the core message is preserved."""
        # Extract key concepts from original
        original_words = original.lower().split()
        translated_words = translated.lower().split()
        
        # Look for preservation of key terms (simple heuristic)
        key_terms = [word for word in original_words if len(word) > 5]  # Longer words likely more important
        
        if not key_terms:
            return 0.8  # Default score when no clear key terms
        
        preserved_concepts = 0
        for term in key_terms:
            # Check if concept is preserved (allowing for translation)
            if term in translated.lower() or any(abs(len(term) - len(word)) <= 2 for word in translated_words):
                preserved_concepts += 1
        
        preservation_score = preserved_concepts / len(key_terms)
        
        # Length similarity (should be reasonably similar)
        length_ratio = min(len(translated), len(original)) / max(len(translated), len(original))
        
        return (preservation_score + length_ratio) / 2
    
    def run_all_examples(self) -> Dict[str, Any]:
        """Run all multilingual prompting examples."""
        self.logger.info("Starting Multilingual and Cross-lingual Prompting demonstrations")
        
        results = {
            "technique_overview": "Multilingual and Cross-lingual Prompting",
            "examples": []
        }
        
        # Run all example methods
        examples = [
            self.language_detection_adaptation(),
            self.cross_lingual_consistency_optimization()
        ]
        
        results["examples"] = examples
        
        # Print cost summary
        self.client.print_cost_summary()
        
        return results


def main():
    """Main execution function."""
    # Initialize output manager
    output_manager = OutputManager("19-multilingual-prompting")
    output_manager.add_header("19: MULTILINGUAL AND CROSS-LINGUAL PROMPTING")
    
    # Initialize technique
    multilingual = MultilingualPrompting()
    
    try:
        # Run examples
        results = multilingual.run_all_examples()
        
        # Display results using OutputManager
        output_manager.display_results(results)
        
        # Add cost summary
        output_manager.add_cost_summary(multilingual.client)
        
        # Save to file
        output_manager.save_to_file()
        
    except KeyboardInterrupt:
        output_manager.add_line("\n\nExecution interrupted by user")
        output_manager.save_to_file()
    except Exception as e:
        output_manager.add_line(f"Error: {e}")
        multilingual.logger.error(f"Execution failed: {e}")
        output_manager.save_to_file()


if __name__ == "__main__":
    main()