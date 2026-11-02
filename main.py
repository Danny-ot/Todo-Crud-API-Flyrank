from fastapi import FastAPI

# Initialize the FastAPI application instance
app = FastAPI(title="To-Do List CRUD API")


@app.get("/")
def read_root():
    """
    Root health check endpoint.
    Returns a simple JSON message to verify the server is running.
    """
    return {"message": "Server is up and running!"}
