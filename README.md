# 🍅 Smart Pomodoro Focus Management System (ITP2 Final Project)

[cite_start]This is a modular Python-based Pomodoro and phone-access control system built strictly according to the Introduction to Programming 2 final project guidelines[cite: 1, 2].

## 📊 1. Project Planning & Design

### Class Hierarchy 
[cite_start]Our system utilizes Object-Oriented Programming (OOP) to establish complete modular encapsulation and custom behaviors[cite: 15, 16]:
* [cite_start]**`PomodoroTimer` (Base Class / Control Class)**: Manages standard time slot data encapsulation, core countdown controls, and basic access rule algorithms[cite: 68].
* [cite_start]**`HardcoreTimer` (Subclass)**: Inherits from `PomodoroTimer` and overrides the access rules for strict checking, demonstrating **Inheritance and Polymorphism**[cite: 17].
* [cite_start]**`ProgressTracker` (Processing Class)**: Responsible for reliable file I/O operations and handling state data persistence with error handling[cite: 13, 69].

## 🛡️ 2. Quality Assurance & Error Handling
 All core variables utilize snake_case, class structures follow PascalCase, and semantic docstrings accompany all methods.  Robust Exception Handling: Encapsulated standard I/O streams inside try-except blocks within storage.py to seamlessly trap IOError and JSONDecodeError without runtime crashing.  


### Logic Flow 
```text
[User CLI Menu Input]
       │
       ├──► Choice 1: Input Task Name ➔ Regex Validation (`utils.py`)
       │              ➔ Start Timer ➔ Custom Action Logging (Decorator)
       │              ➔ Append Session Object ➔ Save via JSON File I/O
       │
       ├──► Choice 2: Fetch Current Hour ➔ Check Odd/Even Access Rule Validation
       │
       └──► Choice 3: Read Historical Data ➔ Chunk Processing (Generator Mode)

