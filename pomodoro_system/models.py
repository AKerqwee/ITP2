from pomodoro_system.utils import log_action

class PomodoroTimer:
    """Core timer logic for focus and access rules"""
    def __init__(self, duration: int = 25):
        self.duration = duration
        self.is_running = False

    @log_action  #decorator
    def start_timer(self):
        """Start the timer session"""
        self.is_running = True
        print(f"⏱️ Timer started. Focusing for {self.duration} minutes.")
        self.is_running = False

    # main function to check if phone is accessible based on the hour
    @log_action  #decorator
    def check_access_rule(self, current_hour: int) -> bool:
        """Check if phone is accessible based on the hour"""
        if current_hour % 2 == 0:
            print(f"📱 Hour {current_hour}: Phone is accessible (Break time).")
            return True
        else:
            print(f"🔒 Hour {current_hour}: Phone locked. Keep focusing!")
            return False

# inheritance example: a stricter timer that only allows phone access after 10 PM
class HardcoreTimer(PomodoroTimer):
    """strict mode: only allows phone access after 10 PM"""
    def check_access_rule(self, current_hour: int) -> bool:
        """polymorphism: override to implement stricter access rules"""
        print("⚠️ Strict mode activated!")
        return current_hour >= 22