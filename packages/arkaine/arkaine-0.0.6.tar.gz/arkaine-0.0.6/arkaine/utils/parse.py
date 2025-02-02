import json
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Type, Union


@dataclass
class SectionConfig:
    """Configuration for a section to be parsed"""

    name: str
    is_json: bool = False
    multiline: bool = True
    required: bool = True
    type: Optional[Type] = str  # Type to convert to
    default: Any = None  # Default value if not found
    multiple: bool = (
        False  # Whether to collect multiple instances of this section
    )


def parse_sections(
    text: str,
    sections: Union[List[str], List[SectionConfig]],
    delimiters: Optional[tuple[str, str]] = None,
) -> Dict[str, Any]:
    """
    Parse sections from text based on headers, handling JSON parsing and
    type conversion.

    Args:
        text: The text to parse
        sections: List of section headers or SectionConfig objects
        delimiters: Optional tuple of (start, end) delimiters

    Returns:
        Dict mapping section names to their content (None if not found)

    Example:
        >>> text = '''
        ... Some intro text
        ... Count: 42
        ... Temperature: 98.6
        ... Items: ["a", "b", "c"]
        ... '''
        >>> sections = [
        ...     SectionConfig("Count", type=int),
        ...     SectionConfig("Temperature", type=float),
        ...     SectionConfig("Items", is_json=True),
        ... ]
        >>> result = parse_sections(text, sections)
        >>> result["Count"]
        42
        >>> result["Temperature"]
        98.6
        >>> result["Items"]
        ['a', 'b', 'c']
    """
    # Convert simple strings to SectionConfig objects
    section_configs = [
        s if isinstance(s, SectionConfig) else SectionConfig(s)
        for s in sections
    ]

    # Initialize results dict with default values
    results = {
        sc.name: [] if sc.multiple else sc.default for sc in section_configs
    }

    # Clean up input text
    text = text.strip()

    # If delimiters specified, extract content between them
    if delimiters:
        start, end = delimiters
        start_idx = text.find(start)
        end_idx = text.rfind(end)
        if start_idx != -1 and end_idx != -1:
            text = text[start_idx + len(start) : end_idx].strip()

    # Split text into lines while preserving empty lines
    lines = text.splitlines()

    current_section = None
    current_content: List[str] = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check if line starts with any section header
        found_section = False
        for config in section_configs:
            # Create pattern that matches "Header:" or "HEADER:" etc
            pattern = rf"^{re.escape(config.name)}:?\s*"
            match = re.match(pattern, line, re.IGNORECASE)

            if match:
                # Save previous section content if any
                if current_section:
                    content = "\n".join(current_content).strip()
                    processed_content = _process_content(
                        content,
                        current_section.is_json,
                        current_section.type,
                    )
                    if current_section.multiple:
                        results[current_section.name].append(processed_content)
                    else:
                        results[current_section.name] = processed_content

                # Start new section
                current_section = config
                current_content = [line[match.end() :]]
                found_section = True
                break

        if not found_section and current_section:
            # If current line doesn't start a new section, append to current
            if current_section.multiline:
                current_content.append(line)

    # Save final section content
    if current_section and current_content:
        content = "\n".join(current_content).strip()
        processed_content = _process_content(
            content,
            current_section.is_json,
            current_section.type,
        )
        if current_section.multiple:
            results[current_section.name].append(processed_content)
        else:
            results[current_section.name] = processed_content

    # Handle required sections
    missing = [
        sc.name
        for sc in section_configs
        if sc.required
        and (results[sc.name] is None or (sc.multiple and not results[sc.name]))
    ]
    if missing:
        # If everything is empty and we have text, assume it's the first
        # required section
        if all(v is None or v == [] for v in results.values()) and text.strip():
            first_missing = next(
                sc for sc in section_configs if sc.name == missing[0]
            )
            results[missing[0]] = _process_content(
                text.strip(),
                first_missing.is_json,
                first_missing.type,
            )
        else:
            missing_str = ", ".join(missing)
            raise ValueError(f"Missing required sections: {missing_str}")

    return results


def _process_content(
    content: str,
    is_json: bool,
    type_: Optional[Type] = None,
) -> Any:
    """Process section content, handling JSON parsing and type conversion"""
    if not content:
        return None

    if is_json:
        try:
            # First try direct JSON parse
            return json.loads(content)
        except json.JSONDecodeError:
            try:
                # Try cleaning up Python literals to JSON
                content = (
                    content.replace("None", "null")
                    .replace("True", "true")
                    .replace("False", "false")
                )
                return json.loads(content)
            except json.JSONDecodeError:
                # If both fail, return as string
                return content

    # If type conversion requested, attempt it
    if type_ is not None and type_ != str:
        try:
            # Handle special case for bool
            if type_ is bool:
                return content.lower() in ("true", "yes", "1", "t", "y")
            # For all other types, use the type constructor
            return type_(content)
        except (ValueError, TypeError):
            # If conversion fails, return original string
            return content

    return content
