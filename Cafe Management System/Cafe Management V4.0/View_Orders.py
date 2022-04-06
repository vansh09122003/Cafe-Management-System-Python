import pandas as pd
import numpy as np
import mysql.connector as sqltor
import pymysql
from sqlalchemy import create_engine

def my_sql_data_fetch(query,type_o):
    empty=0
    myconn=sqltor.connect(host="localhost",user="root",passwd="root",database="cafe") 
    if myconn.is_connected():
        database_data=pd.read_sql(query,myconn)
        if database_data.empty==True and type_o=="orders":
            database_data.loc["No Orders",:]=""
            empty=1
        elif database_data.empty==True and type_o=="verification":
            database_data.loc["No data found",:]=""
            empty=1
    return database_data,empty

def main_menu():
    print("1.Enter 1 for English")
    print("2.Enter 2 for Hindi")
    choice=int(input("Please Select language "))
    if choice==1:
        management_login_eng()
    elif choice==2:
        management_login_hindi()
    else:
        print("Please Make a Valid Choice")
        main_menu()

def management_login_eng():
    #3
    manage_id=input("Enter Id ")
    manage_pass=input("Enter password ")
    print("Verifying")
    data_,empty=my_sql_data_fetch("select * from management where management_id='"+manage_id+"';","verification")
    if empty==0:
        if manage_id==data_.management_id[0] and manage_pass==data_.password[0]:
            print("")
            print("Verification Successful")
            display_pending()
        else:
            print("")
            print("Wrong User ID or Password")
            management_login_eng()
    else:
        print("")
        print("Something Went Wrong")

def management_login_hindi():
    #3
    manage_id=input("आईडी दर्ज करें ")
    manage_pass=input("पास वर्ड दर्ज करें ")
    print("सत्यापन")
    data_,empty=my_sql_data_fetch("select * from management where management_id='"+manage_id+"';","verification")
    if empty==0:
        if manage_id==data_.management_id[0] and manage_pass==data_.password[0]:
            print("")
            print("सत्यापन सफल")
            display_pending()
        else:
            print("")
            print("गलत यूजर आईडी या पासवर्ड")
            management_login_hindi()
    else:
        print("")
        print("कुछ गलत हो गया")

def display_pending():
    i=1

    orders,empty=my_sql_data_fetch("select * from orders where status='pending';","orders")
    if empty==0 or empty==1:
        already_present=pd.DataFrame(orders)
        print(orders)
    
        while i==1:
            orders,empty=my_sql_data_fetch("select * from orders where status='pending';","orders")
            if empty==0:
                if orders.size != already_present.size:
                    print("")
                    print("NEW ORDERS")
                    print("")
                    already_present=pd.DataFrame(orders)
                    print(orders)
                else:
                    continue
            else:
                print("")
                print("Something Went Wrong")
    else:
        print("")
        print("Something Went Wrong")

