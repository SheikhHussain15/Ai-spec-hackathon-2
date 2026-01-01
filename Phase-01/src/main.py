from services import add_task, view_tasks, update_task, mark_task_complete, delete_task
from models import Task
from validation import get_valid_task_id

def display_menu():
    print("\nTodo App Menu:")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Mark Task Complete/Incomplete")
    print("5. Delete Task")
    print("6. Exit")

def main():
    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            description = input("Enter task description: ")
            if description.strip():
                task = add_task(description)
                print(f"Task '{task.description}' (ID: {task.id}) added.")
            else:
                print("Task description cannot be empty.")
        elif choice == '2':
            current_tasks = view_tasks()
            if not current_tasks:
                print("No tasks in the list.")
            else:
                print("\n--- Your Tasks ---")
                for task in current_tasks:
                    status = "✓" if task.completed else " "
                    print(f"[{status}] ID: {task.id}, Description: {task.description}")
                print("------------------")
        elif choice == '3':
            task_id = get_valid_task_id("Enter the ID of the task to update: ")
            new_description = input("Enter the new description: ")
            if new_description.strip():
                updated_task = update_task(task_id, new_description)
                if updated_task:
                    print(f"Task ID {task_id} updated to '{updated_task.description}'.")
                else:
                    print(f"Task with ID {task_id} not found.")
            else:
                print("Task description cannot be empty.")
        elif choice == '4':
            task_id = get_valid_task_id("Enter the ID of the task to mark: ")
            status_choice = input("Mark as (c)omplete or (i)ncomplete? (c/i): ").lower()
            
            if status_choice == 'c':
                marked_task = mark_task_complete(task_id, True)
                if marked_task:
                    print(f"Task ID {task_id} marked as complete.")
                else:
                    print(f"Task with ID {task_id} not found.")
            elif status_choice == 'i':
                marked_task = mark_task_complete(task_id, False)
                if marked_task:
                    print(f"Task ID {task_id} marked as incomplete.")
                else:
                    print(f"Task with ID {task_id} not found.")
            else:
                print("Invalid status choice. Please enter 'c' or 'i'.")
        elif choice == '5':
            task_id = get_valid_task_id("Enter the ID of the task to delete: ")
            deleted_task = delete_task(task_id)
            if deleted_task:
                print(f"Task ID {task_id} ('{deleted_task.description}') deleted.")
            else:
                print(f"Task with ID {task_id} not found.")
        elif choice == '6':
            print("Exiting Todo App. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()