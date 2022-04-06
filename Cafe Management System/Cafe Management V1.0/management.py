import pandas as pd
import numpy as np
import mysql.connector as sqltor
import pymysql
from datetime import date
from datetime import timedelta
from sqlalchemy import create_engine

def my_sql_management_fetch():
    myconn=sqltor.connect(host="localhost",user="root",passwd="root",database="cafe") 
    if myconn.is_connected():
        database_data=pd.read_sql("select * from management;",myconn)
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

def my_sql_items_fetch():
    myconn=sqltor.connect(host="localhost",user="root",passwd="root",database="cafe") 
    if myconn.is_connected():
        database_data=pd.read_sql("select * from items;",myconn)
    return database_data

def my_sql_orders_fetch(query):
    empty=0
    myconn=sqltor.connect(host="localhost",user="root",passwd="root",database="cafe") 
    if myconn.is_connected():
        database_data=pd.read_sql(query,myconn)
        if database_data.empty==True:
            database_data.loc["No Orders",:]=""
            empty=1
    return database_data,empty

def main_menu():
    #1
    print("1.Enter 1 for English")
    print("2.Enter 2 for Hindi")
    choice=int(input("Please select language "))
    if choice==1:
        management_login_eng()
    elif choice==2:
        management_login_hindi()
    else:
        print("Please make a Valid Choice")
        main_menu()


##ENGLISH MENU

def management_login_eng():
    #3
    print("1.For changing password enter 1")
    print("")
    print("2.For login enter 2")
    print("")
    print("3.To return to previous menu enter 3")
    print("")
    choice=int(input("Enter Choice "))
    if choice==1:
        change_pass_management()
    elif choice==2:
        manage_id=input("Enter Id ")
        manage_pass=input("Enter Password ")
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
            print("")
            print("Verification Sucessfull")
            management_menu()
        else:
            print("")
            print("wrong user or pass please try again")
            management_login_eng()
    elif choice==3:
        main_menu()
    else:
        print("Please make a valid choice")
        management_login_eng()
    
def change_pass_management():
    #4
    manage_id=input("Enter Id ")
    print("")
    manage_phone=input("Enter Registered Phone No.")
    print("")
    print("Verifying")
    data=my_sql_management_fetch()
    index=[]
    sucess=0
    for i in data.index:
        index.append(i)
    for j in index:
        if manage_id==data.management_id[j] and manage_phone==data.contact_no[j]:
            sucess=1
            break
        else:
            continue
    if sucess==1:
        print("")
        print("Verification Successful")
        new_pass=input("Enter new password")
        data.loc[data["management_id"]==manage_id,["password"]]=new_pass
        my_sql_data_write('management',data,'replace')
        management_login_eng()
    else:
        print("")
        print("Couldnt Verify Please Try again")
        change_pass_management()
    
def management_menu():
    ##4
    orders,empty=my_sql_orders_fetch("select * from orders")
    if empty==0:
        index_del=[]
        index=0
        for i in orders["order_date"]:
            if i==date.today() - timedelta(days = 2):
                index_del.append(index)
            index+=1
        for j in index_del:
            orders = orders.drop(j)
        my_sql_data_write("orders",orders,"replace")
    
    print("1.For updating items enter 1")
    print("")
    print("2.For removing items enter 2")
    print("")
    print("3.For adding item enter 3")
    print("")
    print("4.For Billing enter 4")
    print("")
    print("5.For setting status to completed enter 5")
    print("")
    print("6.For yesterday's sale enter 6")
    print("")
    choice=int(input("Enter your choice "))
    if choice==1:
        update_item()
    elif choice==2:
        remove_item()
    elif choice==3:
        add_item()
    elif choice==4:
        billing()
    elif choice==5:
        set_completed()
    elif choice==6:
        yesterday_sale()
    else:
        print("")
        print("Make a correct choice")
        management_menu()

def update_item():
    #5
    items=my_sql_items_fetch()
    print(items)
    print("")
    choice=int(input("Enter item index to update items "))
    u_item_name=input("Enter updated name ")
    u_item_price=input("Enter updated price ")
    items.loc[choice:choice,"name":"price"]=u_item_name,u_item_price
    print("Please verify change")
    print(items)
    print("1.Enter 1 to confirm")
    print("")
    print("2.Enter 2 to make changes")
    print("")
    choice=int(input("Make a choice "))
    if choice==1:
        my_sql_data_write('items',items,'replace')
        management_menu()
    elif choice==2:
        update_item()
    
