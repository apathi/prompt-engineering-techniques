"""
Constraint validation utilities for prompt engineering.

Simple validation mechanisms for format compliance,
content constraints, and structured output verification.
"""

import re
import json
from typing import Dict, Any, List, Optional, Union
import xml.etree.ElementTree as ET


class ConstraintValidator:
    """Simple constraint validator for structured outputs."""
    
    @staticmethod
    def validate_json(text: str, required_fields: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Validate JSON format and optionally check for required fields.
        
        Args:
            text: Text to validate as JSON
            required_fields: Optional list of required field names
            
        Returns:
            Validation result with parsed JSON if valid
        """
        result = {
            "is_valid": False,
            "parsed_json": None,
            "errors": [],
            "missing_fields": []
        }
        
        # Try to parse JSON
        try:
            parsed = json.loads(text.strip())
            result["parsed_json"] = parsed
            result["is_valid"] = True
        except json.JSONDecodeError as e:
            result["errors"].append(f"Invalid JSON format: {str(e)}")
            return result
        
        # Check required fields
        if required_fields and isinstance(parsed, dict):
            for field in required_fields:
                if field not in parsed:
                    result["missing_fields"].append(field)
            
            if result["missing_fields"]:
                result["is_valid"] = False
                result["errors"].append(f"Missing required fields: {result['missing_fields']}")
        
        return result
    
    @staticmethod
    def validate_format_pattern(text: str, pattern: str, description: str = "") -> Dict[str, Any]:
        """
        Validate text against a regex pattern.
        
        Args:
            text: Text to validate
            pattern: Regex pattern to match
            description: Description of the expected format
            
        Returns:
            Validation result
        """
        result = {
            "is_valid": False,
            "matches": [],
            "description": description
        }
        
        try:
            matches = re.findall(pattern, text, re.MULTILINE | re.DOTALL)
            result["matches"] = matches
            result["is_valid"] = len(matches) > 0
            
            if not result["is_valid"]:
                result["error"] = f"Text does not match expected pattern: {description}"
                
        except re.error as e:
            result["error"] = f"Invalid regex pattern: {str(e)}"
        
        return result
    
    @staticmethod
    def validate_structured_format(text: str, format_type: str) -> Dict[str, Any]:
        """
        Validate common structured formats.
        
        Args:
            text: Text to validate
            format_type: Type of format ('bullet_list', 'numbered_list', 'table', 'xml')
            
        Returns:
            Validation result
        """
        validators = {
            'bullet_list': ConstraintValidator._validate_bullet_list,
            'numbered_list': ConstraintValidator._validate_numbered_list,
            'table': ConstraintValidator._validate_table,
            'xml': ConstraintValidator._validate_xml
        }
        
        if format_type not in validators:
            return {
                "is_valid": False,
                "error": f"Unsupported format type: {format_type}. Supported: {list(validators.keys())}"
            }
        
        return validators[format_type](text)
    
    @staticmethod
    def _validate_bullet_list(text: str) -> Dict[str, Any]:
        """Validate bullet list format."""
        lines = text.strip().split('\n')
        bullet_pattern = r'^\s*[-*•]\s+.+'
        valid_lines = [line for line in lines if re.match(bullet_pattern, line)]
        
        return {
            "is_valid": len(valid_lines) > 0,
            "total_lines": len([line for line in lines if line.strip()]),
            "valid_bullet_lines": len(valid_lines),
            "format_compliance": len(valid_lines) / max(len([line for line in lines if line.strip()]), 1)
        }
    
    @staticmethod
    def _validate_numbered_list(text: str) -> Dict[str, Any]:
        """Validate numbered list format."""
        lines = text.strip().split('\n')
        numbered_pattern = r'^\s*\d+\.\s+.+'
        valid_lines = [line for line in lines if re.match(numbered_pattern, line)]
        
        return {
            "is_valid": len(valid_lines) > 0,
            "total_lines": len([line for line in lines if line.strip()]),
            "valid_numbered_lines": len(valid_lines),
            "format_compliance": len(valid_lines) / max(len([line for line in lines if line.strip()]), 1)
        }
    
    @staticmethod
    def _validate_table(text: str) -> Dict[str, Any]:
        """Validate table format (simple pipe-separated)."""
        lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
        
        if not lines:
            return {"is_valid": False, "error": "No content found"}
        
        # Check for pipe-separated format
        pipe_lines = [line for line in lines if '|' in line]
        
        if not pipe_lines:
            return {"is_valid": False, "error": "No pipe-separated table rows found"}
        
        # Check column consistency
        column_counts = [len(line.split('|')) for line in pipe_lines]
        consistent_columns = len(set(column_counts)) == 1
        
        return {
            "is_valid": len(pipe_lines) > 0 and consistent_columns,
            "total_lines": len(lines),
            "table_rows": len(pipe_lines),
            "consistent_columns": consistent_columns,
            "column_counts": column_counts
        }
    
    @staticmethod
    def _validate_xml(text: str) -> Dict[str, Any]:
        """Validate XML format."""
        try:
            ET.fromstring(text.strip())
            return {"is_valid": True, "format": "valid XML"}
        except ET.ParseError as e:
            return {"is_valid": False, "error": f"Invalid XML: {str(e)}"}
    
    @staticmethod
    def validate_content_constraints(text: str, constraints: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate content against various constraints.
        
        Args:
            text: Text to validate
            constraints: Dictionary of constraints to check
                - max_length: Maximum character count
                - min_length: Minimum character count
                - required_keywords: List of required keywords
                - forbidden_words: List of forbidden words
                - max_sentences: Maximum sentence count
                
        Returns:
            Validation result
        """
        result = {
            "is_valid": True,
            "violations": []
        }
        
        text_len = len(text)
        
        # Length constraints
        if "max_length" in constraints and text_len > constraints["max_length"]:
            result["violations"].append(f"Text too long: {text_len} > {constraints['max_length']}")
            result["is_valid"] = False
        
        if "min_length" in constraints and text_len < constraints["min_length"]:
            result["violations"].append(f"Text too short: {text_len} < {constraints['min_length']}")
            result["is_valid"] = False
        
        # Required keywords
        if "required_keywords" in constraints:
            text_lower = text.lower()
            missing_keywords = [kw for kw in constraints["required_keywords"] 
                             if kw.lower() not in text_lower]
            if missing_keywords:
                result["violations"].append(f"Missing required keywords: {missing_keywords}")
                result["is_valid"] = False
        
        # Forbidden words
        if "forbidden_words" in constraints:
            text_lower = text.lower()
            found_forbidden = [word for word in constraints["forbidden_words"] 
                             if word.lower() in text_lower]
            if found_forbidden:
                result["violations"].append(f"Contains forbidden words: {found_forbidden}")
                result["is_valid"] = False
        
        # Sentence count
        if "max_sentences" in constraints:
            sentence_count = len([s for s in text.split('.') if s.strip()])
            if sentence_count > constraints["max_sentences"]:
                result["violations"].append(f"Too many sentences: {sentence_count} > {constraints['max_sentences']}")
                result["is_valid"] = False
        
        return result


def validate_output_format(text: str, expected_format: str, **kwargs) -> Dict[str, Any]:
    """
    Convenience function to validate output format.
    
    Args:
        text: Text to validate
        expected_format: Expected format type
        **kwargs: Additional validation parameters
        
    Returns:
        Validation result
    """
    validator = ConstraintValidator()
    
    if expected_format == "json":
        return validator.validate_json(text, kwargs.get("required_fields"))
    elif expected_format in ["bullet_list", "numbered_list", "table", "xml"]:
        return validator.validate_structured_format(text, expected_format)
    else:
        return {
            "is_valid": False,
            "error": f"Unsupported format type: {expected_format}"
        }


def create_format_prompt_suffix(format_type: str, requirements: Optional[Dict[str, Any]] = None) -> str:
    """
    Create a prompt suffix that specifies format requirements.
    
    Args:
        format_type: Type of format required
        requirements: Optional additional requirements
        
    Returns:
        Formatted prompt suffix
    """
    suffixes = {
        "json": "Format your response as a valid JSON object.",
        "bullet_list": "Format your response as a bullet list using - or • symbols.",
        "numbered_list": "Format your response as a numbered list (1., 2., 3., etc.).",
        "table": "Format your response as a table using pipe (|) separators.",
        "xml": "Format your response as valid XML."
    }
    
    base_suffix = suffixes.get(format_type, f"Format your response as {format_type}.")
    
    if requirements:
        if "required_fields" in requirements and format_type == "json":
            fields = ", ".join(requirements["required_fields"])
            base_suffix += f" Include these required fields: {fields}."
        
        if "max_length" in requirements:
            base_suffix += f" Keep response under {requirements['max_length']} characters."
    
    return base_suffix