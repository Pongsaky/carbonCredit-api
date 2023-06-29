from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from connectDB import userDB, transactionDB, serviceAPI
import datetime

app = FastAPI()

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

@app.get("/user/", tags=["user"])
def read_all_data(limit:int=1000):
    res = userDB().select_all(limit=limit)
    return res

@app.get("/user/{id}", tags=["user"])
def read_data(id:int):
    res = userDB().select_one(id=id)
    return res

@app.post("/user/", tags=["user"])
def insert_data(username:str, password:str, email:str, firstname:str, lastname:str, birthday:datetime.datetime, is_business=0, business_name="NULL", business_type="NULL"):
    res = userDB().insert(username=username, password=password, email=email, firstname=firstname, lastname=lastname, 
                birthday=birthday, is_business=is_business, business_name=business_name, business_type=business_type)
    return res


@app.put("/user/", tags=["user"])
def update_data(id:int, username="", password="", email="", firstname="", lastname="", birthday="", is_business="", business_name="", business_type=""):
    res = userDB().update(id=id, username=username, password=password, email=email, firstname=firstname, lastname=lastname, birthday=birthday, 
                is_business=is_business, business_name=business_name, business_type=business_type)
    return res

@app.delete("/user/", tags=["user"])
def delete_data(id:int):
    res = userDB().delete(id=id)
    return res

@app.get("/transaction/", tags=["transaction"])
def welcome_transaction_api():
    return {"msg" : "Welcome to transaction API"}

@app.post("/transaction/transfer/", tags=["transaction"])
def cc_transfer(user_id:int, send_id:int, receive_id:int, amount:int):
    res = transactionDB().transfer(user_id=user_id, send_id=send_id, receive_id=receive_id, amount=amount)
    return res

@app.post("/transaction/exchange/", tags=["transaction"])
def exchange(user_id:int, amount:int, mode:int):
    """
    mode = 0 -> cash to cc \n
    mode = 1 -> cc to cash 
    """
    res = transactionDB().exchange_cash_cc(user_id=user_id, amount=amount, mode=mode)
    return res

@app.post("/transaction/deposit/", tags=["transaction"])
def deposit_cash(user_id:int, amount:int):
    res = transactionDB().deposit_cash(user_id=user_id, amount=amount)
    return res

@app.get("/service/", tags=["service"])
def welcome_service_api():
    return {"msg" : "Welcome to service API"}

@app.post("/service/login/", tags=["service"])
def login(username:str, password:str):
    res = serviceAPI().login(username=username, password=password)
    return res

@app.post("/service/register/", tags=["service"])
def register(username:str, password:str, email:str, firstname:str, lastname:str, birthday:datetime.datetime, is_business=0, business_name="NULL", business_type="NULL", created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')):
    res = serviceAPI().register(username=username, password=password, email=email, firstname=firstname, lastname=lastname,
                                birthday=birthday, is_business=is_business, business_name=business_name, business_type=business_type,
                                created_at=created_at)
    return res

@app.post("/service/transer-cash-to-cc/", tags=["service"])
def transfer_cash_to_cc(user_id, send_id, receive_id, amount:int):
    res = transactionDB().transfer(user_id=user_id, send_id=send_id, receive_id=receive_id, amount=amount)
    return res