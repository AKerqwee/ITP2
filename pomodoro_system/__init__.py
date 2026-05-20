import re
import functools

def log_action(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"🎬 [LOG] Action triggered: 执行了 '{func.__name__}' 方法")
        return func(*args, **kwargs)
    return wrapper

# according to the requirement: validation function--used to validate user input for task names
def validate_task_name(name: str) -> bool:
    """Validate task name: can only contain letters, numbers, and spaces, length between 3-20 characters"""
    return bool(re.match(r"^[A-Za-z0-9\s]{3,20}$", name))

# according to the requirement: generator function--used to read sessions in chunks

def chunk_session_reader(sessions_list, size=2):
    """every time calling this generator, it will yield the next 'size' number of sessions from the list"""
    for i in range(0, len(sessions_list), size):
        yield sessions_list[i:i + size]