import bcrypt
from fastapi import APIRouter
from database.database import get_connection
from models.users import UserLogin
from models.users import UserRegister

router = APIRouter(prefix="/auth", tags=["auth"])

def hash_password(password: str, salt=12):
    pwd = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(salt))
    return pwd.decode("utf-8")

def verify_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

# se connecter 
@router.post("/login")
def login(user: UserLogin):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT password FROM users WHERE email = ?',
        (user.email,)
    )
    password_hashed = cursor.fetchone()
    
    if verify_password(user.password, password_hashed["password"]):
        return {"message": "connected"}

# création de compte 
@router.post("/register")
def register(user: UserRegister):
    conn = get_connection()
    cursor = conn.cursor()
    password = hash_password(user.password)
    cursor.execute(
        'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
        (user.username, user.email, password)
    )
    conn.commit()
    conn.close()
    return {"message": "user created successfully"}