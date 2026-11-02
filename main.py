from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(title="To-Do List CRUD API")

# In-memory database (temporary list of dictionaries)
tasks_db = [
    {"id": 1, "title": "Buy groceries", "completed": False},
    {"id": 2, "title": "Study FastAPI", "completed": True},
]


# Pydantic model for input validation
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, description="The title of the task")
    completed: Optional[bool] = False


@app.get("/tasks")
def get_all_tasks():
    return tasks_db


@app.get("/tasks/{task_id}")
def get_task_by_id(task_id: int):
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with ID {task_id} not found",
    )


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task_input: TaskCreate):
    new_id = max((task["id"] for task in tasks_db), default=0) + 1
    new_task = {
        "id": new_id,
        "title": task_input.title.strip(),
        "completed": task_input.completed,
    }
    tasks_db.append(new_task)
    return new_task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_input: TaskCreate):
    """
    Update an existing task by its ID.
    Replaces the title and completed status with incoming validated data.
    """
    for task in tasks_db:
        if task["id"] == task_id:
            task["title"] = task_input.title.strip()
            task["completed"] = task_input.completed
            return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with ID {task_id} not found",
    )


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    """
    Delete a task by its ID from our in-memory list.
    Returns status 204 No Content upon successful removal.
    """
    for index, task in enumerate(tasks_db):
        if task["id"] == task_id:
            tasks_db.pop(index)
            return  # 204 responses return no body content

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with ID {task_id} not found",
    )
