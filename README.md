# Task Manager (FastAPI + SQLAlchemy ORM)

## Overview

FastAPI application with the following endpoints:
GET /api/tasks: Retrieve all tasks
POST /api/tasks: Create a new task
PUT /api/tasks/{task_id}: Update a task's status
DELETE /api/tasks/{task_id}: Delete a task

SQLAlchemy ORM to create a Task model with the following fields:
id (primary key)
title (string)
description (string)
status (string: "todo", "in_progress", or "done")
created_at (datetime)


## Setup Instructions
## Requirements

- Python (3.8.0)

### Backend (FastAPI)

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/tanishk0297/taskmanagerapi
   cd taskmanagerapi

2. **Install Dependencies:**

   ```bash
   pip install -r requirement.txt
   
2. **Run the FastAPI Server:**

3. ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
   or
   ```bash
   python3 venv venv
   venv\Scripts\activate
   uvicorn main:app --reload
   ```

