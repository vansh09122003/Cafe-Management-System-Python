import pandas as pd
import numpy as np
import mysql.connector as sqltor
import pymysql
from datetime import date
from sqlalchemy import create_engine

def my_sql_user_fetch():
    myconn=sqltor.connect(host="localhost",user="root",passwd="root",database="cafe") 
    if myconn.is_connected():
        database_data=pd.read_sql("select * from user",myconn)
    return database_data

def my_sql_data_write(table,value,type_r_a):
    engine=create_engine('mysql+pymysql://root:root@localhost/cafe') 
    myconn=engine.connect()
    try:
        value.to_sql(name=table,con=myconn,index=False,if_exists=type_r_a)
        print("Success")
    except ValueError as e:
        print(e)
    except Exception as e1:
        print(e1)


def my_sql_items_fetch():
    myconn=sqltor.connect(host="localhost",user="root",passwd="root",database="cafe") 
    if myconn.is_connected():
        database_data=pd.read_sql("select * from items;",myconn)
    return database_data

def main_menu():
    #1
    print("1.Enter 1 for English")
    print("")
    print("2.Enter 2 for Hindi")
    print("")
    choice=int(input("Please select language "))
    print("")
    if choice==1:
        print()
        user_login_eng()
    elif choice==2:
        print()
        user_login_hindi()
    else:
        print("Please make a Valid Choice")
        main_menu()

def user_login_eng():
    #3
    print("1.To sign up enter 1")
    print("")
    print("2.To login enter 2")
    print("")
    print("3.To change Password enter 3")
    print("")
    print("4.To return to previous menu enter 4")
    print("")
    choice=int(input("Enter choice "))
    if choice==1:
        user_sign_up()
    elif choice==2:
        user_id=input("Enter Id ")
        print("")
        user_pass=input("Enter Password ")
        print("")
        print("Verifying")
        data=my_sql_user_fetch()
        index=[]
        sucess=0
        for i in data.index:
            index.append(i)
        for j in index:
            if user_id==data.user_id[j] and user_pass==data.user_password[j]:
                sucess=1
                break
            else:
                continue
        if sucess==1:
            print("Verification Sucessful")
            user_menu()
        else:
            print("Wrong Id or Password")
            print("")
            print("Please try again")
            print("")
            user_login_eng()
    elif choice==3:
        change_pass_user()
    elif choice==4:
        main_menu()
        print()
    else:
        print("Please make a valid choice")
        user_login_eng()

def user_sign_up():
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
        user_login_eng()
    elif choice==2:
        user_id=input("Enter unique User Id ")
        data=my_sql_user_fetch()
        while i==0:
            for j in data["user_id"]:
                if user_id==j:
                    print("")
                    print("Username alredy taken")
                    print("")
                    print("Try another user name")
                    print("")
                    user_id=input("Enter unique User Id ")
                elif user_id!=j:
                    i=1
        user_pass=input("Enter Password ")
        print("")
        user_contact_no=input("Enter Mobile Number ")
        i=0
        while i==0:
            for j in data["contact_no"]:
                if user_contact_no==j:
                    print("Contact Number already in use")
                    print("")
                    print("Try changing password or try another contact number")
                    print("")
                    user_contact_no=input("Enter Unique User Id ")
                elif user_contact_no!=j:
                    i=1
        user_address=input("Enter Address ")
        print("")
        user_pincode=input("Enter Pincode ")
        print("")
        data={"user_id":user_id,"user_password":user_pass,"contact_no":user_contact_no,"address":user_address,"pincode":user_pincode}
        data=pd.DataFrame(data,index=[0])
        my_sql_data_write("user",data,"append")
        user_login_eng()

