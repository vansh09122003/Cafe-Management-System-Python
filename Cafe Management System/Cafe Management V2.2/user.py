import pandas as pd
import numpy as np
import mysql.connector as sqltor
import pymysql
from datetime import date
from sqlalchemy import create_engine

def my_sql_data_fetch(query):
    myconn=sqltor.connect(host="localhost",user="root",passwd="root",database="cafe") 
    if myconn.is_connected():
        database_data=pd.read_sql(query,myconn)
        if database_data.empty==True:
            database_data.loc["Not Found",:]=""
    return database_data

def my_sql_data_write(table,value,type_r_a):
    engine=create_engine('mysql+pymysql://root:root@localhost/cafe') 
    myconn=engine.connect()
    try:
        value.to_sql(name=table,con=myconn,index=False,if_exists=type_r_a)
    except ValueError as e:
        print(e)
    except Exception as e1:
        print(e1)

def change_pass_user():
    #4
    id_=input("Enter Id ")
    contact_no=input("Enter registered Contact number ")

    query_user="select * from user where user_id='"+id_+"';"
    data_user=my_sql_data_fetch(query_user)    

    if id_==data_user.user_id[0] and contact_no==data_user.contact_no[0]:
        print("")
        print("Verification Sucessfull")
        print("")
        new_pass=input("Enter new password")
        data=my_sql_data_fetch("select * from user")
        data.loc[data["user_id"]==id_,["user_password"]]=new_pass
        my_sql_data_write('user',data,'replace')
        user_menu()
    else:
        print("")
        print("wrong user or pass please try again")
        user_menu()

def user_menu():
    #4
    print("1.For placing an order enter 1")
    print("")
    print("2.For changing details enter 2")
    print("")
    choice=int(input("Make your choice "))
    if choice==1:
        order_place()
    elif choice==2:
        user_detail_changer()
    else:
        print("Make a correct Choice ")
        user_menu()

def order_place():
    #4
    items=my_sql_data_fetch("select * from items;")
    print(items)
    i="0"
    item_names=""
    selected_index_s=[]
    selected_index_i=[]
    total_items=0
    total_price=0
    print("Enter / to generate bill")
    while i=="0":
        choice=input("Enter Index of item to Bill ")
        if choice!="/":
            selected_index_s.append(choice)
        elif choice=="/":
            i="/"
    for j in selected_index_s:
        selected_index_i.append(int(j))
    bill=pd.DataFrame(items.loc[selected_index_i,"name":"price"])
    bill.index=range(1,len(selected_index_i)+1)
    for k in bill["price"]:
        total_items+=1
        print("")
        total_price += int(k)
    total={"name":str(total_items),"price":str(total_price)}
    bill.loc["Total",:]=total
    print(bill)
    print("")
    print("1.Enter 1 to confirm order")
    print("")
    print("2.Enter 2 to change")
    print("")
    choice=int(input("Make a Choice "))
    if choice==1:
        bill_np_array=bill.values
        for l in range(0,len(bill_np_array)-1):
            item_names+=bill_np_array[l][0]+','
        date_today=date.today()
        print("We Need to confirm your identity")
        print("")
        user_id=input("Enter User Id ")
        print("")
        user_password=input("Enter Password")
        print("")

        query_user="select * from user where user_id='" + user_id + "';"
        data_user=my_sql_data_fetch(query_user)

        if user_id==data_user.user_id[0] and user_password==data_user.user_password[0]:
            order={"user_id":user_id,"items":item_names,"total_price":total_price,"address":data_user.address[0],"order_date":date_today,"status":"pending"}
            order=pd.DataFrame(order,index=[0])
            my_sql_data_write("orders",order,"append")
            user_menu()
        else:
            print("")
            print("wrong user or pass please try again")
            order_place()

    elif choice==2:
        order_place()
    else:
        print("")
        print("Wrong Choice try again")
        order_place()

