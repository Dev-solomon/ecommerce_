from flask import *
import jwt
from functools import wraps
import os  
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage 
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
  checked_token = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"]) 
  if checked_token['user'] == 'admin':
    resp = make_response(redirect(url_for('admin_dashboard'))) 
    resp.set_cookie('token', str(token))
    return resp
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
    
    try:
      data = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"]) 
      return data
    except:
      return  render_template('login.html', message="oops! something went wrong")
# ------------------------------------------------------------
# Function for Uploading Images
# ------------------------------------------------------------
def upload_image():
  image = request.files['image']
  if image.filename != '':
      image.save(os.path.join('static/upload', secure_filename(image.filename)))
      return image.filename
  return print('didn work')
# -----------------------------------------------
# Function to give Admins accessibility to panel
# -----------------------------------------------
def check_ifadmin(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    url= request.method

    if url == 'GET':
       token = request.cookies.get('token')
       data = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"]) 
       
       if data['user'] != 'admin':
        return render_template('admin/auth-404.html', message="ACCESS DENIED!")
    
    return f(*args, **kwargs)  
  return decorated 