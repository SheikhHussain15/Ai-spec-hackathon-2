import pytest
from services import add_task, view_tasks, update_task, mark_task_complete, delete_task, _reset_state
from models import Task

@pytest.fixture(autouse=True)
def run_before_each_test():
    """Resets the state before each test."""
    _reset_state()

def test_add_task():
    """Tests that a task can be added."""
    description = "Test task"
    task = add_task(description)
    
    assert task.description == description
    assert task.id == 1
    assert not task.completed
    assert len(view_tasks()) == 1
    assert view_tasks()[0] is task

def test_update_task():
    """Tests that a task can be updated."""
    add_task("Initial task") # ID will be 1
    
    updated_task = update_task(1, "Updated task description")
    
    assert updated_task is not None
    assert updated_task.description == "Updated task description"
    assert view_tasks()[0].description == "Updated task description"

def test_update_non_existent_task():
    """Tests updating a task that does not exist."""
    updated_task = update_task(99, "Non-existent task")
    
    assert updated_task is None

def test_mark_task_complete():
    """Tests that a task can be marked complete."""
    add_task("Task to complete")
    
    completed_task = mark_task_complete(1)
    
    assert completed_task is not None
    assert completed_task.completed is True
    assert view_tasks()[0].completed is True

def test_mark_task_incomplete():
    """Tests that a task can be marked incomplete."""
    task = add_task("Task to complete")
    mark_task_complete(task.id, True) # Mark it complete first
    
    incomplete_task = mark_task_complete(task.id, False)
    
    assert incomplete_task is not None
    assert incomplete_task.completed is False
    assert view_tasks()[0].completed is False

def test_mark_non_existent_task():
    """Tests marking a task that does not exist."""
    marked_task = mark_task_complete(99)
    
    assert marked_task is None

def test_delete_task():
    """Tests that a task can be deleted."""
    add_task("Task to delete 1")
    add_task("Task to delete 2")
    
    deleted_task = delete_task(1)
    
    assert deleted_task is not None
    assert deleted_task.id == 1
    assert len(view_tasks()) == 1
    assert view_tasks()[0].id == 2

def test_delete_non_existent_task():
    """Tests deleting a task that does not exist."""
    add_task("Existing task")
    
    deleted_task = delete_task(99)
    
    assert deleted_task is None
    assert len(view_tasks()) == 1
