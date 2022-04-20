from sqllite import *
import random
import pandas as pd
from datetime import date


print('Please select 1 for Admin and 2 for user :')
print('------------------------------------------')
print('1. Admin User')
print('2. Customer')
user_select = input('Please Enter your input :')

def set_admin(username, password):
    """Admin registration"""
    conn = create_db()
    cur = conn.cursor()
    cur.execute("SELECT username,password FROM ADMIN WHERE username=:username AND password=:password",
                {"username": username, 'password': password})
    admin_data = cur.fetchone()
    if admin_data is not None and username == admin_data[0] and password == admin_data[1]:
        print("Account Already Exists")
    else:
        conn.execute("INSERT INTO ADMIN VALUES(?,?)", (username, password))
        conn.commit()
        print('Registration Completed.')


def check_admin(username, password):
    status = ''
    conn = create_db()
    cur = conn.cursor()
    cur.execute("SELECT username,password FROM ADMIN WHERE username=:username AND password=:password",
                {"username": username, 'password': password})
    admin_data = cur.fetchone()
    if admin_data is not None and username == admin_data[0] and password == admin_data[1]:
        status = True
    else:
        status = False
    return status


def check_user(username, password):
    status = ''
    conn = create_db()
    cur = conn.cursor()
    cur.execute("SELECT username,password FROM USERS WHERE username=:username AND password=:password",
                {"username": username, 'password': password})
    user_data = cur.fetchone()
    if user_data is not None and username == user_data[0] and password == user_data[1]:
        status = True

    else:
        status = False
    details = {"status": status,
               "username": user_data[0], "password": user_data[1]}
    return details


def register(username, password):
    """User registration"""
    user = ''
    user_pass = ''
    conn = create_db()
    cur = conn.cursor()
    cur.execute("SELECT username,password FROM USERS WHERE username=:username AND password=:password",
                {"username": username, 'password': password})
    user_data = cur.fetchone()
    if user_data is not None and username == user_data[0] and password == user_data[1]:
        print("Account Already Exists")
    else:
        id = random.randint(1, 100000)
        conn.execute("INSERT INTO USERS VALUES (?,?)", (username, password))
        conn.commit()
        user = username
        user_pass = password
        print('Registration Completed.')
    user_details = {"username": user, "password": user_pass}
    return user_details


def admin_menu():
    choice_view = input('Press 1 to add details:\nPress 2 to view details:\nPress 3 for admin reports:\nYour input: ')
    if choice_view == '1':
        choice = input('Press 1 to add category:\nPress 2 to add products:\nPress 3 to remove products:\nPress 4 to add coupons\nYour input: ')
        if choice == '1':
            add_categories()
        elif choice == '2':
            add_products()
        elif choice == '3':
            remove_products()
        elif choice == '4':
            add_coupons()
        else:
            print('Invalid input')
    elif choice_view == '2':
        choice_data = choice = input('Press 1 to view category:\nPress 2 to view products:\nPress 3 Total number of users:\nYour input: ')
        if choice_data == '1':
            view_categories_admin()
        elif choice_data == '2':
            view_products()
        elif choice_data == '3':
            view_coupons_admin()
    elif choice_view == '3':
        choice_data = choice = input('Press 1 to view all orders:\nPress 2 view month wise products sold:\nPress 3 to viwe all the users:\nPress 4 to view total amount of sell month wise:\nYour input: ')
        if choice_data == '1':
            all_orders()
        elif choice_data == '2':
            month_wise_products()
        elif choice_data == '3':
            total_users()
        elif choice_data == '4':
            total_sells()
    else:
        print('Invalid Input')


def user_menu():
    user_input = input('Press 1 to view category:\nPress 2 to view products:\nPress 3 to view coupons:\nPress 4 to add to cart:\nPress 5 to remove from cart\nPress 6 to view cart\nPress 7 for checkout\nYour input: ')
    if user_input == '1':
        view_categories()
    elif user_input == '2':
        view_all_products()
        print('-------------------------------------------------')
        prod_name = input(
            'Enter product name to view details\nEnter product name: ')
        view_product(prod_name)
    elif user_input == '3':
        view_coupons()
    elif user_input == '4':
        username = user_status["username"]
        password = user_status["password"]
        add_my_cart(username, password)
    elif user_input == '5':
        username = user_status["username"]
        password = user_status["password"]
        remove_from_cart(username, password)
    elif user_input == '6':
        username = user_status["username"]
        password = user_status["password"]
        view_cart(username, password)
    elif user_input == '7':
        username = user_status["username"]
        password = user_status["password"]
        checkout(username, password)
    else:
        print('Invalid input')

