# product.py

from datetime import datetime

class Product:
    def __init__(self, product_id, origin, creator, date=None):
        self.product_id = product_id
        self.origin = origin
        self.current_holder = creator
        self.status = "Created"
        self.history = []

        # Record the creation event
        self.history.append({
            'status': self.status,
            'updated_by': creator,
            'date': date or datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        })

    def update_status(self, status, updater, date=None):
        self.status = status
        self.current_holder = updater
        self.history.append({
            'status': status,
            'updated_by': updater,
            'date': date or datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        })

    def get_history(self):
        return self.history