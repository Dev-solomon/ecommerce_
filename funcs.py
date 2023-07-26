from flask import *
import jwt
from functools import wraps
import os 
# -----------------------------------------------
# This is the function for tokens' acccessibility
# -----------------------------------------------
def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token = request.cookies.get('token') 

    if not token:
      return render_template('login.html', message="Sorry! You're Not Authorized")
    
    try:
      data = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"]) 
    except:
      return  render_template('login.html', message="Session Expired! Login")
    
    return f(*args, **kwargs)  
  
  return decorated 
# ------------------------------------
# Function for setting cookies 
# ------------------------------------
def set_cookies(token):
    resp = make_response(redirect(url_for('account_template'))) 
    resp.set_cookie('token', str(token))
    return resp
# --------------------------------------------------
# Function for Deleting cookie and Logging User Out
# --------------------------------------------------
def del_cookies():
    resp = make_response(render_template('login.html')) 
    resp.delete_cookie('token')
    return resp
# ------------------------------------------------------------
# Function for Getting Who the user in on dashboard
# ------------------------------------------------------------
def user_account():
    token = request.cookies.get('token')
    
    if not token:
        return render_template('login.html', message="Sorry! You're Not Authorized")
    
    try:
      data = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"]) 
      return data
    except:
      return  render_template('login.html', message="Session Expired! Login")
  