def change_pass_user():
    #4
    user_id=input("Enter Id ")
    print("")
    user_phone=input("Enter Registered Phone No. ")
    print("")
    print("Verifying")
    print("")
    data=my_sql_user_fetch()
    index=[]
    sucess=0
    for i in data.index:
        index.append(i)
    for j in index:
        if user_phone==data.contact_no[j] and user_id==data.user_id[j]:
            sucess=1
            break
        else:
            continue
    if sucess==1:
        print("verification Successful")
        print("")
        new_pass=input("Enter New Password ")
        print("")
        data.loc[data["user_id"]==user_id,["user_password"]]=new_pass
        my_sql_data_write('user',data,'replace')
        user_login_eng()
    else:
        print("Couldnt Verify Please Try again")
        change_pass_user()

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
    items=my_sql_items_fetch()
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
        print(k)
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
        data=my_sql_user_fetch()
        index=[]
        sucess=0
        for i in data.index:
            index.append(i)
        for j in index:
            if user_id==data.user_id[j] and user_password==data.user_password[j]:
                sucess=1
                break
            else:
                continue
        if sucess==1:
            order={"user_id":user_id,"items":item_names,"total_price":total_price,"address":data.address[index],"order_date":date_today,"status":"pending"}
            order=pd.DataFrame(order,index=[0])
            my_sql_data_write("orders",order,"append")
            user_menu()
        else:
            print("Wrong Username or Password")
            print("")
            print("Please Try Again")
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
    user_id=input("Enter Id ")
    print("")
    user_pass=input("Enter Password ")
    print("")
    print("Verifying")
    data=my_sql_user_fetch()
    index=[]
    sucess=0
    for i in data.index:
        index.append(i)
    for j in index:
        if user_id==data.user_id[j] and user_pass==data.user_password[j]:
            sucess=1
            break
        else:
            continue
    if sucess==1:
        user_contact_no=input("Enter New contact number ")
        print("")
        i=0
        while i==0:
            for j in data["contact_no"]:
                if user_contact_no==j:
                    print("Contact Number already in use")
                    print("")
                    print("Try Another Contact number")
                    print("")
                    user_contact_no=input("Enter Unique Conatct numver ")
                elif user_contact_no!=j:
                    i=1
        data.loc[data["user_id"]==user_id,["contact_no"]]=user_contact_no
        my_sql_data_write('user',data,'replace')
        user_menu()
    else:
        print("Wrong User id or password")
        print("")
        print("Please Try Again")
        change_user_contact_no()

def change_user_address():
    #5
    user_id=input("Enter Id ")
    print("")
    user_pass=input("Enter Password ")
    print("")
    print("Verifying")
    data=my_sql_user_fetch()
    index=[]
    sucess=0
    for i in data.index:
        index.append(i)
    for j in index:
        if user_id==data.user_id[j] and user_pass==data.user_password[j]:
            sucess=1
            break
        else:
            continue
    if sucess==1:
        user_address=input("Enter New Address ")
        data.loc[data["user_id"]==user_id,["address"]]=user_address
        my_sql_data_write('user',data,'replace')
        user_pincode=input("Enter new Pincode")
        data.loc[data["user_id"]==user_id,["pincode"]]=user_pincode
        my_sql_data_write('user',data,'replace')
        user_menu()
    else:
        print("Wrong User Id or password")
        print("")
        print("Please Try Again")
        change_user_address()

##HINDI MENU


def user_login_hindi():
    #3
    print("1.प्रवेश करने के लिए 1 दर्ज करें")
    print("")
    print("2.प्रवेश करने के लिए 2 दर्ज करें")
    print("")
    print("3.पासवर्ड बदलने के लिए 3 दर्ज करें")
    print("")
    print("4.पिछले मेनू पर लौटने के लिए 4 दर्ज करें")
    print("")
    choice=int(input("पसंद दर्ज करें "))
    if choice==1:
        user_sign_up_hindi()
    elif choice==2:
        user_id=input("आईडी दर्ज करें ")
        print("")
        user_pass=input("पास वर्ड दर्ज करें")
        print("")
        print("सत्यापन")
        print("")
        data=my_sql_user_fetch()
        index=[]
        sucess=0
        for i in data.index:
            index.append(i)
        for j in index:
            if user_id==data.user_id[j] and user_pass==data.user_password[j]:
                sucess=1
                break
            else:
                continue
        if sucess==1:
            print("सत्यापन सफल")
            user_menu_hindi()
        else:
            print("गलत आईडी और पासवर्ड")
            print("")
            print("कृपया पुन: प्रयास करें")
            user_login_hindi()
    elif choice==3:
        change_pass_user_hindi()
    elif choice==4:
        main_menu()
        print()
    else:
        print("कृपया एक वैध विकल्प चुनें")
        user_login_hindi()

def user_sign_up_hindi():
    #4
    i=0
    print("यदि आपने एक बार फिर से उपयोग नहीं किया है तो कृपया फोन नंबर का उपयोग न करें")
    print("")
    print("यदि आप पासवर्ड भूल गए हैं तो कृपया पासवर्ड भूल गए विकल्प का उपयोग करें")
    print("")
    print("1.लॉगिन मेनू पर लौटने के लिए 1 दर्ज करें")
    print("")
    print("2.प्रवेश जारी रखने के लिए 2 दर्ज करें")
    print("")
    choice=int(input("अपनी पसंद करें "))
    if choice==1:
        user_login_hindi()
    elif choice==2:
        user_id=input("अद्वितीय उपयोगकर्ता आईडी दर्ज करें ")
        data=my_sql_user_fetch()
        while i==0:
            for j in data["user_id"]:
                if user_id==j:
                    print("उपयोगकर्ता नाम पहले ही लिया जा चुका है")
                    print("")
                    print("किसी अन्य उपयोगकर्ता नाम का प्रयास करें")
                    print("")
                    user_id=input("अद्वितीय उपयोगकर्ता आईडी दर्ज करें ")
                    print("")
                elif user_id!=j:
                    i=1
        user_pass=input("पास वर्ड दर्ज करें ")
        print("")
        user_contact_no=input("मोबाइल नंबर दर्ज करें ")
        i=0
        while i==0:
            for j in data["contact_no"]:
                if user_contact_no==j:
                    print("संपर्क नंबर पहले से उपयोग में है")
                    print("")
                    print("पासवर्ड बदलने का प्रयास करें या किसी अन्य संपर्क नंबर का प्रयास करें")
                    print("")
                    user_contact_no=input("अद्वितीय उपयोगकर्ता आईडी दर्ज करें ")
                    print("")
                elif user_id!=j:
                    i=1
        user_address=input("पता लिखिए ")
        print("")
        user_pincode=input("पिनकोड दर्ज करें ")
        print("")
        data={"user_id":user_id,"user_password":user_pass,"contact_no":user_contact_no,"address":user_address,"pincode":user_pincode}
        data=pd.DataFrame(data,index=[0])
        my_sql_data_write("user",data,"append")
        user_login_hindi()