def all_orders():
    conn = create_db()
    print(pd.read_sql_query("SELECT * FROM  ORDERS", conn))
    conn.commit()
    admin_menu()

def month_wise_products():
    conn = create_db()
    print(pd.read_sql_query("SELECT count(product_name) As  Products, strftime('%m', purchase_date) As Month from ORDERS group by strftime('%m', purchase_date)", conn))
    conn.commit()
    admin_menu()

def total_sells():
    conn = create_db()
    print(pd.read_sql_query("SELECT total(amount) As  Amount, strftime('%m', purchase_date) As Month from ORDERS group by strftime('%m', purchase_date)", conn))
    conn.commit()
    admin_menu()

def total_users():
    conn = create_db()
    print(pd.read_sql_query("SELECT count(username) as users from USERS", conn))
    conn.commit()
    admin_menu()

def add_categories():
    conn = create_db()
    name = input('Please enter type of categories you want: ')
    name = name.lower()
    id = random.randint(1, 100000)
    conn.execute("INSERT INTO CATEGORIES VALUES (?,?)", (id, name))
    conn.commit()
    print('Categories added successfully')
    print('\n')
    print(pd.read_sql_query("SELECT * FROM  CATEGORIES", conn))
    admin_menu()


def view_categories_admin():
    conn = create_db()
    print(pd.read_sql_query("SELECT * FROM  CATEGORIES", conn))
    conn.commit()
    admin_menu()


def add_products():
    conn = create_db()
    name = input('Please enter product name: ')
    description = input('Please enter product description: ')
    amount = input('Please enter product amount: ')
    product_category = input('Please enter product category name: ')
    cur = conn.cursor()
    cur.execute("SELECT category_id FROM CATEGORIES WHERE name=:name", {
                'name': str(product_category)})
    category_id = cur.fetchone()
    if category_id:
        category_id = category_id[0]
        id = random.randint(1, 100000)
        conn.execute("INSERT INTO PRODUCTS VALUES (?,?,?,?,?)",
                     (id, name, description, amount, int(category_id)))
        conn.commit()
        print('Categories added successfully')
        print('\n')
        print(pd.read_sql_query(
            "SELECT product_name,description,amount from PRODUCTS", conn))
        admin_menu()
    else:
        print('Please enter correct category name')


def view_products():
    conn = create_db()
    print(pd.read_sql_query(
        "SELECT product_name,description,amount from PRODUCTS", conn))
    admin_menu()


def remove_products():
    conn = create_db()
    print(pd.read_sql_query(
        "SELECT product_id,product_name,description,amount from PRODUCTS", conn))
    prod_id = input('Please enter product id: ')
    cur = conn.cursor()
    cur.execute("SELECT product_name FROM PRODUCTS WHERE product_id=:prod_id", {
                'prod_id': int(prod_id)})
    product_id = cur.fetchone()
    if product_id:
        conn.execute("DELETE FROM PRODUCTS WHERE product_id=:prod_id", {
                     'prod_id': int(prod_id)})
        conn.commit()
        print('Product deleted successfully')
        print('\n')
        print(pd.read_sql_query(
            "SELECT product_name,description,amount from PRODUCTS", conn))
        admin_menu()
    else:
        print('Product does not exist')
        admin_menu()


def add_coupons():
    conn = create_db()
    cur = conn.cursor()
    coupon_code = input('Please enter coupon code: ')
    discount = input('Please enter discount')
    id = random.randint(1, 10000000)
    conn.execute("INSERT INTO COUPONS VALUES(?,?,?)",
                 (id, coupon_code, discount))
    conn.commit()
    print('Coupons added successfully')
    print('\n')
    print(pd.read_sql_query("SELECT coupon_code,discount FROM COUPONS", conn))
    admin_menu()


def view_coupons_admin():
    conn = create_db()
    print(pd.read_sql_query("SELECT coupon_code,discount FROM COUPONS", conn))
    admin_menu()


def view_categories():
    """View list of all categories of products"""
    conn = create_db()
    print(pd.read_sql_query("SELECT name FROM CATEGORIES", conn))
    user_menu()


def view_all_products():
    """View product details"""
    conn = create_db()
    cur = conn.cursor()
    cur.execute("SELECT product_name FROM PRODUCTS")
    products = cur.fetchone()
    if products:
        print(pd.read_sql_query(
            "SELECT product_name,description,amount FROM PRODUCTS", conn))
        user_menu()
    else:
        print('No products added on SITE, Visit Again in sometime')
        user_menu()

    conn.commit()


