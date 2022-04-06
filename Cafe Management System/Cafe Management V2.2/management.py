import pandas as pd
import numpy as np
import mysql.connector as sqltor
import pymysql
from datetime import date
from datetime import timedelta
from sqlalchemy import create_engine

def my_sql_data_fetch(query,type_o):
    empty=0
    myconn=sqltor.connect(host="localhost",user="root",passwd="root",database="cafe") 
    if myconn.is_connected():
        database_data=pd.read_sql(query,myconn)
        if database_data.empty==True and type_o=="orders":
            database_data.loc["No Orders",:]=""
            empty=1
        elif database_data.empty==True and type_o=="items":
            database_data.loc["Please add items first",:]=""
            empty=1
    return database_data,empty

def my_sql_data_write(table,value,type_r_a):
    engine=create_engine('mysql+pymysql://root:root@localhost/cafe') 
    myconn=engine.connect()
    try:
        value.to_sql(name=table,con=myconn,index=False,if_exists=type_r_a)
    except ValueError as e:
        print(e)
    except Exception as e1:
        print(e1)

##ENGLISH MENU
        
def management_menu():
    ##4
    orders,empty=my_sql_data_fetch("select * from orders","orders")
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
    items,not_in_use=my_sql_data_fetch("select * from items;","items")
    if not_in_use==0:
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
    else:
        print("Please add items first")
    
def remove_item():
    #5
    items,not_in_use=my_sql_data_fetch("select * from items;","items")
    if not_in_use==0:
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
    else:
        print("Please add items first")

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
    items,not_in_use=my_sql_data_fetch("select * from items","items")
    if not_in_use==0:
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
    else:
        print("Please add items first")
    

def set_completed():
    ##5
    orders,empty=my_sql_data_fetch("select * from orders where status='pending';","orders")
    
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
    orders,empty=my_sql_data_fetch(query,"orders")
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
    
def management_menu_hindi():
    #4
    orders,empty=my_sql_data_fetch("select * from orders","orders")
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
    items,not_in_use=my_sql_data_fetch("select * from items;","items")
    if not_in_use==0:
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
    else:
        print("Please add items first")
def remove_item_hindi():
    #5
    items,not_in_use=my_sql_data_fetch("select * from items;","items")
    if not_in_use==0:
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
    else:
        print("please add items first")

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
    items,not_in_use=my_sql_data_fetch("select * from items;","items")
    if not_in_use==0:
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
    else:
        print("Please add items first")

def set_completed_hindi():
    ##5
    orders,empty=my_sql_data_fetch("select * from orders where status='pending';","orders")
    
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
    orders,empty=my_sql_data_fetch(query,"orders")
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
