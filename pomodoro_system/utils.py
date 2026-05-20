import re
import functools

# 1. decorator 
def log_action(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"🎬 [LOG] Action triggered: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

# 2. validation function
def validate_task_name(name: str) -> bool:
    """Validate task name: can only contain letters, numbers, and spaces, length between 3-20 characters"""
    return bool(re.match(r"^[A-Za-z0-9\s]{3,20}$", name))

# 3. generator function to read sessions in chunks
def chunk_session_reader(sessions_list, size=2):
    for i in range(0, len(sessions_list), size):
        yield sessions_list[i:i + size]