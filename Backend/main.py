from fastapi import FastAPI, HTTPException, Depends
from typing import List
from uuid import uuid4
from sqlalchemy.orm import Session

# İç modüller
from .database.db import get_db, engine, Base
from .models.sql_models import TodoModel
from .schemas.verify import TodoCreate, TodoResponse

# Veritabanı tablosunu oluşturma
Base.metadata.create_all(bind=engine)

app = FastAPI()

# ----Create----
@app.post("/todos", status_code=201, response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = TodoModel(
        id=str(uuid4()),
        title=todo.title,
        description=todo.description,
        completed=todo.completed
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# ----Read----
@app.get("/todos", response_model=List[TodoResponse])
def get_todos(db: Session = Depends(get_db)):
    return db.query(TodoModel).all()

@app.get("/todos/{todo_id}", response_model=TodoResponse)
def read_todo(todo_id: str, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo bulunamadı")
    return todo

# ----Update----
@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: str, todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo bulunamadı")
    
    db_todo.title = todo.title
    db_todo.description = todo.description
    db_todo.completed = todo.completed
    
    db.commit()
    db.refresh(db_todo)
    return db_todo

# ----Delete----
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: str, db: Session = Depends(get_db)):
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo bulunamadı")
    
    db.delete(db_todo)
    db.commit()
    return {"detail": "Todo silindi."} 