def user_detail_changer():
    #4
    print("1.To change password enter 1")
    print("")
    print("2.To change contact number enter 2")
    print("")
    print("3.To change address and pincode enter 3")
    print("")
    choice=int(input("Make a Choice "))
    if choice==1:
        change_pass_user()
    elif choice==2:
        change_user_contact_no()
    elif choice==3:
        change_user_address()
    else:
        print("Make a Correct Choice")

def change_user_contact_no():
    #5
    i=0
    user_id=input("Enter Id ")
    print("")
    user_pass=input("Enter Password ")
    print("")
    print("Verifying")

    query_user="select * from user where user_id='"+user_id+"';"
    data_user=my_sql_data_fetch(query_user)

    if user_id==data_user.user_id[0] and user_pass==data_user.user_password[0]:
        contact_no=input("Enter unique contact number")
        while i==0:
            for j in data_user["contact_no"]:
                if contact_no==j :
                    print("")
                    print("Contact Number alredy taken")
                    print("")
                    print("Try another Contact Number")
                    print("")
                    contact_no=input("Enter unique Contact Number ")
                else:
                    i=1
        data=my_sql_data_fetch("select * from user;")
        data.loc[data["user_id"]==user_id,["contact_no"]]=contact_no
        my_sql_data_write('user',data,'replace')
        user_menu()
    else:
        print("")
        print("wrong user or pass please try again")
        change_user_contact_no()

def change_user_address():
    #5
    user_id=input("Enter Id ")
    print("")
    user_pass=input("Enter Password ")
    print("")
    print("Verifying")

    query_user="select * from user where user_id='"+user_id+"';"
    data_user=my_sql_data_fetch(query_user)    

    if user_id==data_user.user_id[0] and user_pass==data_user.user_password[0]:
        user_address=input("Enter New Address ")
        user_pincode=input("Enter new Pincode")
        data=my_sql_data_fetch("select * from user;")
        data.loc[data["user_id"]==user_id,["pincode"]]=user_pincode
        my_sql_data_write('user',data,'replace')
        data.loc[data["user_id"]==user_id,["address"]]=user_address
        my_sql_data_write('user',data,'replace')
        user_menu()
    else:
        print("Wrong User Id or password")
        print("")
        print("Please Try Again")
        change_user_address()

##HINDI MENU

def change_pass_user_hindi():
        #4
    id_=input("Enter Id ")
    contact_no=input("Enter registered Contact number ")

    query_user="select * from user where user_id='"+id_+"';"
    data_user=my_sql_data_fetch(query_user)    

    if id_==data_user.user_id[0] and contact_no==data_user.contact_no[0]:
        print("")
        print("Verification Sucessfull")
        print("")
        new_pass=input("Enter new password")
        data=my_sql_data_fetch("select * form user")
        data.loc[data["user_id"]==id_,["user_password"]]=new_pass
        my_sql_data_write('user',data,'replace')
        user_menu_hindi()
    else:
        print("")
        print("wrong user or pass please try again")
        user_menu_hindi()

def user_menu_hindi():
    #4
    print("1.आदेश देने के लिए 1 दर्ज करें")
    print("")
    print("2.विवरण बदलने के लिए 2 दर्ज करें")
    print("")
    choice=int(input("अपनी पसंद करें "))
    print("")
    if choice==1:
        order_place_hindi()
    elif choice==2:
        user_detail_changer_hindi()
    else:
        print("एक सही चुनाव करें")
        user_menu_hindi()

