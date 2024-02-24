from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
import mysql.connector
from pydantic import BaseModel
import hashlib
import os


app = FastAPI()

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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
  password="AccessMe",
  database="semicolons"
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
    mycursor = mydb.cursor(dictionary=True)
    hashed_password = hash_password(password)
    sql = "SELECT * FROM users WHERE mail_id = %s AND password_ = %s"
    val = (email, hashed_password)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    if len(myresult) > 0:
        user = myresult[0]
        del user['password_']
        del user['role']
        del user['created_at']
        return user
    else:
        raise HTTPException(status_code=403, detail="Login error")

@app.post("/upload_image/")
async def upload_image(user_id: str, file: UploadFile = File(...)):
    try:
        mycursor = mydb.cursor()
        contents = await file.read()
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        sql = "INSERT INTO smear_detail (user_id, image) VALUES (%s , %s)"
        val = (user_id, contents, )
        mycursor.execute(sql, val)
        mydb.commit()
        with open(file_path, "wb") as f:
            f.write(contents)        
        return JSONResponse(content={"message": "File uploaded successfully", "file_name": file.filename})
    except Exception as e:
        return JSONResponse(content={"message": "Error occurred", "error": str(e)}, status_code=500)






