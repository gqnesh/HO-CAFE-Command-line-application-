from secrets import choice
import mysql.connector as db
import pandas as pd
from tabulate import tabulate
import re
import random as r
import time
from authent1 import security

class feature(security):

    def __init__(self):

        # generates s_key for management login

        with open("Authenticator Of IBIZIA.txt", "a") as file:
            data = file.write(f"Generated security Key - {security.key(self)} at the time of - {time.ctime(time.time())}\n")

        # create connection string
        # create database

        mydb = db.connect(host = "localhost", user = "root", password = "root")
        cur = mydb.cursor()
        db_query = '''Create database if not exists hotel;'''
        cur.execute(db_query)
        mydb.close()
        
        # create table

        mydb = db.connect(host = "localhost", user = "root", password = "root", database = "hotel")
        cur = mydb.cursor()
        register_table = ''' create table if not exists registration(
                            R_id int not null auto_increment primary key,
                            Time varchar(30) not null,
                            Name varchar(50) not null,
                            Age varchar(10) not null,
                            Contact varchar(30) not null unique,
                            Location varchar(30) not null,
                            Uidai varchar(20) not null unique,
                            Email_ID varchar(40) not null unique,
                            User_Name varchar(50) not null unique,
                            Password varchar(30) not null unique);'''

        cur.execute(register_table)
        mydb.close()
        
    # create registration
    # create user-id & password

    # It removes data redundancy and connect directly 
    def set_connection(self):
        
        self.mydb = db.connect(host = "localhost", user = "root", password = "root", database = "hotel")
        self.cur = self.mydb.cursor()

    def set_registration(self,name, age, contact, location, uidai, email_id):

        name = name.strip()
        age = age.strip()
        contact = contact.strip()
        location = location.strip()
        uidai = uidai.strip()
        email_id = email_id.strip()

        print("\n~~~~~~~~~~~~~~~~~~~~ Create User-Id and Password ~~~~~~~~~~~~~~~~~~~~\n")
        print("► Username length should be 5-10 and Password length Should be 10\n")

        try:
            username = input("Create username - ")
            passwd = input("Create password - ")
        except:
            print("\n~~~~~~~~~~ Invalid Information ~~~~~~~~~~\n")

        u_name = username.strip()
        password = passwd.strip()

        self.set_connection()
        q1 = f'''select * from registration where Contact = "{contact}"'''
        self.cur.execute(q1)
        d1 = self.cur.fetchall()
        self.mydb.close()

        self.contact_valid_flag = False
        if len(contact) == 10 and contact != d1:
            self.contact_valid_flag = True

        # validation of uidai

        self.set_connection()
        q2 = f'''select * from registration where Uidai = "{uidai}"'''
        self.cur.execute(q2)
        d2 = self.cur.fetchall()
        self.mydb.close()

        self.uidai_valid_flag = False
        if len(uidai) == 12 and uidai != d2:
            self.uidai_valid_flag = True

        self.set_connection()
        q3 = f'''select * from registration where Email_ID = "{email_id}"'''
        self.cur.execute(q3)
        d3 = self.cur.fetchall()
        self.mydb.close()


        self.email_valid_flag = False
        ptr = r"[a-zA-Z0-9\.*]+@+[a-z]+\.+[com|in|net]+"
        if re.match(ptr, email_id) and email_id != d3:
            self.email_valid_flag = True

        # username length should be 10
        
        self.set_connection()
        q4 = f'''select * from registration where User_Name = "{u_name}"'''
        self.cur.execute(q4)
        d4 = self.cur.fetchall()
        self.mydb.close()

        self.u_name_valid_flag = False
        if len(u_name) >= 5 and len(u_name) <=10 and u_name != d4:
            self.u_name_valid_flag = True

        # password length should be 10
        
        self.password_valid_flag = False
        if len(password) == 10:
            self.password_valid_flag = True

        # for login purpose
        self.register_flag = False
        
        if (self.contact_valid_flag == True) and (self.uidai_valid_flag == True) and (self.email_valid_flag == True) and (self.u_name_valid_flag == True) and (self.password_valid_flag == True):

            # Insert data in db.registration
            self.set_connection()
            insert_data_query = f'''Insert into registration(Time, Name, Age, Contact, Location, Uidai, Email_ID, User_Name, Password) values
                                    ("{time.strftime("%d/%m/%Y %H:%M %p")}","{name}", "{age}", "{contact}", "{location}", "{uidai}", "{email_id}", "{u_name}", "{password}");'''
            self.cur.execute(insert_data_query)
            self.cur.execute("commit;")
            self.mydb.close()

            self.set_connection()
            # get customer data
            mobile_n = contact.strip()
            cus_data_query = f'''select * from registration where contact = "{mobile_n}";'''
            self.cur.execute(cus_data_query)
            data5 = self.cur.fetchall()
            #print(self.cur.execute(cus_data_query))
            self.mydb.close()

            df = pd.DataFrame(data5, columns = ["Id", "Time", "Name", "Age", "Contact", "Location", "Uidai", "Email ID", "User Name", "Password"])
            df.set_index("Id", inplace = True)
            print(tabulate(df, headers = "keys", tablefmt = "psql"))
            
            print("\n~~~~~~~~~~~~~~~~~~~~~~~ Registration Complete ~~~~~~~~~~~~~~~~~~~~~~~~\n")
            self.register_flag = True

        elif (self.contact_valid_flag == False) or (self.uidai_valid_flag == False) or (self.email_valid_flag == False) or (self.u_name_valid_flag == False) or (self.password_valid_flag == False):
            print("\n~~~~~~~~~~~~~~~~~~~~~~~  Invalid Information ~~~~~~~~~~~~~~~~~~~~~~~~~\n")

        else:
            print("\n~~~~~~~~~~~~~~~~~~~~~~~  Invalid Information ~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        
    def set_login(self, u_name, password):
        
        u_name = u_name.strip()
        password = password.strip()

        # check username and password are correct in db
        self.account_details_flag = False
        self.set_connection()
        check_query = f'''Select User_Name, Password from registration where User_Name = "{u_name}";'''
        self.cur.execute(check_query)
        data = self.cur.fetchall()
        self.mydb.close()

        # print(data)
        if data[0][0] == u_name and data[0][1] == password:
            self.account_details_flag = True
            print("\n~~~~~~~~~~ Login Successfully ~~~~~~~~~~\n")

        else:
            print("\n~~~~~~~~~~ Invalid Information ~~~~~~~~~~\n")

class specification(feature):

    def __init__(self):

        self.Delux_room_no = None
        self.Semi_room_no = None
        username = None
        room_id = None
        super().__init__()

        # table of bookings
        self.set_connection()
        bk_rm_query = '''create table if not exists booking_data(
                        B_id int not null auto_increment primary key,
                        UserName varchar(50) not null,
                        Time varchar(30) not null,
                        Room_No varchar(50) not null,
                        Check_IN varchar(30) not null,
                        Check_OUT varchar(30) not null,
                        No_Persons int not null,
                        Premium_Service varchar(30) not null,
                        Pay_Mode varchar(50) not null,
                        Credit_No varchar(50) not null,
                        RPrice int not null);'''
        self.cur.execute(bk_rm_query)
        self.mydb.close()

    def set_management_data(self, username, password):

        username = username.strip()
        password = password.strip()

        with open("Authenticator Of IBIZIA.txt", "r") as file:
            data = file.readlines()

        if username == 'data' and password == data[-1][25:35]:

            print("\n► 1 - Room no's   2 - Registration data   3 - Booking data  4 - Delete data  5 - Exit")

            while True:

                choice = int(input("\nEnter the choice - "))

                if choice == 1:
                    
                    print("\n►1 - Delux rooms   2 - Semi-delux\n")
                    choice1 = int(input("Enter the choice - "))

                    if choice1 == 1:
                        print("\nDelux Rooms\n")
                        for i in range(1001,1021):
                            if i <= 1009:
                                print(i, end = ",")
                            
                            elif i == 1010:
                                print(i, end = "\n")
                            
                            elif i > 1010 and i < 1020:
                                print(i, end = ",")

                            else:
                                print(i,end = ".")

                    else:
                        for i in range(101,121):
                            if i <= 109:
                                print(i, end = ",")
                            
                            elif i == 110:
                                print(i, end = "\n")
                            
                            elif i > 110 and i < 120:
                                print(i, end = ",")

                            else:
                                print(i,end = ".")

                elif choice == 2:

                    self.set_connection()
                    query = '''Select * from registration;'''
                    self.cur.execute(query)
                    table1 = self.cur.fetchall()
                    self.mydb.close()

                    print("\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬  REGISTRATION TABLE  ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n")

                    df = pd.DataFrame(table1, columns = ["Id", "Time", "Name", "Age", "Contact", "Location", "Uidai", "Email ID", "User Name", "Password"])
                    df.set_index("Id", inplace = True)
                    print(tabulate(df, headers = "keys", tablefmt = "psql"))


                elif choice == 3:

                    self.set_connection()
                    query = '''Select * from booking_data;'''
                    self.cur.execute(query)
                    table2 = self.cur.fetchall()
                    self.mydb.close()

                    print("\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬  BOOKING DATA  ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n")
                    df = pd.DataFrame(table2, columns = ["B_id", "UserName", "Time", "Room_No", "Check_IN", "Check_OUT", "No_Persons", "Premium_Service", "Pay_Mode", "Credit_No", "RPrice"])
                    df.set_index("B_id", inplace = True)
                    print(tabulate(df, headers = "keys", tablefmt = "psql"))

                    
                elif choice == 4:
                    
                    username = input("\nEnter username - ")
                    no = input("\nEnter Room no - ")
                    self.set_connection()
                    query = f'''Delete from booking_data where UserName = "{username}" and Room_No = {no};'''
                    self.cur.execute(query)
                    table2 = self.cur.fetchall()
                    self.mydb.close()
                    
                    print("\n~~~~~~~~~~ Data has been Deleted ~~~~~~~~~~\n")

                elif choice == 5:
                    print("\n~~~~~~~~~~ Exit ~~~~~~~~~~\n")
                    break

                else:
                    print("\n~~~~~~~~~~ Invalid Choice ~~~~~~~~~~\n")

    def set_delux_room(self, duration, check_in, check_out, persons, username, time1):

        # self.Delux_room_no = r.randint(10000,99999)

        r_n = [101,102,103,104,105,106,107,108,109,110,110,120,130,140,150,160,170,180,190,200]

        self.Delux_room_no = r.choice(r_n)
        print(self.Delux_room_no)

        duration = duration
        check_in = check_in.strip()
        check_out = check_out.strip()
        persons = persons
        username = username.strip()
        time1 = time1.strip()

        print("\nN O T E ⇨\n")
        print("\n\t\tFor Delux room base price ₹5000 per Day/Night\n\t\tPremium service charge ₹1500\n")

        services1 = input("\nPremium services yes/no - ")
        
        if services1 == "yes" or "Yes":
            
            amount = int(((5000+1500)*duration))
            print(f"\n► For the confirm booking you have to pay ₹{amount}\n")
            print(f"► For the Payment press 'enterkey'")

            press = input("\nPress the enterkey -")
            if press == "":

                print("\n► 1 - Credit/Debit Card   2 - Online Pay   3 - Cash\n")

                pay_mode = int(input("Choose the mode - "))

                if pay_mode == 1:

                    cardno = int(input("\n\t\t▪ Credit/Debit Card no - "))
                    amount1 = int(input("\n\t\t▪ Amount - "))
                    cardpin = input("\n\t\t▪ Pin - ")

                    if len(str(cardno)) == 12 and amount1 == amount and len(str(cardpin)) == 4:
                        
                        self.set_connection()
                        deluxy_query = f'''insert into booking_data(UserName, Time, Room_No, Check_IN, Check_OUT, No_Persons, Premium_Service, Pay_Mode, Credit_No, RPrice) values(
                                            "{username}", "{time1}", "D{self.Delux_room_no}", "{check_in}", "{check_out}", {persons}, "{services1}", "Credit or Debit card", "{cardno}", {amount});'''
                        self.cur.execute(deluxy_query)
                        self.cur.execute("commit;")
                        self.mydb.close()
                        print("\n\t\t~~~~~~~~~~ Payment Successfull !!! ~~~~~~~~~~~\n")
                        print(f"\n\t\t► Your Room no is - D{self.Delux_room_no}")
                        print("\n\t\tNOTE ⇨ R E M E M B E R   T H E   R O O M  I D*\n")

                elif pay_mode == 2:

                    print("\n► Use 1 - Google Pay  2 - Phone Pay  3 - Bharat Pay\n")
                    check1 = (1,2,3) 

                    online_plat = int(input("\n\t\t▪Choose the Mode - "))
                    print("\n\t\t▪Scan the QR code at the Counter.\n")
                    amount3 = int(input("\t\t▪Amount - "))
                    Done = input("\t\t▪To pay press enterkey\n")

                    if online_plat in check1 and amount3 == amount and Done == "":

                        self.set_connection()
                        deluxy_query = f'''insert into booking_data(UserName, Time, Room_No, Check_IN, Check_OUT, No_Persons, Premium_Service, Pay_Mode, Credit_No, RPrice) values(
                                            "{username}", "{time1}", "D{self.Delux_room_no}", "{check_in}", "{check_out}", {persons}, "{services1}", "UPI", "No", {amount});'''
                        self.cur.execute(deluxy_query)
                        self.cur.execute("commit;")
                        self.mydb.close()
                        print("\n\t\t~~~~~~~~~~ Payment Successfull !!! ~~~~~~~~~~~\n")
                        print(f"\n\t\t► Your Room no is - D{self.Delux_room_no}")
                        print("\n\t\tNOTE ⇨ R E M E M B E R   T H E   R O O M  I D*\n")

                elif pay_mode == 3:

                    cash = int(input("\n\t\t▪Amount - "))

                    if cash == amount:

                        self.set_connection()
                        deluxy_query = f'''insert into booking_data(UserName, Time, Room_No, Check_IN, Check_OUT, No_Persons, Premium_Service, Pay_Mode, Credit_No, RPrice) values(
                                            "{username}", "{time1}", "D{self.Delux_room_no}", "{check_in}", "{check_out}", {persons}, "{services1}", "Cash", "No", {amount});'''
                        self.cur.execute(deluxy_query)
                        self.cur.execute("commit;")
                        self.mydb.close()
                        print("\n\t\t~~~~~~~~~~ Payment Successfull !!! ~~~~~~~~~~~\n")
                        print(f"\n\t\t► Your Room no is - D{self.Delux_room_no}")
                        print("\n\t\tNOTE ⇨ R E M E M B E R   T H E   R O O M  I D*\n")
 
                else:
                    print("\n~~~~~~~~~~ Invalid Choice ~~~~~~~~~~\n")


            else:
                print("\n~~~~~~~~~~ Invalid Key ~~~~~~~~~~\n")

        elif services1 == "no" or "No":
            
            amount2 = int((5000)*duration)
            print(f"\n► For the confirm booking you have to pay ₹{amount2}\n")
            
            press = input("\nPress the enterkey -")
            if press == "":

                print("\n► 1 - Credit/Debit Card   2 - Online Pay   3 - Cash\n")

                pay_mode = int(input("Choose the mode - "))

                if pay_mode == 1:

                    cardno = int(input("\n\t\t▪ Credit/Debit Card no - "))
                    amount1 = int(input("\n\t\t▪ Amount - "))
                    cardpin = input("\n\t\t▪ Pin - ")

                    if len(str(cardno)) == 12 and amount1 == amount and len(str(cardpin)) == 4:
                        
                        self.set_connection()
                        deluxy_query = f'''insert into booking_data(UserName, Time, Room_No, Check_IN, Check_OUT, No_Persons, Premium_Service, Pay_Mode, Credit_No, RPrice) values(
                                            "{username}", "{time1}", "D{self.Delux_room_no}", "{check_in}", "{check_out}", {persons}, "{services1}", "Credit or Debit card", "{cardno}", {amount});'''
                        self.cur.execute(deluxy_query)
                        self.cur.execute("commit;")
                        self.mydb.close()
                        print("\n\t\t~~~~~~~~~~ Payment Successfull !!! ~~~~~~~~~~~\n")
                        print(f"\n\t\t► Your Room no is - D{self.Delux_room_no}")
                        print("\n\t\tNOTE ⇨ R E M E M B E R   T H E   R O O M  I D*\n")

                elif pay_mode == 2:

                    print("\n► Use 1 - Google Pay  2 - Phone Pay  3 - Bharat Pay\n")
                    check1 = (1,2,3) 

                    online_plat = int(input("\n\t\t▪Choose the Mode - "))
                    print("\n\t\t▪Scan the QR code at the Counter.\n")
                    amount3 = int(input("\t\t▪Amount - "))
                    Done = input("\t\t▪To pay press enterkey\n")

                    if online_plat in check1 and amount3 == amount and Done == "":

                        self.set_connection()
                        deluxy_query = f'''insert into booking_data(UserName, Time, Room_No, Check_IN, Check_OUT, No_Persons, Premium_Service, Pay_Mode, Credit_No, RPrice) values(
                                            "{username}", "{time1}", "D{self.Delux_room_no}", "{check_in}", "{check_out}", {persons}, "{services1}", "UPI", "No", {amount});'''
                        self.cur.execute(deluxy_query)
                        self.cur.execute("commit;")
                        self.mydb.close()
                        print("\n\t\t~~~~~~~~~~ Payment Successfull !!! ~~~~~~~~~~~\n")
                        print(f"\n\t\t► Your Room no is - D{self.Delux_room_no}")
                        print("\n\t\tNOTE ⇨ R E M E M B E R   T H E   R O O M  I D*\n")

                elif pay_mode == 3:

                    cash = int(input("\n\t\t▪Amount - "))

                    if cash == amount:

                        self.set_connection()
                        deluxy_query = f'''insert into booking_data(UserName, Time, Room_No, Check_IN, Check_OUT, No_Persons, Premium_Service, Pay_Mode, Credit_No, RPrice) values(
                                            "{username}", "{time1}", "D{self.Delux_room_no}", "{check_in}", "{check_out}", {persons}, "{services1}", "Cash", "No", {amount});'''
                        self.cur.execute(deluxy_query)
                        self.cur.execute("commit;")
                        self.mydb.close()
                        print("\n\t\t~~~~~~~~~~ Payment Successfull !!! ~~~~~~~~~~~\n")
                        print(f"\n\t\t► Your Room no is - D{self.Delux_room_no}")
                        print("\n\t\tNOTE ⇨ R E M E M B E R   T H E   R O O M  I D*\n")
 
                else:
                    print("\n~~~~~~~~~~ Invalid Choice ~~~~~~~~~~\n")


            else:
                print("\n~~~~~~~~~~ Invalid Key ~~~~~~~~~~\n")

    def set_semi_delux_room(self, duration, check_in, check_out, persons, username, time2):
        
        r_n = [1001,1002,1003,1004,1005,1006,1007,1008,1009,1010,1011,1012,1013,1014,1015,1016,1017,1018,1019,1020]

        self.Semi_room_no = r.choice(r_n)

        check_in = check_in.strip()
        check_out = check_out.strip()
        persons = persons
        username = username.strip()
        time2 = time2.strip()


        print("\nN O T E ⇨")
        print("\n\tFor Semi-Delux room base price ₹3000 per Day/Night\n\t\tPremium service charge ₹1500\n")

        services1 = input("Premium services yes/no - ")

        if services1 == "yes" or "Yes":
            print(f"\n► Your Room no is - S{self.Semi_room_no}")
            amount = int((3000+1500)*duration)
            print(f"\n► For the confirm booking you have to pay ₹{amount}\n")

            press = input("\nPress the enterkey -")
            if press == "":

                print("\n► 1 - Credit/Debit Card   2 - Online Pay   3 - Cash\n")

                pay_mode = int(input("Choose the mode - "))

                if pay_mode == 1:

                    cardno = int(input("\n\t\t▪ Credit/Debit Card no - "))
                    amount1 = int(input("\n\t\t▪ Amount - "))
                    cardpin = input("\n\t\t▪ Pin - ")

                    if len(str(cardno)) == 12 and amount1 == amount and len(str(cardpin)) == 4:
                        
                        self.set_connection()
                        deluxy_query = f'''insert into booking_data(UserName, Time, Room_No, Check_IN, Check_OUT, No_Persons, Premium_Service, Pay_Mode, Credit_No, RPrice) values(
                                            "{username}", "{time1}", "S{self.Semi_room_no}", "{check_in}", "{check_out}", {persons}, "{services1}", "Credit or Debit card", "{cardno}", {amount});'''
                        self.cur.execute(deluxy_query)
                        self.cur.execute("commit;")
                        self.mydb.close()
                        print("\n\t\t~~~~~~~~~~ Payment Successfull !!! ~~~~~~~~~~~\n")
                        print(f"\n\t\t► Your Room no is - D{self.Semi_room_no}")
                        print("\n\t\tNOTE ⇨ R E M E M B E R   T H E   R O O M  I D*\n")

                elif pay_mode == 2:

                    print("\n► Use 1 - Google Pay  2 - Phone Pay  3 - Bharat Pay\n")
                    check1 = (1,2,3) 

                    online_plat = int(input("\n\t\t▪Choose the Mode - "))
                    print("\n\t\t▪Scan the QR code at the Counter.\n")
                    amount3 = int(input("\t\t▪Amount - "))
                    Done = input("\t\t▪To pay press Enterkey\n")

                    if online_plat in check1 and amount3 == amount and Done == "":

                        self.set_connection()
                        deluxy_query = f'''insert into booking_data(UserName, Time, Room_No, Check_IN, Check_OUT, No_Persons, Premium_Service, Pay_Mode, Credit_No, RPrice) values(
                                            "{username}", "{time1}", "S{self.Semi_room_no}", "{check_in}", "{check_out}", {persons}, "{services1}", "UPI", "No", {amount});'''
                        self.cur.execute(deluxy_query)
                        self.cur.execute("commit;")
                        self.mydb.close()
                        print("\n\t\t~~~~~~~~~~ Payment Successfull !!! ~~~~~~~~~~~\n")
                        print(f"\n\t\t► Your Room no is - D{self.Semi_room_no}")
                        print("\n\t\tNOTE ⇨ R E M E M B E R   T H E   R O O M  I D*\n")

                elif pay_mode == 3:

                    cash = int(input("\n\t\t▪Amount - "))

                    if cash == amount:

                        self.set_connection()
                        deluxy_query = f'''insert into booking_data(UserName, Time, Room_No, Check_IN, Check_OUT, No_Persons, Premium_Service, Pay_Mode, Credit_No, RPrice) values(
                                            "{username}", "{time1}", "S{self.Semi_room_no}", "{check_in}", "{check_out}", {persons}, "{services1}", "Cash", "No", {amount});'''
                        self.cur.execute(deluxy_query)
                        self.cur.execute("commit;")
                        self.mydb.close()
                        print("\n\t\t~~~~~~~~~~ Payment Successfull !!! ~~~~~~~~~~~\n")
                        print(f"\n\t\t► Your Room no is - D{self.Semi_room_no}")
                        print("\n\t\tNOTE ⇨ R E M E M B E R   T H E   R O O M  I D*\n")

                else:
                    print("\n~~~~~~~~~~ Invalid Choice ~~~~~~~~~~\n")


            else:
                print("\n~~~~~~~~~~ Invalid Key ~~~~~~~~~~\n")

        elif services1 == "no" or "No":

            amount = int((3000)*duration)
            print(f"\n► For the confirm booking you have to pay ₹{amount}\n")

            press = input("\nPress the enterkey -")
            if press == "":

                print("\n► 1 - Credit/Debit Card   2 - Online Pay   3 - Cash\n")

                pay_mode = int(input("Choose the mode - "))

                if pay_mode == 1:

                    cardno = int(input("\n\t\t▪ Credit/Debit Card no - "))
                    amount1 = int(input("\n\t\t▪ Amount - "))
                    cardpin = input("\n\t\t▪ Pin - ")

                    if len(str(cardno)) == 12 and amount1 == amount and len(str(cardpin)) == 4:
                        
                        self.set_connection()
                        deluxy_query = f'''insert into booking_data(UserName, Time, Room_No, Check_IN, Check_OUT, No_Persons, Premium_Service, Pay_Mode, Credit_No, RPrice) values(
                                            "{username}", "{time1}", "S{self.Semi_room_no}", "{check_in}", "{check_out}", {persons}, "{services1}", "Credit or Debit card", "{cardno}", {amount});'''
                        self.cur.execute(deluxy_query)
                        self.cur.execute("commit;")
                        self.mydb.close()
                        print("\n\t\t~~~~~~~~~~ Payment Successfull !!! ~~~~~~~~~~~\n")
                        print(f"\n\t\t► Your Room no is - D{self.Semi_room_no}")
                        print("\n\t\tNOTE ⇨ R E M E M B E R   T H E   R O O M  I D*\n")

                elif pay_mode == 2:

                    print("\n► Use 1 - Google Pay  2 - Phone Pay  3 - Bharat Pay\n")
                    check1 = (1,2,3) 

                    online_plat = int(input("\n\t\t▪Choose the Mode - "))
                    print("\n\t\t▪Scan the QR code at the Counter.\n")
                    amount3 = int(input("\t\t▪Amount - "))
                    Done = input("\t\t▪To pay press enterkey -\n")

                    if online_plat in check1 and amount3 == amount and Done == "":

                        self.set_connection()
                        deluxy_query = f'''insert into booking_data(UserName, Time, Room_No, Check_IN, Check_OUT, No_Persons, Premium_Service, Pay_Mode, Credit_No, RPrice) values(
                                            "{username}", "{time1}", "S{self.Semi_room_no}", "{check_in}", "{check_out}", {persons}, "{services1}", "UPI", "No", {amount});'''
                        self.cur.execute(deluxy_query)
                        self.cur.execute("commit;")
                        self.mydb.close()
                        print("\n\t\t~~~~~~~~~~ Payment Successfull !!! ~~~~~~~~~~~\n")
                        print(f"\n\t\t► Your Room no is - D{self.Semi_room_no}")
                        print("\n\t\tNOTE ⇨ R E M E M B E R   T H E   R O O M  I D*\n")

                elif pay_mode == 3:

                    cash = int(input("\n\t\t▪Amount - "))

                    if cash == amount:

                        self.set_connection()
                        deluxy_query = f'''insert into booking_data(UserName, Time, Room_No, Check_IN, Check_OUT, No_Persons, Premium_Service, Pay_Mode, Credit_No, RPrice) values(
                                            "{username}", "{time1}", "S{self.Semi_room_no}", "{check_in}", "{check_out}", {persons}, "{services1}", "Cash", "No", {amount});'''
                        self.cur.execute(deluxy_query)
                        self.cur.execute("commit;")
                        self.mydb.close()
                        print("\n\t\t~~~~~~~~~~ Payment Successfull !!! ~~~~~~~~~~~\n")
                        print(f"\n\t\t► Your Room no is - D{self.Semi_room_no}")
                        print("\n\t\tNOTE ⇨ R E M E M B E R   T H E   R O O M  I D*\n")
 
                else:
                    print("\n~~~~~~~~~~ Invalid Choice ~~~~~~~~~~\n")


            else:
                print("\n~~~~~~~~~~ Invalid Key ~~~~~~~~~~\n")

    def get_booking_info(self, username, room_id):

        username = username.strip()
        room_id = room_id.strip()

        self.set_connection()
        query = f'''Select * from booking_data where UserName = "{username}" and Room_No = "{room_id}"'''
        self.cur.execute(query)
        data = self.cur.fetchall()
        self.cur.close()

        # to show data in table form
        df = pd.DataFrame(data, columns = ["B_id", "UserName", "Time", "Room_No", "Check_IN", "Check_OUT", "No_Persons", "Premium_Service", "Pay_Mode", "Credit_No", "RPrice"])
        df.set_index("B_id", inplace = True)
        print(tabulate(df, headers = "keys", tablefmt = "psql"))

if __name__ == "__main__":
    
    room = specification()
        
    while True:

        print("\n⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶  WELCOME TO ABC HOTEL ⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶\n")
        print("►► 1-For Management\n►► 2-Facilities\n►► 3-Online Booking\n►► 4-Buy Orders")
        print("►► 5-Booking Info\n►► 6-Orders Info\n►► 7-Exit")

        try:
            ch = int(input("\nChoose the field - "))
                
        except:
            ch = None
            print("\n⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶  Enter valid choice ⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶\n")

        try:
            if ch == 1:
                print("\n⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶  For Management ⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶\n")
                
                username = input("Enter the username - ")
                password = input("Enter the Password - ")

                room.set_management_data(username, password)

            elif ch == 2:
                print("\n⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶  Facilities ⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶\n")

            elif ch == 3:
                print("\n⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶  Online Booking ⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶\n")

                print("\n1- Registration\n2- Login\n")

                try:
                    ch1 = int(input("Choose the field - "))
                        
                except:
                    print("\n~~~~~~~~~~ Invalid Choice ~~~~~~~~~~\n")

                try:
                    if ch1 == 1:

                        print("\n~~~~~~~~~~ Do Registration First ~~~~~~~~~~\n")

                        name = input("Enter the name - ")
                        age = input("Enter the age - ")
                        contact = input("Enter the contact -")
                        location = input("Enter the address location - ")
                        uidai = input("Enter the Adhaar number - ")
                        email_id = input("Enter the email_id - ")
                        
                        room.set_registration(name, age, contact, location, uidai, email_id)

                    elif ch1 == 2:
                        print("\n~~~~~~~~~~ Login Page ~~~~~~~~~~\n")

                        u_name = input("Enter the user name - ")
                        password = input("Enter the password - ")

                        room.set_login(u_name, password)

                        if room.account_details_flag == True:

                            while True:
                            
                                print("\n~~~~~~~~~~ Choose Room Specification ~~~~~~~~~~\n")
                                #print("Fill all data*")
                                #print("⊶⊶⊶⊶⊶⊶  Category- Date of travel and guest|Room ⊶⊶⊶⊶⊶⊶\n")

                                print("\n► Room » 1- Delux  2- semi-Delux  3- Exit\n")

                                ch2 = int(input("Enter the specification - "))

                                if ch2 == 1:

                                    print("\n~~~~~~~~~~ Delux ~~~~~~~~~~\n")                                
                                    duration = int(input("►Days/Nights - "))
                                    check_in = input("\n► Check In Date - ")
                                    check_out = input("\n► Check Out Date - ")
                                    persons = int(input("\n► Count of people - "))
                                    username = input("\n► Enter the Username - ")
                                    time1 = input("\n► Enter time (24:00) - ")

                                    room.set_delux_room(duration, check_in, check_out, persons, username, time1)
                                            
                                elif ch2 == 2:
                                        
                                    print("\n~~~~~~~~~~ Semi-Delux ~~~~~~~~~~\n")
                                    duration = int(input("► Days/Nights - "))
                                    check_in = input("\n► Check In Date - ")
                                    check_out = input("\n► Check Out Date - ")
                                    persons = int(input("\n► Count of people - "))
                                    username = input("\n► Enter the Username - ")
                                    time2 = input("\n► Enter time (24:00) - ")

                                    room.set_semi_delux_room(duration, check_in, check_out, persons, username, time2)
                                    
                                elif ch2 == 3:
                                    print("\n~~~~~~~~~~ Exit ~~~~~~~~~~\n")
                                    break
                                    
                                else:
                                    print("\n~~~~~~~~~~ Invalid choice ~~~~~~~~~~\n")
                                
                    else:
                        print("\n~~~~~~~~~~ Invalid Choice ~~~~~~~~~~\n")
                        
                except:
                    pass

            elif ch == 4:
                print("\n⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶  Buy Orders ⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶\n")

            elif ch == 5:
                print("\n⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶  Booking Info ⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶\n")

                username = input("\nEnter Username - ")
                room_id = input("\nEnter your Room-ID - ")

                room.get_booking_info(username, room_id)

            elif ch == 6:
                print("\n⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶  Orders Info ⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶\n")

            elif ch == 7:
                print("\n⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶  Exit ⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶\n")
                break

            else:
                print("\n⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶  Invalid choice ⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶⊶\n")

        except:
            print("HERE WE GO AGAIN")