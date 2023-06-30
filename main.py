from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from connectDB import userDB, transactionDB, serviceAPI
from datetime import datetime, timedelta, timezone

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    username : str = "username"
    password : str = "password"
    email : str = "email@gmail.com"
    firstname : str = "firstname"
    lastname : str = "lastname"
    birthday : datetime = datetime.now(tz=timezone(timedelta(hours=7))).strftime('%Y-%m-%d %H:%M:%S')
    is_business : int = 0
    business_name : Union[str, None] = "NULL"
    business_type : Union[str, None] = "NULL"

class Cc_transaction(BaseModel):
    user_id : int
    send_id : int
    receive_id : int
    amount : int

class Cash_transaction(BaseModel):
    user_id : int
    amount : int

class Exchange_transaction(BaseModel):
    user_id : int
    amount : int
    mode : int

class Login(BaseModel):
    username : str
    password : str

@app.get("/")
def main():
    return {"msg": "Hello world"}

@app.get("/user/", tags=["user"])
def read_all_data(limit:int=1000):
    res = userDB().select_all(limit=limit)
    return res

@app.get("/user/{id}", tags=["user"])
def read_data(id:int):
    res = userDB().select_one(id=id)
    return res

@app.post("/user/", tags=["user"])
def insert_data(user : User):
    res = userDB().insert(username=user.username, password=user.password, email=user.email, firstname=user.firstname, lastname=user.lastname, 
                birthday=user.birthday, is_business=user.is_business, business_name=user.business_name, business_type=user.business_type, created_at=datetime.now(tz=timezone(timedelta(hours=7))).strftime('%Y-%m-%d %H:%M:%S'))
    return res

@app.put("/user/{user_id}", tags=["user"])
def update_data(user_id :int, user : User):
    res = userDB().update(id=user_id, username=user.username, password=user.password, email=user.email, firstname=user.firstname, lastname=user.lastname, birthday=user.birthday, 
                is_business=user.is_business, business_name=user.business_name, business_type=user.business_type)
    return res

@app.delete("/user/{user_id}", tags=["user"])
def delete_data(user_id :int):
    res = userDB().delete(id=user_id)
    return res

@app.get("/transaction/", tags=["transaction"])
def welcome_transaction_api():
    return {"msg" : "Welcome to transaction API"}

@app.post("/transaction/transfer/", tags=["transaction"])
def cc_transfer(transaction : Cc_transaction):
    res = transactionDB().transfer(user_id=transaction.user_id, send_id=transaction.send_id, receive_id=transaction.receive_id, amount=transaction.amount)
    return res

@app.post("/transaction/exchange/", tags=["transaction"])
def exchange(transaction : Exchange_transaction):
    """
    mode = 0 -> cash to cc \n
    mode = 1 -> cc to cash 
    """
    res = transactionDB().exchange_cash_cc(user_id=transaction.user_id, amount=transaction.amount, mode=transaction.mode)
    return res

@app.post("/transaction/deposit/", tags=["transaction"])
def deposit_cash(transaction : Cash_transaction):
    res = transactionDB().deposit_cash(user_id=transaction.user_id, amount=transaction.amount)
    return res

@app.get("/service/", tags=["service"])
def welcome_service_api():
    return {"msg" : "Welcome to service API"}

@app.post("/service/login/", tags=["service"])
def login(login : Login):
    res = serviceAPI().login(username=login.username, password=login.password)
    return res

@app.post("/service/register/", tags=["service"])
def register(user : User):
    res = serviceAPI().register(username=user.username, password=user.password, email=user.email, firstname=user.firstname, lastname=user.lastname, 
                birthday=user.birthday, is_business=user.is_business, business_name=user.business_name, business_type=user.business_type, created_at=datetime.now(tz=timezone(timedelta(hours=7))).strftime('%Y-%m-%d %H:%M:%S'))
    return res

@app.post("/service/transer-cash-to-cc/", tags=["service"])
def transfer_cash_to_cc(transaction : Cc_transaction):
    res = transactionDB().transfer(user_id=transaction.user_id, send_id=transaction.send_id, receive_id=transaction.receive_id, amount=transaction.amount)
    return res

@app.get("/service/send-email/", tags=["service"])
def sendEMAIL(password, sender="sender@gmail.com", recipient="recipient@gmail.com", plain_text="Hi,\nThis is a test email.\nHere is the link you wanted:\nhttps://www.python.org", 
                  html_text="""
                    <html>
                      <head></head>
                      <body>
                        <h1>Hello My name is นายพงศกร แก้วใจดี</h1>
                        <p>Hi,<br>
                          This is a test email.<br>
                          Here is the <a href="https://www.python.org">link</a> you wanted.
                        </p>
                      </body>
                    </html>
                  """):
    res = serviceAPI().send_mail(sender=sender, recipient=recipient, password=password, plain_text=plain_text, html_text=html_text)
    return res

class Person(BaseModel):
    name: str
    lastname : str
    tel : Union[str, None] = None

@app.post("/test/")
async def hello_person(person : Person):
    return f"Hello {person.name} {person.lastname} tel: {person.tel} "