def view_product(product_name):
    """View product details"""
    conn = create_db()
    cur = conn.cursor()
    print(pd.read_sql_query("SELECT product_name,description,amount FROM PRODUCTS WHERE product_name=:product_name",
          conn, params={'product_name': product_name}))
    conn.commit()
    user_menu()


def view_coupons():
    """View list of all Coupons"""
    conn = create_db()
    cur = conn.cursor()
    cur.execute("SELECT coupon_code,discount FROM COUPONS")
    coupons = cur.fetchone()
    if coupons:
        print(pd.read_sql_query("SELECT coupon_code,discount FROM COUPONS", conn))
        user_menu()
    else:
        print('NO coupons available')
        user_menu()
    conn.commit()


def add_my_cart(username, password):
    """
    Add products to your cart
    """
    conn = create_db()
    cur = conn.cursor()
    cur.execute("SELECT username,password FROM USERS WHERE username=:username AND password=:password",
                {"username": username, 'password': password})
    user_name = cur.fetchone()
    if user_name is not None and username == user_name[0] and password == user_name[1]:
        user_name = user_name[0]
        print(pd.read_sql_query(
            "SELECT product_name,description,amount FROM PRODUCTS", conn))
        product_name = input('Enter product name to add: ')
        cur.execute("SELECT amount FROM PRODUCTS WHERE product_name=:product_name", {
                    'product_name': product_name})
        amount = cur.fetchone()
        if amount is not None:
            amount = amount[0]
            id = random.randint(1, 10000000)
            conn.execute("INSERT INTO MYCART VALUES(?,?,?,?)",
                         (id, str(product_name), int(amount), str(user_name)))
            conn.commit()
            print('Your cart:')
            print('\n')
            print(pd.read_sql_query(
                "SELECT product_name,amount FROM MYCART WHERE username=:username", conn,
                params={'username': str(user_name)}))
            user_menu()
        else:
            print('Product not found enter valid product name please')
            user_menu()
    else:
        print('Incorrect Username Or Password')


def view_cart(username, password):
    """
    Add products to your cart
    """
    conn = create_db()
    cur = conn.cursor()
    cur.execute("SELECT username,password FROM USERS WHERE username=:username AND password=:password",
                {"username": username, 'password': password})
    user_name = cur.fetchone()
    if user_name is not None and username == user_name[0] and password == user_name[1]:
        user_name = user_name[0]
        print(pd.read_sql_query(
            "SELECT product_name,amount FROM MYCART WHERE username=:username", conn,
            params={'username': str(user_name)}))
        user_menu()
    else:
        print('Incorrect Username Or Password')

    conn.commit()


def remove_from_cart(username, password):
    """Remove products from cart"""
    conn = create_db()
    cur = conn.cursor()
    cur.execute("SELECT username,password FROM USERS WHERE username=:username AND password=:password",
                {"username": username, 'password': password})
    user_name = cur.fetchone()
    if user_name is not None and username == user_name[0] and password == user_name[1]:
        user_name = user_name[0]
        print('Your cart:')
        print('\n')
        print(pd.read_sql_query(
            "SELECT product_name,amount FROM MYCART WHERE username=:username", conn,
            params={'username': str(user_name)}))
        product_name = input('Enter product name to remove')
        conn.execute("DELETE FROM MYCART WHERE product_name=:product_name COLLATE NOCASE",
                     {'product_name': product_name})
        conn.commit()
        print('Product removed from your cart')
        user_menu()
    else:
        print('Incorrect Username or password')


