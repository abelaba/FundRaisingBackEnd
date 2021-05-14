import os
import json
import psycopg2
from authPayload import authPayload 
from authResponse import authResponse
DBNAME = "fundme"
DBUSER = "postgres"
DBPASSWORD = "12345"
AUTHSECRET = "keyboardcat"
EXPIRESSECONDS = 3000
def newFund(userId,title,category,description,goal):
    conn = None
    query = 'insert into campaign (userid,\"title\",\"category\", \"description\",goal) values ({},\'{}\',\'{}\',\'{}\',{})'.format(userId,title,category,description,goal)
    try:
        conn = psycopg2.connect("dbname=" + DBNAME + " user=" + DBUSER +" password=" +DBPASSWORD)
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        conn.close()
        return True
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