from fastapi import APIRouter
from models.users import UserRegister
from database.database import get_connection

# par rapport à ici : tags permet de mettre un nom à toutes les routes utilisées par le router dans le Swagger 
router = APIRouter(prefix="/users", tags=["users"])

# récupérer la liste de tous les utilisateurs
@router.get("")
def get_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# récupérer un utilisateur par son id
@router.get("/{id}")
def get_user(id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM users WHERE id = ?',
        (id,)
    )
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        return {"message": "user not found"} 
    
    return dict(row)

# créez un utilisateur
@router.post("/create")
def create_user(user: UserRegister):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
        (user.username, user.email, user.password)
    )
    conn.commit()
    conn.close()
    return {"message": "user created successfully"}

# modifier les informations d'un utilisateur
@router.patch("/patch/{id}")
def update_user(id: int, user: UserRegister):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE users SET username = ?, email = ? WHERE id = ?'
    )

# supprimer un utilisateur
@router.delete("/delete/{id}")
def delete_user(id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'DELETE FROM users WHERE id = ?',
        (id,)
    )
    conn.commit()
    conn.close()
    return {"message": "user deleted successfully"}