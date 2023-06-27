import mysql.connector
import datetime

mydb = mysql.connector.connect(
        host="34.143.137.245",
        user="root",
        password="CoalLa1234",
        database="carboncredit"
    )
print("Connection sucessfully")
class userDB:
    def __init__(self):
        self.mydb = mydb
        self.mycursor = self.mydb.cursor()

    def select_all(self, limit=1000):
        result = {}
        sql = f"""SELECT * FROM `user`"""
        self.mycursor.execute(sql)
        column = ["id", "username", "password", "email", "firstname", "lastname", "is_business", "business_name", "business_type", "bod", "cash_balance", "cc_balance"]
        row = self.mycursor.fetchall()

        for row_i in row:
            for idx, r in enumerate(row_i[:-1]):
                result[row_i[0]] = {column[1]:row_i[1], column[2]:row_i[2], column[3]:row_i[3],
                                    column[4]:row_i[4], column[5]:row_i[5], column[6]:row_i[6],
                                    column[7]:row_i[7], column[8]:row_i[8], column[9]:row_i[9],
                                    column[10]:row_i[10], column[11]:row_i[11],}
        return result

    def select_one(self, id:int):
        result = {}
        sql = f"""SELECT * FROM `user` WHERE user.id={id}"""
        self.mycursor.execute(sql)
        column = ["id", "username", "password", "email", "firstname", "lastname", "is_business", "business_name", "business_type", "bod", "cash_balance", "cc_balance"]
        row = self.mycursor.fetchone()
        if row == None:
            return {"msg" : f"Not found user_id = {id}"}
    
        for idx, r in enumerate(row[:-1]):
            result[column[idx]] = r
        return result

    def insert(self, username:str, password:str, email:str, firstname:str, lastname:str, birthday:datetime.datetime, is_business=0, business_name="NULL", business_type="NULL", created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')):
        sql = f"INSERT INTO `user` (`username`, `password`, `email`, `firstname`, `lastname`, `is_business`, `business_name`, `business_type`, `birthday`, `created_at`) VALUES ('{username}', '{password}', '{email}', '{firstname}', '{lastname}', {is_business}, '{business_name}', '{business_type}', '{birthday}', '{created_at}');"
        self.mycursor.execute(sql)
        self.mydb.commit()
        return {"msg": "INSERT SUCESSFULLY"}
    
    def delete(self, id:int):
        sql = f"DELETE FROM `user` WHERE user.id={id}"
        self.mycursor.execute(sql)
        self.mydb.commit()
        return {"msg": "DELETE SUCESSFULLY"}

    def update(self, id:int, username="", password="", email="", firstname="", lastname="", birthday="", is_business="", business_name="", business_type=""):
        user_selected = self.select_one(id=id)
        if username=="":
            username=user_selected['username']
        if password=="":
            password=user_selected['password']
        if email=="":
            email=user_selected['email']
        if firstname=="":
            firstname=user_selected['firstname']    
        if lastname=="":
            lastname=user_selected['lastname']
        if birthday=="":
            birthday=user_selected['bod']
        if is_business=="":
            is_business=user_selected['is_business']
        if business_name=="":
            business_name=user_selected['business_name']
        if business_type=="":
            business_type=user_selected['business_type']

        sql = f"""UPDATE `user` SET `username`='{username}', `password`='{password}', `email`='{email}', `firstname`='{firstname}', `lastname`='{lastname}', `is_business`='{is_business}', `business_name`='{business_name}', `business_type`='{business_type}', `birthday`='{birthday}'
                WHERE `id`={id};"""

        self.mycursor.execute(sql)
        self.mydb.commit()
        return {"msg": "UPDATE SUCESSFULLY"}

class transactionDB:
    def __init__(self):
        self.mydb = mydb
        self.mycursor = self.mydb.cursor()

    def get_current_cash_cc(self, user_id):
        # Get current cash_balance and cc_balance
        sql_current = f"""SELECT id, cc_balance, cash_balance FROM `user` WHERE id={user_id};"""
        self.mycursor.execute(sql_current)
        row = self.mycursor.fetchone()
        if row == None:
            return {"msg" : f"Not found user_id = {user_id}"}
        result = {"cc_balance": row[1], "cash_balance": row[2]}
        return result

    def transfer(self, user_id, send_id, receive_id, amount:int, status=1):
        if amount<0:
            return {"msg": "amount must more than 0"}
        
        send_current = self.get_current_cash_cc(send_id)
        receive_current = self.get_current_cash_cc(receive_id)

        # transfer cc_balance
        # NOTE!!! cash_balance is not calculate yet
        if float(send_current["cc_balance"])-amount >= 0:
            # Update cash_balance, cc_balance
            sql_send = f"""UPDATE `user` SET `cc_balance`={float(send_current["cc_balance"])-amount} WHERE id={send_id}"""
            sql_receive = f"""UPDATE `user` SET `cc_balance`={float(receive_current["cc_balance"])+amount} WHERE id={receive_id}"""
            self.mycursor.execute(sql_send)
            self.mydb.commit()
            self.mycursor.execute(sql_receive)
            self.mydb.commit()

            # Insert transaction
            sql = f"""INSERT INTO `cc_transaction` (`user_id`, `send_id`, `receive_id`, `amount`, `status`) 
                    VALUES ('{user_id}', '{send_id}', '{receive_id}', '{amount}', '{status}');"""
            self.mycursor.execute(sql)
            self.mydb.commit()
            return {"msg": "Transfering is sucessfully"}
        else:
            return {"msg": "cc_balance is not enough for transfering."}

    def deposit_cash(self, user_id, amount:int, status=1):
        if amount<0:
            return {"msg": "amount must more than 0"}
        user_current = self.get_current_cash_cc(user_id=user_id)

        sql = f"""UPDATE `user` SET cash_balance={user_current["cash_balance"]+amount} WHERE id={user_id}"""
        sql_cash_trasaction = f"""INSERT INTO `cash_transaction` (`user_id`,`amount`) VALUES ({user_id}, {amount})"""
        self.mycursor.execute(sql)
        self.mydb.commit()
        self.mycursor.execute(sql_cash_trasaction)
        self.mydb.commit()
        return {"msg": f"user_id: {user_id} cash balance += {amount} complete"}

    def exchange_cash_cc(self, user_id, amount:int, mode:int, status=1):
        exchange_rate = 100. / 1000.
        user_current = self.get_current_cash_cc(user_id=user_id) 
        cash_current = user_current["cash_balance"]
        cc_current = user_current["cc_balance"]

        if mode == 0: # Cash to CC
            if cash_current - amount < 0:
                return {"msg" : "Your cash is not enough to exchange"}
            sql = f"""UPDATE `user` SET cc_balance={cc_current + (amount/exchange_rate)}, cash_balance={cash_current-amount} WHERE id={user_id}"""
            sql_exchange_transaction = f"""INSERT INTO `exchange_transaction` (`user_id`,`amount`, `mode`) VALUES ({user_id}, {amount}, {mode})"""
            self.mycursor.execute(sql)
            self.mydb.commit()
            self.mycursor.execute(sql_exchange_transaction)
            self.mydb.commit()
            return {"msg" : f"user_id: {user_id} Exchange from {amount} cash to {(amount/exchange_rate)} cc"}
        elif mode == 1: # CC to Cash
            if cc_current - amount < 0:
                return {"msg" : "Your cc is not enough to exchange"}
            sql = f"""UPDATE `user` SET `cash_balance`='{cash_current+ (amount*exchange_rate)}', `cc_balance`='{cc_current-amount}' WHERE `id`={user_id};"""
            print(sql)
            sql_exchange_transaction = f"""INSERT INTO `exchange_transaction` (`user_id`,`amount`, `mode`) VALUES ({user_id}, {amount}, {mode})"""
            self.mycursor.execute(sql)
            self.mydb.commit()
            self.mycursor.execute(sql_exchange_transaction)
            self.mydb.commit()
            return {"msg" : f"user_id: {user_id} Exchange from {amount} cc to {(amount*exchange_rate)} cash"}

class serviceAPI:
    def __init__(self):
        self.mydb = mydb
        self.mycursor = self.mydb.cursor()

    def login(self, username, password):
        result = {}
        sql = f"""SELECT * FROM `user` WHERE (username='{username}' OR email='{username}') AND password='{password}'; """
        self.mycursor.execute(sql)
        column = ["id", "username", "password", "email", "firstname", "lastname", "is_business", "business_name", "business_type", "bod", "cash_balance", "cc_balance"]
        row = self.mycursor.fetchone()
        if row == None:
            return {"msg" : f"Not found username or password"}
        for idx, r in enumerate(row[:-1]):
            result[column[idx]] = r
        return result
    
    def register(self, username:str, password:str, email:str, firstname:str, lastname:str, birthday:datetime.datetime, is_business=0, business_name="NULL", business_type="NULL", created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')):
        # Check username, email or other avoid same value 
        res = userDB().insert(username, password, email, firstname, lastname, birthday, is_business, business_name, business_type, created_at)
        if res["msg"] == "INSERT SUCESSFULLY":
            return {"msg" : "register is successful"}
        
    def transfer_cash_to_cc(self):
        pass
