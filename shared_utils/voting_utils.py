"""
Voting utilities for self-consistency in prompt engineering.

Simple voting mechanisms to aggregate multiple reasoning paths
and determine the most consistent answer.
"""

from typing import List, Dict, Any, Tuple
from collections import Counter
import re


def simple_majority_vote(responses: List[str]) -> Dict[str, Any]:
    """
    Perform simple majority voting on a list of responses.
    
    Args:
        responses: List of response strings
        
    Returns:
        Dictionary with voting results and analysis
    """
    if not responses:
        return {"winner": "", "confidence": 0.0, "vote_counts": {}, "analysis": "No responses provided"}
    
    # Simple exact match voting
    vote_counts = Counter(responses)
    most_common = vote_counts.most_common(1)[0]
    winner = most_common[0]
    winner_count = most_common[1]
    
    confidence = winner_count / len(responses)
    
    return {
        "winner": winner,
        "confidence": confidence,
        "vote_counts": dict(vote_counts),
        "total_responses": len(responses),
        "analysis": f"Winner selected with {winner_count}/{len(responses)} votes ({confidence:.1%} confidence)"
    }


def extract_final_answer(response: str) -> str:
    """
    Extract the final answer from a response string.
    Looks for common patterns like "Answer:", "Final answer:", numbers, etc.
    
    Args:
        response: Response string to extract answer from
        
    Returns:
        Extracted final answer
    """
    response = response.strip()
    
    # Look for explicit answer markers
    answer_patterns = [
        r"(?:final answer|answer|conclusion):\s*([^\n.]+)",
        r"(?:therefore|thus|so),?\s*([^\n.]+)",
        r"answer is\s*([^\n.]+)",
        r"result is\s*([^\n.]+)"
    ]
    
    for pattern in answer_patterns:
        match = re.search(pattern, response, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    # Look for numbers (for math problems)
    number_match = re.search(r"(\d+(?:\.\d+)?(?:\s*(?:km/h|mph|hours?|minutes?|seconds?|meters?|km|m))?)", response)
    if number_match:
        return number_match.group(1).strip()
    
    # Fallback: return last sentence
    sentences = response.split('.')
    if sentences:
        return sentences[-1].strip()
    
    return response


def semantic_similarity_vote(responses: List[str]) -> Dict[str, Any]:
    """
    Perform voting based on semantic similarity of extracted answers.
    Groups similar answers together before voting.
    
    Args:
        responses: List of response strings
        
    Returns:
        Dictionary with voting results and analysis
    """
    if not responses:
        return {"winner": "", "confidence": 0.0, "vote_counts": {}, "analysis": "No responses provided"}
    
    # Extract final answers
    answers = [extract_final_answer(response) for response in responses]
    
    # Group similar answers (simple string similarity)
    answer_groups = {}
    for i, answer in enumerate(answers):
        # Find if this answer is similar to any existing group
        matched = False
        for group_key in answer_groups.keys():
            if _are_similar_answers(answer, group_key):
                answer_groups[group_key].append(i)
                matched = True
                break
        
        if not matched:
            answer_groups[answer] = [i]
    
    # Count votes for each group
    vote_counts = {answer: len(indices) for answer, indices in answer_groups.items()}
    
    if not vote_counts:
        return simple_majority_vote(responses)
    
    # Find winner
    winner = max(vote_counts, key=vote_counts.get)
    winner_count = vote_counts[winner]
    confidence = winner_count / len(responses)
    
    return {
        "winner": winner,
        "confidence": confidence,
        "vote_counts": vote_counts,
        "total_responses": len(responses),
        "answer_groups": answer_groups,
        "analysis": f"Semantic winner: '{winner}' with {winner_count}/{len(responses)} votes ({confidence:.1%} confidence)"
    }


def _are_similar_answers(answer1: str, answer2: str) -> bool:
    """
    Check if two answers are semantically similar.
    Simple implementation using string similarity.
    """
    if not answer1 or not answer2:
        return False
    
    # Normalize answers
    a1 = answer1.lower().strip()
    a2 = answer2.lower().strip()
    
    # Exact match
    if a1 == a2:
        return True
    
    # Check if one contains the other (for longer explanations)
    if len(a1) > 5 and len(a2) > 5:
        if a1 in a2 or a2 in a1:
            return True
    
    # Check for similar numerical values
    num1 = re.search(r"(\d+(?:\.\d+)?)", a1)
    num2 = re.search(r"(\d+(?:\.\d+)?)", a2)
    if num1 and num2:
        try:
            val1 = float(num1.group(1))
            val2 = float(num2.group(1))
            if abs(val1 - val2) < 0.1:  # Close numerical values
                return True
        except ValueError:
            pass
    
    return False


def analyze_consistency(responses: List[str]) -> Dict[str, Any]:
    """
    Analyze the consistency of multiple responses.
    
    Args:
        responses: List of response strings
        
    Returns:
        Consistency analysis with metrics
    """
    if len(responses) < 2:
        return {"consistency_score": 1.0, "analysis": "Cannot measure consistency with < 2 responses"}
    
    # Extract answers
    answers = [extract_final_answer(response) for response in responses]
    unique_answers = set(answers)
    
    # Calculate consistency metrics
    consistency_score = 1.0 - (len(unique_answers) - 1) / len(answers)
    most_common_count = Counter(answers).most_common(1)[0][1]
    agreement_ratio = most_common_count / len(answers)
    
    analysis = f"Found {len(unique_answers)} unique answers out of {len(responses)} responses. "
    analysis += f"Consistency score: {consistency_score:.2f}, Agreement ratio: {agreement_ratio:.2f}"
    
    return {
        "consistency_score": consistency_score,
        "agreement_ratio": agreement_ratio,
        "unique_answers": len(unique_answers),
        "total_responses": len(responses),
        "answers": answers,
        "analysis": analysis
    }