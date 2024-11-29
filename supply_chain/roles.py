# roles.py

class Roles:
    def __init__(self):
        self.roles = {
            'supplier': set(),
            'manufacturer': set(),
            'logistics': set(),
            'retailer': set(),
            'consumer': set()
        }

    def assign_role(self, role, entity):
        if role in self.roles:
            self.roles[role].add(entity)
        else:
            raise ValueError(f"Role {role} does not exist")

    def has_role(self, role, entity):
        return entity in self.roles.get(role, set())