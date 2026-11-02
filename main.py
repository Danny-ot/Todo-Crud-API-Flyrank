from fastapi import FastAPI, HTTPException, status

app = FastAPI(title="To-Do List CRUD API")

# In-memory database (temporary list of dictionaries)
tasks_db = [
    {"id": 1, "title": "Buy groceries", "completed": False},
    {"id": 2, "title": "Study FastAPI", "completed": True},
]


@app.get("/tasks")
def get_all_tasks():
    """
    Retrieve all tasks in the list.
    """
    return tasks_db


@app.get("/tasks/{task_id}")
def get_task_by_id(task_id: int):
    """
    Retrieve a single task by its integer ID.
    Raises 404 if the task is not found.
    """
    for task in tasks_db:
        if task["id"] == task_id:
            return task

    # Return standard JSON error message with 404 status code
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with ID {task_id} not found",
    )
