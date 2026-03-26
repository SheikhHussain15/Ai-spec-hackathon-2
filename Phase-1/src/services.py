from typing import List, Optional
from models import Task

tasks: List[Task] = []
_next_id = 1 # Changed to private global

def _reset_state(): # Added for testing purposes
    global tasks, _next_id
    tasks = []
    _next_id = 1

def add_task(description: str) -> Task:
    """Adds a new task to the to-do list."""
    global _next_id
    task = Task(id=_next_id, description=description)
    tasks.append(task)
    _next_id += 1
    return task

def view_tasks() -> List[Task]:
    """Returns all tasks in the to-do list."""
    return tasks

def update_task(task_id: int, new_description: str) -> Optional[Task]:
    """Updates the description of an existing task."""
    for task in tasks:
        if task.id == task_id:
            task.description = new_description
            return task
    return None

def mark_task_complete(task_id: int, completed: bool = True) -> Optional[Task]:
    """Marks a task as complete or incomplete."""
    for task in tasks:
        if task.id == task_id:
            task.completed = completed
            return task
    return None

def delete_task(task_id: int) -> Optional[Task]:
    """Deletes a task from the to-do list."""
    global tasks
    for i, task in enumerate(tasks):
        if task.id == task_id:
            return tasks.pop(i)
    return None