def remove_item():
    #5
    items=my_sql_items_fetch()
    print(items)
    choice=int(input("Enter item index to remove items "))
    items=items.drop(choice)
    print("Please verify change")
    print("")
    print(items)
    print("")
    print("1.Enter 1 to confirm")
    print("")
    print("2.Enter 2 to make changes")
    print("")
    choice=int(input("Make a choice "))
    
    if choice==1:
        my_sql_data_write('items',items,'replace')
        management_menu()
    elif choice==2:
        remove_item()

def add_item():
    #5
    n_item_name=input("Enter item name ")
    n_item_price=input("Enter item price ")
    items={"name":n_item_name,"price":n_item_price}
    items=pd.DataFrame(items,index=[0])
    print("Please view change")
    print("")
    print(items)
    print("")
    print("1.Enter 1 to confirm")
    print("")
    print("2.Enter 2 to make changes")
    print("")
    choice=int(input("Make a choice "))
    if choice==1:
        my_sql_data_write('items',items,'append')
        management_menu()
    elif choice==2:
        add_item()

def billing():
    #5
    items=my_sql_items_fetch()
    print(items)
    i="0"
    selected_index_s=[]
    selected_index_i=[]
    item_names=""
    total_items=0
    total_price=0
    print("Enter / to generate bill")
    while i=="0":
        choice=input("Enter index of item to bill ")
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
        total_price=total_price+int(k)
    total={"name":str(total_items),"price":str(total_price)}
    bill.loc["Total",:]=total
    print(bill)
    print("1.Enter 1 to confirm order")
    print("")
    print("2.Enter 2 to change")
    print("")
    choice=int(input("Make a choice "))
    if choice==1:
        bill_np_array=bill.values
        for l in range(0,len(bill_np_array)-1):
            item_names+=bill_np_array[l][0]+','
        date_today=date.today()
        order={"user_id":"Management Person","items":item_names,"total_price":total_price,"address":"At Cafe","order_date":date_today,"status":"pending"}
        order=pd.DataFrame(order,index=[0])
        my_sql_data_write("orders",order,"append")
        management_menu()
    elif choice==2:
        billing()
    else:
        print("Wrong Choice")
        billing()
    

def set_completed():
    ##5
    orders,empty=my_sql_orders_fetch("select * from orders where status='pending';")
    
    if empty==0:
        print(orders)
        print("")
        choice=int(input("Enter index to set order as complete "))
        orders.loc[choice:choice,"status":"status"]="completed"
        print("Please verify change")
        print("")
        print(orders)
        print("")
        print("1.Enter 1 to confirm")
        print("")
        print("2.Enter 2 to make changes")
        print("")
        choice=int(input("Make a choice "))
    
        if choice==1:
            my_sql_data_write('orders',orders,'replace')
            management_menu()
        elif choice==2:
            set_completed()
    else:
        print("No Orders")

def yesterday_sale():
    #5
    total_price=0
    total_orders=0
    yesterday_date=date.today() - timedelta(days = 1)
    query="select * from orders where status='completed' and order_date=" +"'" + str(yesterday_date) +"'" + ";"
    orders,empty=my_sql_orders_fetch(query)
    if empty==1:
        print("No Orders")
    else:
        for i in orders["total_price"]:
            total_orders+=1
            total_price += int(i)
        orders.loc["Total",:]="Not Applicable",total_orders,total_price,"Not Applicable","Not Applicable","Not Applicable"
        print(orders)
    management_menu()
    

##HINDI MENU

