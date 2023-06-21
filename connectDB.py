import mysql.connector
import datetime

class userDB:
    def __init__(self, host, user, password, database):
        self.mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
        self.mycursor = self.mydb.cursor()

    def select_all(self, limit=1000):
        sql = f"""SELECT * FROM `user` LIMIT {limit}"""
        self.mycursor.execute(sql)
        result = self.mycursor.fetchall()
        return result

    def select_one(self, id:int):
        result = {}
        sql = f"""SELECT * FROM `user` WHERE user.id={id}"""
        self.mycursor.execute(sql)
        column = ["id", "username", "password", "email", "firstname", "lastname", "is_business", "business_name", "business_type", "bod", "cash_balance", "cc_balance"]
        row = self.mycursor.fetchone()
    
        for idx, r in enumerate(row[:-1]):
            result[column[idx]] = r
        return result

    def insert(self, username:str, password:str, email:str, firstname:str, lastname:str, birthday:datetime.datetime, is_business=0, business_name="NULL", business_type="NULL"):
        sql = f"INSERT INTO `user` (`username`, `password`, `email`, `firstname`, `lastname`, `is_business`, `business_name`, `business_type`, `birthday`) VALUES ('{username}', '{password}', '{email}', '{firstname}', '{lastname}', {is_business}, '{business_name}', '{business_type}', '{birthday}');"
        self.mycursor.execute(sql)
        self.mydb.commit()
        print("INSERT SUCESSFULLY")
    
    def delete(self, id:int):
        sql = f"DELETE FROM `user` WHERE user.id={id}"
        self.mycursor.execute(sql)
        self.mydb.commit()
        print("DELETE SUCESSFULLY")

    def update(self, id:int, username="", password="", email="", firstname="", lastname="", birthday="", is_business="", business_name="", business_type=""):
        user_selected = self.select(id=id)
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
        
        print(sql)
        self.mycursor.execute(sql)
        self.mydb.commit()
        print("UPDATE SUCESSFULLY")