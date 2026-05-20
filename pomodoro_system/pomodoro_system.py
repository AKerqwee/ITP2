import json
import os
from datetime import datetime

class PomodoroTimer:
    """Core timer logic for focus and access rules"""
    def __init__(self, duration: int = 25):
        self.duration = duration
        self.is_running = False

    def start_timer(self):
        """Start the timer session"""
        self.is_running = True
        print(f"⏱️ Timer started. Focusing for {self.duration} minutes.")
        # Simulated running phase for the demo
        self.is_running = False

    def check_access_rule(self, current_hour: int) -> bool:
        """Check if phone is accessible based on the hour (every other time slot)"""
        if current_hour % 2 == 0:
            print(f"📱 Hour {current_hour}: Phone is accessible (Break time).")
            return True
        else:
            print(f"🔒 Hour {current_hour}: Phone locked. Keep focusing!")
            return False


class ProgressTracker:
    """Handles saving and loading the user's progress using file I/O"""
    def __init__(self, filename="progress.json"):
        self.filename = filename

    def save_data(self, data: dict):
        """Save session data to a JSON file"""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"💾 Progress saved to {self.filename}")

    def load_data(self) -> dict:
        """Load session data from the JSON file"""
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"total_minutes": 0, "sessions": []}


# Testing the basic modules
if __name__ == "__main__":
    print(">>> Testing Timer Component:")
    timer = PomodoroTimer(25)
    timer.start_timer()
    timer.check_access_rule(14)  # Even hour - should be accessible
    
    print("\n>>> Testing Progress Tracker Component:")
    tracker = ProgressTracker()
    sample_data = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "total_minutes": 25,
        "sessions": ["Programming Assignment 3"]
    }
    tracker.save_data(sample_data)
    print("Loaded Data:", tracker.load_data())