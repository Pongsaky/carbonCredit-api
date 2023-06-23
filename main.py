from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from connectDB import userDB, transactionDB
import datetime

app = FastAPI()

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

@app.get("/user/")
def read_all_data(limit:int=1000):
    res = userDB().select_all(limit=limit)
    return res

@app.get("/user/{id}")
def read_data(id:int):
    res = userDB().select_one(id=id)
    return res

@app.post("/user/")
def insert_data(username:str, password:str, email:str, firstname:str, lastname:str, birthday:datetime.datetime, is_business=0, business_name="NULL", business_type="NULL"):
    res = userDB().insert(username=username, password=password, email=email, firstname=firstname, lastname=lastname, 
                birthday=birthday, is_business=is_business, business_name=business_name, business_type=business_type)
    return res


@app.put("/user/")
def update_data(id:int, username="", password="", email="", firstname="", lastname="", birthday="", is_business="", business_name="", business_type=""):
    res = userDB().update(id=id, username=username, password=password, email=email, firstname=firstname, lastname=lastname, birthday=birthday, 
                is_business=is_business, business_name=business_name, business_type=business_type)
    return res

@app.delete("/user/")
def delete_data(id:int):
    res = userDB().delete(id=id)
    return res

@app.post("/transaction/")
def cc_transfer(user_id:int, send_id:int, receive_id:int, amount:int):
    res = transactionDB().transfer(user_id=user_id, send_id=send_id, receive_id=receive_id, amount=amount)
    return res