import re
import tkinter as tk
from tkinter import messagebox

def parse_item_list(file_path):
    items = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:  # Skip empty lines
                continue
                
            # Updated pattern to handle both tab and multiple spaces as separators
            pattern = r'^Skin\s*-\s*([^-]+?)\s*-\s*\[(.*?)\]\s*-\s*([^-]+?)\s*-\s*([^-]+?)\s*-\s*([^\s]+?)\s+(.+)$'
            match = re.match(pattern, line)
            
            if match:
                god, skin_name, collection, number, tier, uuid = match.groups()
                items.append({
                    'god': god.strip(),
                    'skin_name': skin_name.strip(),
                    'collection': collection.strip(),
                    'number': number.strip(),
                    'tier': tier.strip(),
                    'uuid': uuid.strip()
                })
            else:
                print(f"Warning: Could not parse line: {line}")
                
    return items

def validate_item_list(file_path):
    """Validates the item list and returns a tuple of (is_valid, error_messages)"""
    if not file_path:
        return False, ["No file selected"]
        
    try:
        items = parse_item_list(file_path)
        if not items:
            return False, ["File is empty or contains no valid items"]
            
        errors = []
        for i, item in enumerate(items, 1):
            # Validate UUID format
            uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
            if not re.match(uuid_pattern, item['uuid'].lower()):
                errors.append(f"Line {i}: Invalid UUID format: {item['uuid']}")
            
            # Validate required fields are not empty
            for field in ['god', 'skin_name', 'collection', 'number', 'tier']:
                if not item[field]:
                    errors.append(f"Line {i}: Missing {field}")
            
            # Validate tier format (T1, T2, T3, T4, T5)
            if not re.match(r'^T[1-5]$', item['tier']):
                errors.append(f"Line {i}: Invalid tier format: {item['tier']}")
        
        return len(errors) == 0, errors
        
    except Exception as e:
        return False, [f"Error reading file: {str(e)}"]

class Screen1(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # ... existing code ...
        
        # Add validate button before the Next button
        validate_button = tk.Button(
            self,
            text="Validate Item List",
            command=self.validate_list
        )
        validate_button.pack(pady=5)
        
        # ... existing Next button and other existing code ...
    
    def validate_list(self):
        file_path = self.controller.item_list_path.get()
        is_valid, errors = validate_item_list(file_path)
        
        if is_valid:
            messagebox.showinfo("Validation Success", "Item list is valid!")
        else:
            error_message = "Validation Failed:\n\n" + "\n".join(errors)
            messagebox.showerror("Validation Error", error_message)

# ... existing code ...