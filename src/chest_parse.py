from dataclasses import dataclass
from typing import List, Tuple, Dict
import re
import uuid

@dataclass
class ChestItem:
    item_id: str
    display_name: str
    raw_name: str
    god_name: str = ""
    skin_name: str = ""
    collection: str = ""
    number: str = ""
    tier: str = ""
    item_type: str = "skin"
    warnings: List[str] = None

    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []

class ChestParser:
    # Pattern for the new skin format
    SKIN_PATTERN = r'^Skin\s*-\s*([^-]+?)\s*-\s*\[(.*?)\]\s*-\s*([^-]+?)\s*-\s*([^-]+?)\s*-\s*([^\s]+?)\s+([0-9a-f-]+)$'
    
    # Patterns for other item types with UUID at end
    PATTERNS = {
        'music': r'^Music\s*-\s*Pack\s*-\s*([^-]+?)\s*-\s*([^-]+?)\s+([0-9a-f-]+)$',
        'badge': r'^Badge\s*-\s*([^-]+?)\s*-\s*([^-]+?)\s+([0-9a-f-]+)$',
        'global_emote': r'^Global\s*Emote\s*-\s*([^-]+?)\s*-\s*([^-]+?)\s+([0-9a-f-]+)$',
        'jump_stamp': r'^Jump\s*Stamp\s*-\s*([^-]+?)\s*-\s*([^-]+?)\s+([0-9a-f-]+)$',
        'title': r'^Title\s*-\s*([^-]+?)\s*-\s*([^-]+?)\s+([0-9a-f-]+)$',
        'announcer': r'^Announcer\s*Pack\s*-\s*([^-]+?)\s+([0-9a-f-]+)$'
    }

    @staticmethod
    def parse_file(file_path: str) -> Tuple[List[ChestItem], List[str]]:
        """Parse the input file and return a tuple of (items, global_warnings)"""
        items = []
        global_warnings = []
        
        with open(file_path, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                    
                try:
                    item = ChestParser._parse_line(line)
                    items.append(item)
                except ValueError as e:
                    global_warnings.append(f"Line {line_num}: {str(e)}\nLine content: {line}")
                
        return items, global_warnings

    @staticmethod
    def _parse_line(line: str) -> ChestItem:
        """Parse a single line in any supported format."""
        # First try the skin pattern
        match = re.match(ChestParser.SKIN_PATTERN, line)
        if match:
            god_name, skin_name, collection, number, tier, item_id = match.groups()
            
            # Validate UUID format
            try:
                uuid.UUID(item_id)
            except ValueError:
                raise ValueError(f"Invalid UUID format: {item_id}")
                
            warnings = []
            # Check tier format but don't fail
            if not re.match(r'^T[1-5]$', tier):
                warnings.append(f"Non-standard tier format: {tier}")
                
            display_name = f"{god_name.strip()} - {skin_name.strip()}"
            
            return ChestItem(
                item_id=item_id.strip(),
                display_name=display_name,
                raw_name=line,
                god_name=god_name.strip(),
                skin_name=skin_name.strip(),
                collection=collection.strip(),
                number=number.strip(),
                tier=tier.strip(),
                item_type="skin",
                warnings=warnings
            )
            
        # Try other patterns if skin pattern doesn't match
        for item_type, pattern in ChestParser.PATTERNS.items():
            match = re.match(pattern, line)
            if match:
                # Last group is always UUID, rest is name components
                *name_parts, item_id = match.groups()
                
                # Validate UUID format
                try:
                    uuid.UUID(item_id)
                except ValueError:
                    raise ValueError(f"Invalid UUID format: {item_id}")
                
                # Join name parts for display
                display_name = " - ".join(part.strip() for part in name_parts)
                
                return ChestItem(
                    item_id=item_id.strip(),
                    display_name=display_name,
                    raw_name=line,
                    item_type=item_type
                )
                
        raise ValueError("Line does not match any supported format")

    @staticmethod
    def validate_file(file_path: str) -> Tuple[bool, List[str], List[ChestItem]]:
        """
        Validate the item list file format.
        Returns (is_valid, errors, items)
        """
        errors = []
        items = []
        try:
            items, warnings = ChestParser.parse_file(file_path)
            if warnings:
                errors.extend(warnings)
            return len(items) > 0, errors, items
            
        except Exception as e:
            return False, [f"Error reading file: {str(e)}"], []
