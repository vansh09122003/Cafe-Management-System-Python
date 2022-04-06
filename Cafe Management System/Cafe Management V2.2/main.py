from management import management_menu,management_menu_hindi
from user import user_menu,user_menu_hindi
import pandas as pd
import numpy as np
import mysql.connector as sqltor
import pymysql
from sqlalchemy import create_engine

def my_sql_data_write(table,value,type_r_a):
    engine=create_engine('mysql+pymysql://root:root@localhost/cafe') 
    myconn=engine.connect()
    try:
        value.to_sql(name=table,con=myconn,index=False,if_exists=type_r_a)
    except ValueError as e:
        print(e)
    except Exception as e1:
        print(e1)

def my_sql_data_fetch(query):
    myconn=sqltor.connect(host="localhost",user="root",passwd="root",database="cafe") 
    if myconn.is_connected():
        database_data=pd.read_sql(query,myconn)
        if database_data.empty==True:
            database_data.loc["Not Found",:]=""
    return database_data

def main_menu():
    #1
    print("1.Enter 1 for English")
    print("2.Enter 2 for Hindi")
    choice=int(input("Please select language "))
    if choice==1:
        login_eng()
    elif choice==2:
        login_hindi()
        print("")
    else:
        print("Please make a Valid Choice")
        main_menu()

##ENGLISH 

def login_eng():
    print("1.For changing password enter 1")
    print("")
    print("2.For login enter 2")
    print("")
    print("3.To sign up enter 3")
    print("")
    print("4.To return to previous menu enter 3")
    print("")
    choice=int(input("Enter Choice "))
    if choice==1:
        change_pass()
    elif choice==2:
        
        id_=input("Enter Id ")
        pass_=input("Enter Password ")

        query_user="select * from user where user_id='"+id_+"';"
        data_user=my_sql_data_fetch(query_user)
        query_manage="select * from management where management_id='"+id_+"';"
        data_manage=my_sql_data_fetch(query_manage)

        if id_==data_manage.management_id[0] and pass_==data_manage.password[0]:
            print("")
            print("Verification Sucessfull")
            management_menu()
        elif id_==data_user.user_id[0] and pass_==data_user.user_password[0]:
            print("")
            print("Verification Sucessfull")
            user_menu()
        else:
            print("")
            print("wrong user or pass please try again")
            login_eng()
    elif choice==3:
        sign_up()
    elif choice==4:
        main_menu()
    else:
        print("Please make a valid choice")
        login_eng()

def sign_up():
    #4
    i=0
    print("Please note that if you have used phone number once you cant use that again")
    print("")
    print("If you forgot password please use forgot password option")
    print("")
    print("1.To return to login menu enter 1")
    print("")
    print("2.To continue sign up enter 2")
    print("")
    choice=int(input("Make your choice "))
    if choice==1:
        login_eng()
    elif choice==2:
        id_=input("Enter unique User Id ")
        query_user="select * from user;"
        data_user=my_sql_data_fetch(query_user)
        query_manage="select * from management;"
        data_manage=my_sql_data_fetch(query_manage)
        while i==0:
            for j in data_user["user_id"]:
                for l in data_manage["management_id"]:
                    if id_==j or id_==l:
                        print("")
                        print("Username alredy taken")
                        print("")
                        print("Try another user name")
                        print("")
                        id_=input("Enter unique User Id ")
                    else:
                        i=1
        pass_=input("Enter Password ")
        print("")
        contact_no=input("Enter Mobile Number ")
        i=0
        while i==0:
            for j in data_user["contact_no"]:
                for l in data_manage["contact_no"]:
                    if id_==i or id_==l:
                        print("")
                        print("Contact Number alredy taken")
                        print("")
                        print("Try another Contact Number")
                        print("")
                        contact_no=input("Enter unique Contact Number ")
                    else:
                        i=1
        address_=input("Enter Address ")
        print("")
        pincode_=input("Enter Pincode ")
        print("")
        data={"user_id":id_,"user_password":pass_,"contact_no":contact_no,"address":address_,"pincode":pincode_}
        data=pd.DataFrame(data,index=[0])
        my_sql_data_write("user",data,"append")
        login_eng()

