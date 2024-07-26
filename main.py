from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import Base, Task, User

app = FastAPI()

origins = [
    "https://taskmanager.tanishk.me",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

class TaskCreate(BaseModel):
    title: str
    description: str
    userdata: int

class TaskUpdate(BaseModel):
    status: str

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if db_user.password != user.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    return {"id": db_user.id, "username": db_user.username}

@app.post("/api/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/api/tasks/{user_id}")
def read_tasks(user_id: int, db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.userid == user_id).all()
    return tasks

@app.post("/api/tasks/")
async def create_task(title: str = Form(...), description: str = Form(...), userdata: int = Form(...), uploadfile: UploadFile = File(...), db: Session = Depends(get_db)):
    print("Create Task Endpoint Called")
    print(title, description, userdata, uploadfile)
    try:
        contents = await uploadfile.read()
        with open(f"uploads/{uploadfile.filename}", "wb") as f:
            f.write(contents)
        
        db_task = Task(title=title, description=description, userid=userdata, filename=uploadfile.filename)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        
        return db_task
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@app.put("/api/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.status = task.status
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully"}

@app.get("/uploads/{filename}")
def read_upload_file(filename: str):
    return FileResponse(f"uploads/{filename}")