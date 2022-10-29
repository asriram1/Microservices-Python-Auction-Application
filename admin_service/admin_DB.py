import mysql.connector
from flask import Flask, render_template, json, request


import jsonify


db = mysql.connector.connect(
host="localhost",
user="root",
password="root",
database= "admin_db"
)


# import sqlalchemy as db

# # specify database configurations
# config = {
#     'host': '127.0.0.1',
#     'port': 3308,
#     'user': 'root',
#     'password': 'root',
#     'database': 'admin_db'
# }
# db_user = config.get('user')
# db_pwd = config.get('password')
# db_host = config.get('host')
# db_port = config.get('port')
# db_name = config.get('database')
# # specify connection string
# connection_str = "mysql+pymysql://root:root@mysql:3308/admin_db"
# # connect to database
# engine = db.create_engine(connection_str)
# connection = engine.connect()
# # pull metadata of a table
# metadata = db.MetaData(bind=engine)
# metadata.reflect(only=['Admin'])

# test_table = metadata.tables['Admin']
# test_table

# myuser = "Admin1"
# myCommand = "SELECT COUNT(*) FROM Admin WHERE Username = "+"'"+myuser+"'"
# mycursor.execute(myCommand)

# for x in mycursor:
#     print(x[0])

#mycursor.execute("CREATE TABLE Admin (Username VARCHAR(50) UNIQUE NOT NULL, Password VARCHAR(50) NOT NULL, AdminID int PRIMARY KEY AUTO_INCREMENT, loggedIn BOOLEAN NOT NULL)")
# mycursor.execute("INSERT INTO Admin (Username, Password) VALUES (%s,%s)", ("Admin2", "Pass2"))
#mycursor.execute("ALTER TABLE Admin ADD COLUMN loggedIn BOOLEAN NOT NULL")
# mycursor.execute("ALTER TABLE Admin ADD UNIQUE (Username)")
# myCommand = "UPDATE Admin SET loggedIn = true WHERE Username = " + "'admin3'"
# mycursor.execute(myCommand)
# db.commit()
# db.commit()
# mycursor.execute("DESCRIBE Admin")


# # db.commit()

# # mycursor.execute("SELECT * FROM Admin")
# for x in mycursor:
#     print(x)
class Admin_DB:

    def __init__(self):
        self.db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database= "admin_db"
        )
        self.mycursor = self.db.cursor()

    def signup(self, username, password):
        loggedIn = 0
        try:
            self.mycursor.execute("INSERT INTO Admin (Username, Password, loggedIn) VALUES (%s,%s,%s)", (username, password, loggedIn))
            self.db.commit()
        except:
            return jsonify({'Error': 'Username already exists!'})
        

    def login(self, username, password):
        try:
            myCommand = "SELECT loggedIn FROM Admin WHERE Username = "+ "'"+username+"'"+" AND Password = "+ "'"+password+"'"
            self.mycursor.execute(myCommand)
        except:
            return jsonify({'Error': 'Incorrect username or password!'})

        for x in self.mycursor:
            loggedIn = x[0]

        if loggedIn ==0:
            try:
                myCommand = "UPDATE Admin SET loggedIn = 1 WHERE Username = "+ "'"+username+"'"+" AND Password = "+ "'"+password+"'"
                self.mycursor.execute(myCommand)
                self.db.commit()
            except:
                return jsonify({'Error': 'Admin already logged in!'})   
        else:
            return jsonify({'Error': 'Admin already logged in!'})     
    def logout(self,username):
        try:
            myCommand = "SELECT loggedIn FROM Admin WHERE Username = "+ "'"+username+ "'"
            self.mycursor.execute(myCommand)
        except:
            return jsonify({'Error': 'Admin does not exist!'})

        for x in self.mycursor:
            loggedIn = x[0]

        if loggedIn ==1:
            myCommand = "UPDATE Admin SET loggedIn = 0 WHERE Username = "+ "'"+username+"'"
            self.mycursor.execute(myCommand)
            self.db.commit()
        else:
            return jsonify({'Error': 'Admin already logged out!'})  
        
    def change_admin_username(self, new_username, old_username):

        try:
            myCommand = "SELECT loggedIn FROM Admin WHERE Username = "+ "'"+old_username+"'"
            self.mycursor.execute(myCommand)
        except:
            return jsonify({'Error': 'Username does not exist!'})
    
        for x in self.mycursor:
            loggedIn = x[0]
    
        if loggedIn ==0 or loggedIn ==1:
            myCommand = "UPDATE Admin SET Username = "+ "'" + new_username +"'"+" WHERE Username = "+ "'"+old_username+"'"
            self.mycursor.execute(myCommand)
            self.db.commit()
        else:
            return jsonify({'Error': 'Admin needs to log in before changing username!'})

def main():
    Admin_Db = Admin_DB()
    #Admin_Db.change_admin_username('fourth_admin', 'third_admin')

    # Admin1 = Admin("anotherAdmin", "pass")
    # Admin1.login()    


if __name__ == "__main__":
    main()