def change_pass():
    id_=input("Enter Id ")
    contact_no=input("Enter registered Contact number ")

    query_user="select * from user where user_id='"+id_+"';"
    data_user=my_sql_data_fetch(query_user)
    query_manage="select * from management where management_id='"+id_+"';"
    data_manage=my_sql_data_fetch(query_manage)    

    if id_==data_manage.management_id[0] and contact_no==data_manage.contact_no[0]:
        print("")
        print("Verification Sucessfull")
        print("")
        new_pass=input("Enter new password")
        data=my_sql_data_fetch("select * from management")
        data.loc[data["management_id"]==id_,["password"]]=new_pass
        my_sql_data_write('management',data,'replace')
    elif id_==data_user.user_id[0] and contact_no==data_user.contact_no[0]:
        print("")
        print("Verification Sucessfull")
        print("")
        new_pass=input("Enter new password")
        data=my_sql_data_fetch("select * form user")
        data.loc[data["user_id"]==id_,["user_password"]]=new_pass
        my_sql_data_write('user',data,'replace')
    else:
        print("")
        print("wrong user or pass please try again")
        login_eng()


##HINDI

def login_hindi():
    print("1.For changing password enter 1")
    print("")
    print("2.For login enter 2")
    print("")
    print("3.To sign up enter 3")
    print("")
    print("4.To return to previous menu enter 3")
    print("")
    choice=int(input("Enter Choice "))
    if choice==1:
        change_pass()
    elif choice==2:
        
        id_=input("Enter Id ")
        pass_=input("Enter Password ")

        query_user="select * from user where user_id='"+id_+"';"
        data_user=my_sql_data_fetch(query_user)
        query_manage="select * from management where management_id='"+id_+"';"
        data_manage=my_sql_data_fetch(query_manage)

        if id_==data_manage.management_id[0] and pass_==data_manage.password[0]:
            print("")
            print("Verification Sucessfull")
            management_menu_hindi()
        elif id_==data_user.user_id[0] and pass_==data_user.user_password[0]:
            print("")
            print("Verification Sucessfull")
            user_menu_hindi()
        else:
            print("")
            print("wrong user or pass please try again")
            login_hindi()
    elif choice==3:
        sign_up()
    elif choice==4:
        main_menu()
    else:
        print("Please make a valid choice")
        login_hindi()

def sign_up_hindi():
    #4
    i=0
    print("Please note that if you have used phone number once you cant use that again")
    print("")
    print("If you forgot password please use forgot password option")
    print("")
    print("1.To return to login menu enter 1")
    print("")
    print("2.To continue sign up enter 2")
    print("")
    choice=int(input("Make your choice "))
    if choice==1:
        login_hindi()
    elif choice==2:
        id_=input("Enter unique User Id ")
        query_user="select * from user;"
        data_user=my_sql_data_fetch(query_user)
        query_manage="select * from management;"
        data_manage=my_sql_data_fetch(query_manage)
        while i==0:
            for j in data_user["user_id"]:
                for l in data_manage["management_id"]:
                    if id_==j or id_==l:
                        print("")
                        print("Username alredy taken")
                        print("")
                        print("Try another user name")
                        print("")
                        id_=input("Enter unique User Id ")
                    else:
                        i=1
        pass_=input("Enter Password ")
        print("")
        contact_no=input("Enter Mobile Number ")
        i=0
        while i==0:
            for j in data_user["contact_no"]:
                for l in data_manage["contact_no"]:
                    if id_==i or id_==l:
                        print("")
                        print("Contact Number alredy taken")
                        print("")
                        print("Try another Contact Number")
                        print("")
                        contact_no=input("Enter unique Contact Number ")
                    else:
                        i=1
        address_=input("Enter Address ")
        print("")
        pincode_=input("Enter Pincode ")
        print("")
        data={"user_id":id_,"user_password":pass_,"contact_no":contact_no,"address":address_,"pincode":pincode_}
        data=pd.DataFrame(data,index=[0])
        my_sql_data_write("user",data,"append")
        login_hindi()

def change_pass_hindi():
    id_=input("Enter Id ")
    contact_no=input("Enter registered Contact number ")

    query_user="select * from user where user_id='"+id_+"';"
    data_user=my_sql_data_fetch(query_user)
    query_manage="select * from management where management_id='"+id_+"';"
    data_manage=my_sql_data_fetch(query_manage)    

    if id_==data_manage.management_id[0] and contact_no==data_manage.contact_no[0]:
        print("")
        print("Verification Sucessfull")
        print("")
        new_pass=input("Enter new password")
        data=my_sql_data_fetch("select * from management")
        data.loc[data["management_id"]==id_,["password"]]=new_pass
        my_sql_data_write('management',data,'replace')
    elif id_==data_user.user_id[0] and contact_no==data_user.contact_no[0]:
        print("")
        print("Verification Sucessfull")
        print("")
        new_pass=input("Enter new password")
        data=my_sql_data_fetch("select * form user")
        data.loc[data["user_id"]==id_,["user_password"]]=new_pass
        my_sql_data_write('user',data,'replace')
    else:
        print("")
        print("wrong user or pass please try again")
        login_hindi()
##main_menu
main_menu()