from fastapi import APIRouter
from models.users import UserCreate
from database.database import get_connection

router = APIRouter(prefix="/users", tags=["users"])

@router.get("")
def get_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@router.post("/create")
def create_user(user: UserCreate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
        (user.name, user.email, user.password)
    )
    conn.commit()
    conn.close()
    return {"message": "user created successfully"}