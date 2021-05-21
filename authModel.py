import os
import json

# pip install psycopg2
import psycopg2

#pip install -U python-dotenv
from dotenv import load_dotenv
load_dotenv()

# pip install pyjwt
import jwt

from authPayload import authPayload 
from authResponse import authResponse

# Get environment variables
DBNAME = "fundme"
DBUSER = "postgres"
DBPASSWORD = "12345"
AUTHSECRET = "keyboardcat"
EXPIRESSECONDS = 3000

def authenticate(email, password):

    conn = None
    query = "select * from users where \"email\"='" + email + "' and \"password\"='" + password + "'"
    try:
        conn = psycopg2.connect("dbname=" + DBNAME + " user=" + DBUSER +" password=" +DBPASSWORD)
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        
        isAdmin = False

        if cur.rowcount == 1:
            for row in rows:
                payload = authPayload(row[0],row[1],row[5])
                break

            encoded_jwt = jwt.encode(payload.__dict__, AUTHSECRET, algorithm='HS256')
            response = authResponse(encoded_jwt,EXPIRESSECONDS)
            
            return response.__dict__
        else:
            return False
        
    except (Exception, psycopg2.DatabaseError) as error:
        
        print(error)
        if conn is not None:
            cur.close()
            conn.close()

        return False
    finally:
        if conn is not None:
            cur.close()
            conn.close()

def verify(token):
     
    decoded = jwt.decode(token, AUTHSECRET, algorithms=['HS256'])
    return decoded
  

def create(email,username,password):
    conn = None
    query = "insert into users (\"email\", \"username\", \"password\",balance ) values('"+email+"','"+username +"','"+password+"',0)"

    try:
        conn = psycopg2.connect("dbname=" + DBNAME + " user=" + DBUSER +" password=" +DBPASSWORD)
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        
        if conn is not None:
            cur.close()
            conn.close()

        return "Email already exits"
    finally:
        if conn is not None:
            cur.close()
            conn.close()

