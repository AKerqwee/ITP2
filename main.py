# main.py
import sys
from datetime import datetime
from pomodoro_system import log_action
from pomodoro_system.models import PomodoroTimer, StrictPomodoroTimer, StudySession
from pomodoro_system.storage import ProgressTracker
from pomodoro_system.utils import validate_task_name

@log_action
def main():
    tracker = ProgressTracker()
    timer = PomodoroTimer(25)  

    while True:  # control loop to keep the program running until user decides to exit
        print("\n=== 🍅 Pomodoro Focus System ===")
        print("1. Start Focus Session")
        print("2. Check Current Phone Access Status")
        print("3. Exit")
        
        choice = input("Select an option: ").strip()
        
        if choice == "1":
            task_name = input("Enter task name: ").strip()
            
            # run validation logic to check if the task name is valid
            if not validate_task_name(task_name):
                print("❌ Invalid task name! (Must be 3-20 chars, alphanumeric only)")
                continue
            
            # run timer logic to start the focus session
            timer.start_timer()
            
            # run entity logic to create a study session record
            session = StudySession(datetime.now().strftime("%Y-%m-%d"), timer.duration, task_name)
            
            # run storage logic to save the session data
            current_data = tracker.load_data()
            current_data["total_minutes"] += timer.duration
            current_data["sessions"].append(session.to_dict())
            tracker.save_data(current_data)
            
        elif choice == "2":
            # run access rule logic to check if phone is accessible based on the current hour
            current_hour = datetime.now().hour
            timer.check_access_rule(current_hour)
            
        elif choice == "3":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()