from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from src.database import get_session
from src.middleware.auth_middleware import get_current_user
from src.auth.schemas import TokenData
from src.models.task import Task, TaskPublic, TaskCreate, TaskCreateRequest, TaskUpdate, TaskPatchComplete

router = APIRouter(prefix="/users", tags=["tasks"])

# Simplified endpoints that get user_id from token
simple_router = APIRouter(tags=["tasks"])

@simple_router.get("/tasks", response_model=List[TaskPublic])
def get_my_tasks(
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user.
    User ID is extracted from the JWT token.
    """
    # Query tasks for the authenticated user
    tasks = session.exec(
        select(Task).where(Task.user_id == current_user.user_id)
    ).all()

    return tasks

@simple_router.post("/tasks", response_model=TaskPublic)
def create_my_task(
    task_data: TaskCreateRequest,
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.
    User ID is extracted from the JWT token.
    """
    # Create the task with the provided data and associate it with the user
    # We need to add user_id to the data before validation
    task_dict = task_data.model_dump()
    task_dict["user_id"] = current_user.user_id
    task = Task.model_validate(task_dict)

    session.add(task)
    session.commit()
    session.refresh(task)

    return task

@simple_router.get("/tasks/{task_id}", response_model=TaskPublic)
def get_my_task(
    task_id: str,
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task for the authenticated user.
    User ID is extracted from the JWT token.
    """
    # Query for the specific task for the authenticated user
    task = session.exec(
        select(Task).where(Task.id == task_id).where(Task.user_id == current_user.user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task

@simple_router.put("/tasks/{task_id}", response_model=TaskPublic)
def update_my_task(
    task_id: str,
    task_data: TaskUpdate,
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific task for the authenticated user.
    User ID is extracted from the JWT token.
    """
    # Query for the specific task for the authenticated user
    task = session.exec(
        select(Task).where(Task.id == task_id).where(Task.user_id == current_user.user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update the task with the provided data
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    # Update the updated_at timestamp
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task

@simple_router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_task(
    task_id: str,
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task for the authenticated user.
    User ID is extracted from the JWT token.
    """
    # Query for the specific task for the authenticated user
    task = session.exec(
        select(Task).where(Task.id == task_id).where(Task.user_id == current_user.user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    session.delete(task)
    session.commit()

    return

@simple_router.patch("/tasks/{task_id}/toggle", response_model=TaskPublic)
def toggle_task_completion(
    task_id: str,
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a specific task.
    User ID is extracted from the JWT token.
    """
    # Query for the specific task for the authenticated user
    task = session.exec(
        select(Task).where(Task.id == task_id).where(Task.user_id == current_user.user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Toggle the completion status
    task.completed = not task.completed
    # Update the updated_at timestamp
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task

@router.get("/{user_id}/tasks", response_model=List[TaskPublic])
def get_user_tasks(
    user_id: str,
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the specified user.
    The user_id in the path must match the user_id in the JWT token.
    """
    # Verify that the user_id in the path matches the user_id in the token
    if user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user ID mismatch"
        )

    # Query tasks for the authenticated user
    tasks = session.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()

    return tasks

@router.post("/{user_id}/tasks", response_model=TaskPublic)
def create_task(
    user_id: str,
    task_data: TaskCreateRequest,
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the specified user.
    The user_id in the path must match the user_id in the JWT token.
    """
    # Verify that the user_id in the path matches the user_id in the token
    if user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user ID mismatch"
        )

    # Create the task with the provided data and associate it with the user
    task = Task.model_validate(task_data, from_attributes=True)
    task.user_id = user_id

    session.add(task)
    session.commit()
    session.refresh(task)

    return task

@router.get("/{user_id}/tasks/{task_id}", response_model=TaskPublic)
def get_task(
    user_id: str,
    task_id: str,
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task for the specified user.
    The user_id in the path must match the user_id in the JWT token.
    """
    # Verify that the user_id in the path matches the user_id in the token
    if user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user ID mismatch"
        )

    # Query for the specific task for the authenticated user
    task = session.exec(
        select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task

@router.put("/{user_id}/tasks/{task_id}", response_model=TaskPublic)
def update_task(
    user_id: str,
    task_id: str,
    task_data: TaskUpdate,
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific task for the specified user.
    The user_id in the path must match the user_id in the JWT token.
    """
    # Verify that the user_id in the path matches the user_id in the token
    if user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user ID mismatch"
        )

    # Query for the specific task for the authenticated user
    task = session.exec(
        select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update the task with the provided data
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    # Update the updated_at timestamp
    task.updated_at = datetime.utcnow()  # This will set it to current time

    session.add(task)
    session.commit()
    session.refresh(task)

    return task

@router.delete("/{user_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    user_id: str,
    task_id: str,
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task for the specified user.
    The user_id in the path must match the user_id in the token.
    """
    # Verify that the user_id in the path matches the user_id in the token
    if user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user ID mismatch"
        )

    # Query for the specific task for the authenticated user
    task = session.exec(
        select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    session.delete(task)
    session.commit()

    return

@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskPublic)
def update_task_completion(
    user_id: str,
    task_id: str,
    completion_data: TaskPatchComplete,
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update only the completion status of a specific task for the specified user.
    The user_id in the path must match the user_id in the token.
    """
    # Verify that the user_id in the path matches the user_id in the token
    if user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user ID mismatch"
        )

    # Query for the specific task for the authenticated user
    task = session.exec(
        select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update only the completion status
    task.completed = completion_data.completed
    # Update the updated_at timestamp
    task.updated_at = datetime.utcnow()  # This will set it to current time

    session.add(task)
    session.commit()
    session.refresh(task)

    return task