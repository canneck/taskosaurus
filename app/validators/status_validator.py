import json
from pathlib import Path

class StatusValidator:
    def __init__(self):
        rules_path = Path(__file__).parent.parent / 'config' / 'rules.json'
        with open(rules_path) as f:
            self.rules = json.load(f)['status_rules']
    
    def is_valid_transition(self, current_status, new_status):
        allowed = self.rules['transitions'].get(current_status, [])
        return new_status in allowed