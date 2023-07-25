from sqlalchemy import create_engine, text
import os 
from flask import jsonify

 
connection_string= "mysql+pymysql://w9zq4w1r3n8b9pimbtqv:pscale_pw_3sU811I9L3xHRlHkUqFMRPnoYZHjIjkGwyVbyHrFkaP@aws.connect.psdb.cloud/jedidiah?charset=utf8mb4"

engine = create_engine(
  connection_string, 
  connect_args={
    "ssl": {
      "ssl_ca": "/etc/ssl/cert.pem"
    }
  })



def registration(data):
     with engine.connect() as conn:
        query = text("INSERT INTO registration (email, pass, status) VALUES (:email, :password, :status)")

        conn.execute(query, 
                    dict(email=data['email'],
                    password=data['password'],
                    status=1)
                    ) 
        
        
def login_user(data):
    with engine.connect() as conn:
        result = conn.execute(text("select * from registration"))
        
        # users = []
        for row in result.fetchall():
            print(row._mapping)
            
            if row._mapping['email'] == data['email']:
                print('Login User')
            else:
                print('Enter right email')
        return ''
         
            
        
        
             
    
        
        
