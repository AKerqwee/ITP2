# main.py
# main.py
import sys
from datetime import datetime

# ensure have these imports to access your defined classes and functions
from pomodoro_system.models import PomodoroTimer, HardcoreTimer
from pomodoro_system.storage import ProgressTracker
from pomodoro_system.utils import validate_task_name, chunk_session_reader

def main():
    # initialization of your main classes
    timer = PomodoroTimer(25)
    tracker = ProgressTracker()
    
    while True:
        print("\n=== Smart Pomodoro Timer ===")
        print("1. Start Focus Session")
        print("2. Check Phone Access Status")
        print("3. View History Records (Batch Load)")
        print("4. Exit")
        
        choice = input("Please enter your choice: ").strip()
        
        if choice == "1":
            task_name = input("Enter your focus task name: ").strip()
            
            # run the regex validator in utils
            if not validate_task_name(task_name):
                print("❌ Invalid task name! (Must be 3-20 characters, alphanumeric only)")
                continue
                
            # run the timer logic you defined in models
            timer.start_timer()
            
            # reading and updating JSON file persistence layer
            current_data = tracker.load_data()
            current_data["total_minutes"] += timer.duration
            current_data["sessions"].append({
                "date": datetime.now().strftime("%Y-%m-%d"),
                "duration": timer.duration,
                "name": task_name
            })
            tracker.save_data(current_data)
            
        elif choice == "2":
            # run even/odd hour access validation algorithm
            current_hour = datetime.now().hour
            timer.check_access_rule(current_hour)
            
        elif choice == "3":
            current_data = tracker.load_data()
            sessions = current_data.get("sessions", [])
            if not sessions:
                print("📭 No records found.")
                continue
                
            print("\n--- History Sessions (Batch Loaded) ---")
            # run generator iterator, loading data in batches
            for batch in chunk_session_reader(sessions, size=2):
                for item in batch:
                    print(f"• [{item.get('date')}] Task: {item.get('name')} | Duration: {item.get('duration')} mins")
                cmd = input("Press [Enter] for next batch, or 'q' to return: ").strip()
                if cmd.lower() == 'q':
                    break
                    
        elif choice == "4":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("❌ Invalid option. Please try again.")

if __name__ == "__main__":
    main()