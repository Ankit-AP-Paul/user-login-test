from fastapi import FastAPI, HTTPException
import mysql.connector
from pydantic import BaseModel
import hashlib


app = FastAPI()

class UserRegistration(BaseModel):
    name: str
    role: str
    email: str
    password: str
    age: int
    weight: float
    height: float

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database=""
)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


@app.get("/")
def index():
    return {"message": "FastAPI is working"}

@app.post("/user_registration")
def user_registration(user: UserRegistration):
    mycursor = mydb.cursor()
    sql = "SELECT * FROM users WHERE mail_id = %s"
    val = (user.email,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    if len(myresult) > 0:
        raise HTTPException(status_code=403, detail="Email already exists")
    else:
        hashed_password = hash_password(user.password)
        sql = "INSERT INTO users (username, role, mail_id, password_, age, weight, height) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (user.name, user.role, user.email, hashed_password, user.age, user.weight, user.height)
        mycursor.execute(sql, val)
        mydb.commit()
        return {"userid": user.email, "message": "User Registered"}

@app.post("/user_login")
def user_login(email: str, password: str):
    mycursor = mydb.cursor()
    hashed_password = hash_password(password)
    sql = "SELECT * FROM users WHERE mail_id = %s AND password_ = %s"
    val = (email, hashed_password)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    if len(myresult) > 0:
        return {"message": "User Logged In"}
    else:
        raise HTTPException(status_code=403, detail="Login error")






