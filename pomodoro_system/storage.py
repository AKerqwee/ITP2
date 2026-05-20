import json
import os

class ProgressTracker:
    """Word initialization processing class：responsible for saving and loading progress data, and filtering sessions"""
    def __init__(self, filename="progress.json"):
        self.filename = filename

    def save_data(self, data: dict):
        try:  # using try-except to handle potential file I/O errors gracefully
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"💾 Progress saved to {self.filename}")
        except IOError as e:
            print(f"❌ File write error: {e}")

    def load_data(self) -> dict:
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("⚠️ File corrupted. Initializing empty data.")
        return {"total_minutes": 0, "sessions": []}

    
    def filter_long_sessions(self) -> list:
        data = self.load_data()
        sessions = data.get("sessions", [])
        # using lambda and filter to get sessions with duration >= 25 minutes
        return list(filter(lambda x: x.get("duration", 0) >= 25 if isinstance(x, dict) else False, sessions))