def management_login_hindi():
    #3
    print("1.पासवर्ड बदलने के लिए 1 दर्ज करें")
    print("")
    print("2.प्रवेश के लिए 2 दर्ज करें")
    print("")
    print("3.पिछले मेनू पर लौटने के लिए 3 दर्ज करें")
    print("")
    choice=int(input("अपनी पसंद दर्ज करें "))
    if choice==1:
        change_pass_management_hindi()
    elif choice==2:
        manage_id=input("आईडी दर्ज करें ")
        print("")
        manage_pass=input("पासवर्ड दर्ज करें ")
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
            print("सत्यापन सफल")
            management_menu_hindi()
        else:
            print("गलत उपयोगकर्ता या पासवर्ड कृपया पुनः प्रयास करें")
            management_login_hindi()
    elif choice==3:
        main_menu()
    else:
        print("कृपया एक वैध विकल्प बनाएं")
        management_menu_hindi()
    
def change_pass_management_hindi():
    #4
    manage_id=input("आईडी दर्ज करें ")
    print("")
    manage_phone=input("पंजीकृत फोन नंबर दर्ज करें ")
    print("")
    print("सत्यापन")
    data=my_sql_management_fetch()
    index=[]
    sucess=0
    for i in data.index:
        index.append(i)
    for j in index:
        if manage_id==data.management_id[j] and manage_phone==data.contact_no[j]:
            sucess=1
            break
        else:
            continue
    if sucess==1:
        print("सत्यापन सफल")
        print("")
        new_pass=input("नया पासवर्ड दर्ज करें")
        data.loc[data["management_id"]==manage_id,["password"]]=new_pass
        my_sql_data_write('management',data,'replace')
        management_login_hindi()
    else:
        print("")
        print("कृपया सत्यापित करें फिर से प्रयास करें")
        change_pass_management_hindi()
    
def management_menu_hindi():
    #4
    orders,empty=my_sql_orders_fetch("select * from orders")
    if empty==0:
        index_del=[]
        index=0
        for i in orders["order_date"]:
            if i==date.today() - timedelta(days = 2):
                index_del.append(index)
            index+=1
        for j in index_del:
            orders = orders.drop(j)
        my_sql_data_write("orders",orders,"replace")

    print("1.अद्यतन करने के लिए आइटम 1 दर्ज करें")
    print("")
    print("2.आइटम हटाने के लिए 2 दर्ज करें")
    print("")
    print("3.आइटम जोड़ने के लिए 3 दर्ज करें")
    print("")
    print("4.बिलिंग के लिए 4 दर्ज करें")
    print("")
    print("5.पूर्ण स्थिति दर्ज करने के लिए 5 दर्ज करें")
    print("")
    print("6.कल की बिक्री के लिए 6 दर्ज करें")
    print("")
    choice=int(input("अपनी पसंद दर्ज करें "))
    if choice==1:
        update_item_hindi()
    elif choice==2:
        remove_item_hindi()
    elif choice==3:
        add_item()
    elif choice==4:
        billing_hindi()
    elif choice==5:
        set_completed_hindi()
    elif choice==6:
        yesterday_sale_hindi()
    else:
        print("एक सही चुनाव करें")
        management_menu_hindi()

def update_item_hindi():
    #5
    items=my_sql_items_fetch()
    print(items)
    choice=int(input("आइटम अपडेट करने के लिए आइटम इंडेक्स डालें"))
    u_item_name=input("अद्यतन नाम दर्ज करें")
    u_item_price=input("अद्यतन मूल्य दर्ज करें")
    items.loc[choice:choice,"name":"price"]=u_item_name,u_item_price
    print("कृपया बदलाव सत्यापित करें")
    print(items)
    print("1.पुष्टि करने के लिए 1 दर्ज करें")
    print("")
    print("2.परिवर्तन करने के लिए 2 दर्ज करें")
    print("")
    choice=int(input("एक का चयन करो "))
    if choice==1:
        my_sql_data_write('items',items,'replace')
        management_menu_hindi()
    elif choice==2:
        update_item_hindi()
    
def remove_item_hindi():
    #5
    items=my_sql_items_fetch()
    print(items)
    print("")
    choice=int(input("आइटम हटाने के लिए आइटम इंडेक्स डालें "))
    items=items.drop(choice)
    print("")
    print("कृपया बदलाव सत्यापित करें")
    print("")
    print(items)
    print("")
    print("1.पुष्टि करने के लिए 1 दर्ज करें")
    print("")
    print("2.परिवर्तन करने के लिए 2 दर्ज करें")
    print("")
    choice=int(input("एक का चयन करो "))
    if choice==1:
        my_sql_data_write('items',items,'replace')
        management_menu_hindi()
    elif choice==2:
        remove_item_hindi()

