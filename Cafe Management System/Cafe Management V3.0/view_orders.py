import pandas as pd
import numpy as np
import mysql.connector as sqltor
import pymysql
from sqlalchemy import create_engine

def my_sql_management_fetch():
    myconn=sqltor.connect(host="localhost",user="root",passwd="root",database="cafe") 
    if myconn.is_connected():
        database_data=pd.read_sql("select * from management;",myconn)
    return database_data

def my_sql_orders_fetch():
    myconn=sqltor.connect(host="localhost",user="root",passwd="root",database="cafe") 
    if myconn.is_connected():
        database_data=pd.read_sql("select * from orders where status='pending';",myconn)
        if database_data.empty==True:
            database_data.loc["No Orders",:]=""
    return database_data

def main_menu():
    print("1.Enter 1 for English")
    print("2.Enter 2 for Hindi")
    choice=int(input("Please Select language "))
    if choice==1:
        management_login_eng()
    elif choice==2:
        management_login_hindi()
    else:
        print("Please make a valid choice")
        main_menu()

def management_login_eng():
    #3
    manage_id=input("Enter Id ")
    manage_pass=input("Enter password ")
    print("Verifying")
    data=my_sql_management_fetch()
    index=[]
    sucess=0
    for i in data.index:
        index.append(i)
    for j in index:
        if manage_id==data.management_id[j] and manage_pass==data.password[j]:
            sucess=1
            break
        else:
            continue
    if sucess==1:
        print("Verification Successful")
        display_pending()
    else:
        print("Wrong username or password")
        print("")
        print("Please Try Again")
        management_login_eng()

def management_login_hindi():
    #3
    manage_id=input("आईडी दर्ज करें ")
    manage_pass=input("पास वर्ड दर्ज करें ")
    data=my_sql_management_fetch()
    index=[]
    sucess=0
    for i in data.index:
        index.append(i)
    for j in index:
        if manage_id==data.management_id[j] and manage_pass==data.password[j]:
            sucess=1
            break
        else:
            continue
    if sucess==1:
        print("सत्यापन सफल ")
        display_pending()
    else:
        print("उपयोगकर्ता का गलत नाम और पासवर्ड")
        print("")
        print("कृपया पुन: प्रयास करें")
        management_login_hindi()

def display_pending():
    i=1

    orders=my_sql_orders_fetch()
    already_present=pd.DataFrame(orders)
    print(orders)
    
    while i==1:
        orders=my_sql_orders_fetch()
        if orders.size != already_present.size:
            print("")
            print("NEW ORDERS")
            print("")
            already_present=pd.DataFrame(orders)
            print(orders)
        else:
            continue

##Main 
main_menu()
