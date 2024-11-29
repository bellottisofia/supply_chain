# utils.py

from datetime import datetime, timedelta
import random

class TimeSimulator:
    def __init__(self, start_time=None):
        if start_time:
            self.current_time = start_time
        else:
            self.current_time = datetime.utcnow()

    def advance_time(self, min_hours=1, max_hours=24):
        delta_hours = random.randint(min_hours, max_hours)
        delta = timedelta(hours=delta_hours)
        self.current_time += delta
        return self.current_time

    def get_time_str(self):
        return self.current_time.strftime('%Y-%m-%d %H:%M:%S')