def add_item_hindi():
    #5
    n_item_name=input("आइटम नाम दर्ज करें")
    print("")
    n_item_price=input("आइटम मूल्य दर्ज करें")
    print("")
    items={"name":n_item_name,"price":n_item_price}
    items=pd.DataFrame(items,index=[0])
    print("कृपया बदलाव की पुष्टि करें")
    print("")
    print(items)
    print("")
    print("1.पृष्ठ परिवर्तन की पुष्टि करें")
    print("")
    print("2.परिवर्तन करने के लिए 2 दर्ज करें")
    print("")
    choice=int(input("एक का चयन करो"))
    if choice==1:
        my_sql_data_write('items',items,'append')
        management_menu_hindi()
    elif choice==2:
        add_item_hindi()

def billing_hindi():
    #5
    items=my_sql_items_fetch()
    print(items)
    i="0"
    item_names=""
    selected_index_s=[]
    selected_index_i=[]
    total_items=0
    total_price=0
    print("")
    print("बिल जनरेट करने के लिए / दर्ज करें")
    while i=="0":
        print("")
        choice=input("बिल के लिए आइटम का सूचकांक दर्ज करें ")
        if choice!="/":
            selected_index_s.append(choice)
        elif choice=="/":
            i="/"
    for j in selected_index_s:
        selected_index_i.append(int(j))
    index=range(1,len(selected_index_i)+1)
    bill=pd.DataFrame(items.loc[selected_index_i,"name":"price"])
    bill.index=index
    for k in bill["price"]:
        total_items+=1
        total_price=total_price+int(k)
    total={"name":str(total_items),"price":str(total_price)}
    bill.loc["Total",:]=total
    print(bill)
    print("")
    print("1.आदेश की पुष्टि करने के लिए 1 दर्ज करें")
    print("")
    print("2.बदलने के लिए 2 दर्ज करें")
    print("")
    choice=int(input("एक का चयन करो "))
    if choice==1:
        bill_np_array=bill.values
        for l in range(0,len(bill_np_array)-1):
            item_names+=bill_np_array[l][0]+','
        date_today=date.today()
        order={"user_id":"Management Person","items":item_names,"total_price":total_price,"address":"At Cafe","order_date":date_today,"status":"pending"}
        order=pd.DataFrame(order,index=[0])
        my_sql_data_write("orders",order,"append")
        management_menu_hindi()
    elif choice==2:
        billing_hindi()
    else:
        print("")
        print("गलत पंसद")
        billing_hindi()

def set_completed_hindi():
    ##5
    orders,empty=my_sql_orders_fetch("select * from orders where status='pending';")
    
    if empty==0:
        print(orders)
        print("")
        choice=int(input("आदेश को पूर्ण के रूप में सेट करने के लिए अनुक्रमणिका दर्ज करें "))
        orders.loc[choice:choice,"status":"status"]="completed"
        print("कृपया बदलाव सत्यापित करें")
        print("")
        print(orders)
        print("")
        print("1.पुष्टि करने के लिए 1 दर्ज करें")
        print("")
        print("2.परिवर्तन करने के लिए 2 दर्ज करें")
        print("")
        choice=int(input("एक का चयन करो "))
        print("")
        if choice==1:
            my_sql_data_write('orders',orders,'replace')
            management_menu_hindi()
        elif choice==2:
            set_completed_hindi()
    else:
        print("कोई आदेश नहीं")
        print("")

def yesterday_sale_hindi():
    #5
    total_price=0
    total_orders=0
    yesterday_date=date.today() - timedelta(days = 1)
    query="select * from orders where status='completed' and order_date=" +"'" + str(yesterday_date) +"'" + ";"
    orders,empty=my_sql_orders_fetch(query)
    if empty==1:
        print("कोई आदेश नहीं")
    else:
        for i in orders["total_price"]:
            total_orders+=1
            total_price += int(i)
        orders.loc["Total",:]="Not Applicable",total_orders,total_price,"Not Applicable","Not Applicable","Not Applicable"
        print(orders)
    management_menu_hindi()

##MAIN
##main_menu()
