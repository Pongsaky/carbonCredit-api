from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from connectDB import userDB
import datetime

app = FastAPI()

mydb = userDB(host="localhost", user="root", password="Pongsakon_123", database="carboncredit")

origins = [
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def main():
    return {"msg": "Hello world"}

@app.get("/user/{id}")
def read_data(id:int):
    return mydb.select(id=id)

@app.post("/user/")
def insert_data(username:str, password:str, email:str, firstname:str, lastname:str, birthday:datetime.datetime, is_business=0, business_name="NULL", business_type="NULL"):
    mydb.insert(username=username, password=password, email=email, firstname=firstname, lastname=lastname, 
                birthday=birthday, is_business=is_business, business_name=business_name, business_type=business_type)
    return {"msg": "Insert sucessfully"}

@app.put("/user/")
def update_data(id:int, username="", password="", email="", firstname="", lastname="", birthday="", is_business="", business_name="", business_type=""):
    mydb.update(id=id, username=username, password=password, email=email, firstname=firstname, lastname=lastname, birthday=birthday, 
                is_business=is_business, business_name=business_name, business_type=business_type)
    return {"msg": "Update sucessfully"}

@app.delete("/user/")
def delete_data(id:int):
    mydb.delete(id=id)
    return {"msg": "Delete sucessfully"}