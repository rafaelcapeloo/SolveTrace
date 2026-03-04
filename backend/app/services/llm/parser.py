"""
LLM response parser — validates and structures the Gemini output.
"""

import json
import re
from typing import Any


def parse_llm_response(raw_response: str) -> dict[str, Any]:
    """
    Parse the LLM's raw text response into a structured dictionary.
    Handles JSON extraction from markdown code blocks, cleaning, and validation.
    """
    # Try to extract JSON from code blocks first
    json_match = re.search(r"```(?:json)?\s*\n?(.*?)\n?\s*```", raw_response, re.DOTALL)
    if json_match:
        json_str = json_match.group(1)
    else:
        # Try parsing the entire response as JSON
        json_str = raw_response.strip()

    # Clean common issues
    json_str = _clean_json_string(json_str)

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        # Last resort: try to find any JSON object in the text
        obj_match = re.search(r"\{[\s\S]*\}", raw_response)
        if obj_match:
            try:
                data = json.loads(_clean_json_string(obj_match.group()))
            except json.JSONDecodeError:
                raise ValueError(f"Failed to parse LLM response as JSON: {e}")
        else:
            raise ValueError(f"No JSON object found in LLM response: {e}")

    # Validate required fields
    return _validate_and_normalize(data)


def _clean_json_string(s: str) -> str:
    """Clean common JSON formatting issues from LLM output."""
    # Remove trailing commas before closing brackets/braces
    s = re.sub(r",\s*([}\]])", r"\1", s)
    # Fix single quotes to double quotes (careful with apostrophes in text)
    # Only do this if no double quotes exist (unlikely for valid JSON)
    return s


def _validate_and_normalize(data: dict) -> dict:
    """Validate the parsed data has required fields and normalize structure."""
    required = ["approach", "complexity", "code_solutions"]
    for field in required:
        if field not in data:
            raise ValueError(f"Missing required field in LLM response: {field}")

    # Ensure approach is a list
    if not isinstance(data["approach"], list):
        data["approach"] = [data["approach"]]

    # Ensure complexity has required subfields
    complexity = data["complexity"]
    for subfield in ["time", "space"]:
        if subfield not in complexity:
            complexity[subfield] = "Unknown"

    # Ensure code_solutions is a dict
    if not isinstance(data["code_solutions"], dict):
        data["code_solutions"] = {"code": str(data["code_solutions"])}

    # Normalize optional fields to correct types
    data.setdefault("key_insights", [])
    data.setdefault("common_pitfalls", [])
    data.setdefault("related_problems", [])
    data.setdefault("diagrams", [])
    data.setdefault("pattern_tags", [])
    data.setdefault("difficulty_assessment", None)
    data.setdefault("interview_tips", [])

    return data
