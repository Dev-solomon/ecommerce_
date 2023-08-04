from sqlalchemy import create_engine, text   
from flask import *
from datetime import date
from funcs import upload_image

# ----------------------------------------------------------
# Connection string For Cloud connection to Database
# ----------------------------------------------------------
connection_string= "mysql+pymysql://w9zq4w1r3n8b9pimbtqv:pscale_pw_3sU811I9L3xHRlHkUqFMRPnoYZHjIjkGwyVbyHrFkaP@aws.connect.psdb.cloud/jedidiah?charset=utf8mb4"
# ******************************************************
engine = create_engine(
  connection_string, 
  connect_args={
    "ssl": {
      "ssl_ca": "/etc/ssl/cert.pem"
    }
  }) 
# --------------------------------------------------------------
# This is the function to add users and their whole basic info
# --------------------------------------------------------------
def registration(data):
  with engine.connect() as conn:
    query = text("INSERT INTO registration (email, pass, status) VALUES (:email, :password, :status)")

    conn.execute(query, 
                dict(email=data['email'],
                password=data['password'],
                status=1)
                ) 
    print('{} Sucessfully Registered'.format(data['email']))
#------------------------------------------ 
# The login function for users  
# -----------------------------------------
def login_user(data):
  with engine.connect() as conn:
      result = conn.execute(text("select * from registration"))
      
      # users = []
      for row in result.fetchall():  
          if row._mapping['email'] == data['email'] and row._mapping['pass'] == data['password']: 
              return data['email']
          if row._mapping['email'] == 'admin' and row._mapping['pass'] == 'password':
            return 'admin'
      return  ''
# ----------------------------------------------------
# Saving the User Details in Settings
# ----------------------------------------------------
def save_user_settings(data):
  with engine.connect() as conn:
    try: 
      add_settings = conn.execute(text("UPDATE registration SET first_name = :firstname, last_name = :lastname WHERE email = :email"),
                                  dict(firstname = data['firstname'],
                                  lastname = data['lastname'],
                                  email =data['email']))
      if add_settings.rowcount == 0:
        return render_template('my-account.html', pass_message="Usernames Not Updated")
      return render_template('my-account.html', pass_message="Username Updated Successfully")
    except:
      print('nothing done to the database')
# ----------------------------------------------------
#Function to Update the Password of the User
# ---------------------------------------------------- 
def update_user_password(data):
  with engine.connect() as conn:
    try: 
      update_password = conn.execute(text("UPDATE registration SET pass = :password WHERE pass = :check_pass"),
                                  dict(password = data['new_password'],
                                       check_pass = data['cur_password']))
      if update_password.rowcount == 0:
        return render_template('my-account.html', pass_message="Password Not Updated")
      return render_template('my-account.html', pass_message="Password Updated Successfully")
    except:
      print('nothing done to the database')
# --------------------------------------------------------------
# This is the function to  create new products
# --------------------------------------------------------------
def create_new_product(data): 
  with engine.connect() as conn:
    query = text("INSERT INTO products(title, tag, description, category, image, m_name, m_brand, stock, price, discount, orders, date, status) VALUES(:title, :title_tag, :description, :category, :image, :m_name, :m_brand, :stock, :price, :discount, :orders, :date, :status)")
    #  Check if stock field is empty
    if data['stock'] == '':
      stock = 0
    else: 
      stock = int(data['stock'])
    # Check if price field is empty
    if data['price'] == '':
      price= 0
    else: 
      price = int(data['price'])
    # Check if discount field is empty 
    if data['discount'] == '':
      discount = 0
    else: 
      discount= int(data['discount'])
    # Check if orders field is empty 
    if data['orders'] == '':
      orders = 0
    else: 
      orders= int(data['orders'])
    # RUN DATABASE QUERY
    result = conn.execute(query, 
                dict(title = data['title'],
                    title_tag = data['title_tag'],
                    description = data['description'],
                    category = data['category'],
                    image =  upload_image(),
                    m_name = data['m_name'],
                    m_brand = data['m_brand'],
                    stock =   stock,
                    price = price,
                    discount = discount,
                    orders = orders,
                    date = date.today(),
                    status = 1
                    )
                ) 
    if result.rowcount == 0:
      return False
    return True
# ------------------------------------------
# Get the products from database
# ------------------------------------------
def get_products():
  with engine.connect() as conn:
    query = text("SELECT * FROM products")
    
    get_products = conn.execute(query)
    
    if get_products.rowcount == 0:
      print('nothing in database')
      
    products = get_products.fetchall()
    
    return products 