def checkout(username, password):
    """Buy all products from cart apply coupon if any and checkout"""
    conn = create_db()
    cur = conn.cursor()
    cur.execute("SELECT username,password FROM USERS WHERE username=:username AND password=:password",
                {"username": username, 'password': password})
    user_name = cur.fetchone()
    if user_name is not None and username == user_name[0] and password == user_name[1]:
        user_name = user_name[0]
        cur.execute("SELECT username FROM MYCART WHERE username=:username", {
                    'username': str(user_name)})
        check_cart = cur.fetchone()
        if check_cart:
            print(pd.read_sql_query(
                "SELECT coupon_code,discount FROM COUPONS", conn))
            print('\n')
            apply_coupon = input('Do you wish to apply any coupon yes/no ?: ')
            if apply_coupon.lower() == 'yes':
                coupon_code = input('Enter coupon code: ')
                query = conn.execute("SELECT discount FROM COUPONS WHERE coupon_code=:coupon_code", {
                                     'coupon_code': coupon_code})
                query = query.fetchone()
                print('query ', query)
                if query is not None:
                    coupon_discount = query
                    discount = coupon_discount[0]
                    user_cart = conn.execute(
                        "SELECT SUM(amount) FROM MYCART WHERE username=:username", {'username': user_name})
                    amount = user_cart.fetchone()[0]
                    discount_amount = (amount*discount)/100
                    final_amount = amount-discount_amount
                    print(pd.read_sql_query(
                        "SELECT product_name,amount FROM MYCART WHERE username=:username", conn,
                          params={'username': str(user_name)}))
                    print('')
                    print('\n')
                    print('Total Bill Amount =', amount)
                    print('Discounted Amount =', discount_amount)
                    print('Amount to be paid =', final_amount)
                    cur_prod = conn.cursor()
                    cur_prod.execute(
                        "SELECT product_name, amount FROM MYCART WHERE username=:username", {'username': user_name})
                    prod_data = cur_prod.fetchall()
                    prod_val = list(prod_data)
                    print(prod_val)
                    product_data = ''
                    product_amount = 0
                    for i in prod_data:
                        ord_id = random.randint(1, 100000)
                        today = date.today().strftime('%Y-%m-%d')
                        product_data = i[0]
                        product_amount = (i[1]*discount)/100
                        print(product_data)
                        conn.execute("INSERT INTO ORDERS VALUES (?,?,?,?,?)",(ord_id, product_data, product_amount, username, today))
                    conn.commit()    
                    conn.execute("DELETE  FROM MYCART WHERE username=:username", {
                                 'username': user_name})
                    conn.commit()
                    print('Order Placed')
                    user_menu()
                else:
                    print('Invalid Coupon code')
                    user_menu()
            elif apply_coupon.lower() == 'no':
                user_cart = conn.execute(
                        "SELECT SUM(amount) FROM MYCART WHERE username=:username", {'username': user_name})
                amount = user_cart.fetchone()[0]
                print(pd.read_sql_query(
                        "SELECT product_name,amount FROM MYCART WHERE username=:username", conn,
                        params={'username': str(user_name)}))
                print('')
                print('\n')
                print('Total Bill Amount =', amount)
                cur_prod = conn.cursor()
                cur_prod.execute(
                        "SELECT product_name, amount FROM MYCART WHERE username=:username", {'username': user_name})
                prod_data = cur_prod.fetchall()
                prod_val = list(prod_data)
                print(prod_val)
                product_data = ''
                product_amount = 0
                for i in prod_data:
                    ord_id = random.randint(1, 100000)
                    today = date.today().strftime('%Y-%m-%d')
                    product_data = i[0]
                    product_amount = i[1]
                    conn.execute("INSERT INTO ORDERS VALUES (?,?,?,?,?)",(ord_id, product_data, product_amount, username, today))
                conn.commit()    
                conn.execute("DELETE  FROM MYCART WHERE username=:username", {
                                 'username': user_name})
                conn.commit()
                print('Order Placed')
                user_menu()
            else:
                print('Invalid Input')
                
                


if user_select == '1':
    print('Press 1 for new Admin registration:')
    print('Press 2 if already an Admin user')
    admin_select = input('Please Enter your input :')
    if admin_select == '1':
        admin_username = input('Enter username: ')
        admin_password = input('Enter password: ')
        set_admin(admin_username, admin_password)
        admin_menu()
    elif admin_select == '2':
        print('Please enter username and password.')
        user = input('Username: ')
        password = input('Password: ')
        admin_status = check_admin(user, password)
        if admin_status == True:
            admin_menu()
        else:
            print('Not a valid user')
    else:
        print('Invalid input')

elif user_select == '2':
    print('Welcome')
    print('Press 1 for new registration:')
    print('Press 2 if already  a customer')
    customer_select = input('Please Enter your input :')
    if customer_select == '1':
        customer_username = input('Enter username: ')
        customer_password = input('Enter password: ')
        user_data = register(customer_username, customer_password)
    elif customer_select == '2':
        print('Please enter username and password.')
        user_name = input('Username: ')
        user_password = input('Password: ')
        user_status = check_user(user_name, user_password)
        if user_status["status"] == True:
            user_menu()

        else:
            print('Not a valid user')
    else:
        print('Invalid input')
else:
    print('No a valid input')