def order_place_hindi():
    #4
    items=my_sql_data_fetch("select * from items;")
    print(items)
    i="0"
    item_names=""
    selected_index_s=[]
    selected_index_i=[]
    total_items=0
    total_price=0
    print("बिल जनरेट करना / दर्ज करना")
    print("")
    while i=="0":
        choice=input("बिल के लिए आइटम का सूचकांक दर्ज करें ")
        if choice!="/":
            selected_index_s.append(choice)
        elif choice=="/":
            i="/"
    for j in selected_index_s:
        selected_index_i.append(int(j))
    bill=pd.DataFrame(items.loc[selected_index_i,"name":"price"])
    bill.index=range(1,len(selected_index_i)+1)
    for k in bill["price"]:
        total_items+=1
        total_price += int(k)
    total={"name":str(total_items),"price":str(total_price)}
    bill.loc["Total",:]=total
    print(bill)
    print("")
    print("1.आदेश की पुष्टि करने के लिए 1 दर्ज करें")
    print("")
    print("2.बदलने के लिए 2 दर्ज करें")
    print("")
    choice=int(input("एक का चयन करो "))
    print("")
    if choice==1:
        bill_np_array=bill.values
        for l in range(0,len(bill_np_array)-1):
            item_names+=bill_np_array[l][0]+','
        date_today=date.today()
        print("हमें आपकी पहचान की पुष्टि करने की आवश्यकता है")
        print("")
        user_id=input("उपयोगकर्ता आईडी दर्ज करें ")
        print("")
        user_password=input("पास वर्ड दर्ज करें ")
        print("")

        query_user="select * from user where user_id='"+user_id+"';"
        data_user=my_sql_data_fetch(query_user)

        if user_id==data_user.user_id[0] and user_password==data_user.user_password[0]:
            order={"user_id":user_id,"items":item_names,"total_price":total_price,"address":data_user.address[0],"order_date":date_today,"status":"pending"}
            order=pd.DataFrame(order,index=[0])
            my_sql_data_write("orders",order,"append")
            user_menu_hindi()
        else:
            print("")
            print("wrong user or pass please try again")
            order_place_hindi()

    elif choice==2:
        order_place_hindi()
    else:
        print("गलत चॉइस फिर से कोशिश करें")
        order_place_hindi()

def user_detail_changer_hindi():
    #4
    print("1.पासवर्ड बदलने के लिए 1 दर्ज करें")
    print("")
    print("2.संपर्क नंबर बदलने के लिए 2 दर्ज करें")
    print("")
    print("3.पता बदलने के लिए और पिनकोड 3 दर्ज करें")
    print("")
    choice=int(input("एक का चयन करो "))
    if choice==1:
        change_pass_user_hindi()
    elif choice==2:
        change_user_contact_no_hindi()
    elif choice==3:
        change_user_address_hindi()
    else:
        print("एक सही चुनाव करें")

def change_user_contact_no_hindi():
    #5
    i=0
    user_id=input("Enter Id ")
    print("")
    user_pass=input("Enter Password ")
    print("")
    print("Verifying")

    query_user="select * from user where user_id='"+user_id+"';"
    data_user=my_sql_data_fetch(query_user)

    if user_id==data_user.user_id[0] and user_pass==data_user.user_password[0]:
        contact_no=input("Enter unique contact number")
        while i==0:
            for j in data_user["contact_no"]:
                if contact_no==j :
                    print("")
                    print("Contact Number alredy taken")
                    print("")
                    print("Try another Contact Number")
                    print("")
                    contact_no=input("Enter unique Contact Number ")
                else:
                    i=1
        data=my_sql_data_fetch("select * from user;")
        data.loc[data["user_id"]==user_id,["contact_no"]]=contact_no
        my_sql_data_write('user',data,'replace')
        user_menu_hindi()
    else:
        print("")
        print("wrong user or pass please try again")
        change_user_contact_no_hindi()

def change_user_address_hindi():
    #5
    user_id=input("Enter Id ")
    print("")
    user_pass=input("Enter Password ")
    print("")
    print("Verifying")

    query_user="select * from user where user_id='"+user_id+"';"
    data_user=my_sql_data_fetch(query_user)    

    if user_id==data_user.user_id[0] and user_pass==data_user.user_password[0]:
        user_address=input("Enter New Address ")
        user_pincode=input("Enter new Pincode")
        data=my_sql_data_fetch("select * from user;")
        data.loc[data["user_id"]==user_id,["pincode"]]=user_pincode
        my_sql_data_write('user',data,'replace')
        data.loc[data["user_id"]==user_id,["address"]]=user_address
        my_sql_data_write('user',data,'replace')
        user_menu_hindi()
    else:
        print("Wrong User Id or password")
        print("")
        print("Please Try Again")
        change_user_address_hindi()

change_user_contact_no()