def change_pass_user_hindi():
    #4
    user_id=input("आईडी दर्ज करें ")
    print("")
    user_phone=input("दर्ज फोन नंबर दर्ज करें ")
    print("")
    print("सत्यापन")
    data=my_sql_user_fetch()
    index=[]
    sucess=0
    for i in data.index:
        index.append(i)
    for j in index:
        if user_phone==data.contact_no[j] and user_id==data.user_id[j]:
            sucess=1
            break
        else:
            continue
    if sucess==1:
        print("सत्यापन सफल रहा")
        print("")
        new_pass=input("नया पासवर्ड दर्ज करें ")
        print("")
        data.loc[data["user_id"]==user_id,["user_password"]]=new_pass
        my_sql_data_write('user',data,'replace')
        user_login_hindi()
    else:
        print("कृपया सत्यापित करें फिर से प्रयास करें")
        change_pass_user_hindi()

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
    items=my_sql_items_fetch()
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
        print(k)
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
        data=my_sql_user_fetch()
        index=[]
        sucess=0
        for i in data.index:
            index.append(i)
        for j in index:
            if user_id==data.user_id[j] and user_password==data.user_password[j]:
                sucess=1
                break
            else:
                continue
        if sucess==1:
            order={"user_id":user_id,"items":item_names,"total_price":total_price,"address":data.address[index],"order_date":date_today,"status":"pending"}
            order=pd.DataFrame(order,index=[0])
            my_sql_data_write("orders",order,"append")
            user_menu_hindi()
        else:
            print("गलत उपयोगकर्ता या पास कृपया पुनः प्रयास करें")
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
    user_id=input("आईडी दर्ज करें ")
    print("")
    user_pass=input("पास वर्ड दर्ज करें ")
    print("")
    print("सत्यापन")
    data=my_sql_user_fetch()
    index=[]
    sucess=0
    for i in data.index:
        index.append(i)
    for j in index:
        if user_id==data.user_id[j] and user_pass==data.user_password[j]:
            sucess=1
            break
        else:
            continue
    if sucess==1:
        user_contact_no=input("Enter new contact number")
        i=0
        while i==0:
            for j in data["contact_no"]:
                if user_contact_no==j:
                    print("संपर्क नंबर पहले से उपयोग में है")
                    print("")
                    print("किसी अन्य संपर्क नंबर का प्रयास करें")
                    print("")
                    user_contact_no=input("अद्वितीय उपयोगकर्ता आईडी दर्ज करें ")
                    print("")
                elif user_id!=j:
                    i=1
        data.loc[data["user_id"]==user_id,["contact_no"]]=user_contact_no
        my_sql_data_write('user',data,'replace')
        user_menu_hindi()
    else:
        print("")
        print("गलत उपयोगकर्ता आईडी या पासवर्ड कृपया पुनः प्रयास करें")
        change_user_contact_no_hindi()

def change_user_address_hindi():
    #5
    user_id=input("आईडी दर्ज करें ")
    print("")
    user_pass=input("पास वर्ड दर्ज करें ")
    print("")
    print("सत्यापन")
    print("")
    data=my_sql_user_fetch()
    index=[]
    sucess=0
    for i in data.index:
        index.append(i)
    for j in index:
        if user_id==data.user_id[j] and user_pass==data.user_password[j]:
            sucess=1
            break
        else:
            continue
    if sucess==1:
        user_address=input("नया पता दर्ज करें ")
        data.loc[data["user_id"]==user_id,["address"]]=user_address
        my_sql_data_write('user',data,'replace')
        user_pincode=input("पिनकोड को दर्ज करें ")
        data.loc[data["user_id"]==user_id,["pincode"]]=user_pincode
        my_sql_data_write('user',data,'replace')
        user_menu_hindi()
    else:
        print("")
        print("गलत यूजर आईडी या पास कृपया पुनः प्रयास करें")
        change_user_address_hindi()


##MAIN
##main_menu()
