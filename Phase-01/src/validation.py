def is_valid_task_id(task_id_str: str) -> bool:
    """Checks if a string can be converted to a positive integer."""
    try:
        task_id = int(task_id_str)
        return task_id > 0
    except ValueError:
        return False

def get_valid_task_id(prompt: str) -> int:
    """Prompts the user for a task ID until valid input is received."""
    while True:
        user_input = input(prompt)
        if is_valid_task_id(user_input):
            return int(user_input)
        else:
            print("Invalid input. Please enter a positive number for the task ID.")
