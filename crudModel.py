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

def getFunds():
    conn = None
    query = "select userid,campaign.id,title,category,description,campaign.balance,goal,approved,email from public.campaign JOIN public.users on campaign.userid=users.id"

    try:
        conn = psycopg2.connect("dbname=" + DBNAME + " user=" + DBUSER +" password=" +DBPASSWORD)
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        result = cur.fetchall()
        amount = len(result)
        response = []
        for r in result:
            
            response.append({
                    "userid":r[0],
                    "id":r[1],
                    "title":r[2],
                    "category":r[3],
                    "description":r[4],
                    "balance":r[5],
                    "goal":r[6],
                    "approved":r[7],
                    "email":r[8]

                })
        
        return json.dumps(response)
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

def deleteFunds(fundId,userId):
    conn=None
    query= "Delete from campaign where id={} and userid={}".format(fundId,userId)
    try:
        conn = psycopg2.connect("dbname=" + DBNAME + " user=" + DBUSER +" password=" +DBPASSWORD)
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        return {"success":True}
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if conn is not None:
            cur.close()
            conn.close()
            return {"success":False}
    finally:
        if conn is not None:
            cur.close()
            conn.close()
def pay(c_id,amount,name,card,expiry,cvv):
    conn = None
 
    query = "select * from ecards where name='{}' and cardnumber ='{}' and expiry ='{}' and cvv ='{}' ".format(name,card,expiry,cvv)
 
    try:
        conn = psycopg2.connect("dbname=" + DBNAME + " user=" + DBUSER +" password=" +DBPASSWORD)
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        result = cur.fetchone()
        if (result == None):
            return "incorrect card details"

        id=result[0]
        query = "select * from bankaccount where id={}".format(id)
        cur = conn.cursor()
        cur.execute(query)
        # conn.commit()
        result = cur.fetchone()
        amnt = result[3]
        if(amnt <  amount):
            return "Insufficient balance"
        getuserId = "select * from campaign where id={}".format(c_id)
        cur =  conn.cursor()
        cur.execute(getuserId)
        # conn.commit()
        res = cur.fetchone()

        if(res == None):
            return "incorrect card details"
        userId = res[0]
        cBalance = res[5] + amount
        getBalance = "select * from users where id={}".format(userId)
        cur =  conn.cursor()
        cur.execute(getBalance)
        # conn.commit()
        res = cur.fetchone()
        if(res==None):
            return "error occured try again"
        balance = int(res[4]) + amount
        query1 = "update users set balance = {} where id={}".format(balance,userId)
        cur =  conn.cursor()
        cur.execute(query1)
        # conn.commit()
        out = int(amnt) - amount
        if (amnt < out):
            return "insufficient Balance"
        query2 = "update bankaccount set amount={} where id={}".format(out,id)
        cur = conn.cursor()
        cur.execute(query2)
        query3 = "update campaign set balance={} where id={}".format(cBalance,c_id)
        cur.execute(query3)
        conn.commit()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if conn is not None:
            cur.close()
            conn.close()
            return "Error detected try again"
    finally:
        if conn is not None:
            cur.close()
            conn.close()

def withdraw(userId,account,amount):
    conn = None
    conn = psycopg2.connect("dbname=" + DBNAME + " user=" + DBUSER +" password=" +DBPASSWORD)
    getAmountUser = "select * from users where id={}".format(userId)
    cur = conn.cursor()
    cur.execute(getAmountUser)
    conn.commit()
    result = cur.fetchone()
    if(len(result)< 1):
        return "not allowed"
    userAmount = result[4]
    getAmountBank = "select * from bankaccount where id={}".format(account)
    cur = conn.cursor()
    cur.execute(getAmountBank)
    conn.commit()
    res = cur.fetchone()
    if(res==None):
        return "bank account not found"
    bankAmount = res[3]
    if(userAmount < amount):
        return "insufficient balace"
    userAmount = userAmount - amount
    if(userAmount<0):
        return "insufficient balance"
    bankAmount = bankAmount  + amount
    updateUser= "update users set balance={} where id={}".format(userAmount,userId)
    cur = conn.cursor()
    cur.execute(updateUser)
    conn.commit()
    updateBank = "update bankaccount set amount={} where id={}".format(bankAmount,account)
    cur = conn.cursor()
    cur.execute(updateBank)
    conn.commit()
    transaction = "insert into transactions (userid,type,accountnumber,amount)values({},'Withdraw',{},{})".format(userId,account,amount)
    cur = conn.cursor()
    cur.execute(transaction)
    conn.commit()
    conn.close()
    return True
def getTransactions(userId):
    conn = None
    conn = psycopg2.connect("dbname=" + DBNAME + " user=" + DBUSER +" password=" +DBPASSWORD)
    query = "select * from transactions where userId={}".format(userId)
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    res = cur.fetchall()
    response = []
    for r in res:
        response.append({
                "userid":r[0],
                "id":r[1],
                "type":r[2],
                "account":r[3],
                "amount":r[4]
            })
    return response

def getBalance(id):
    conn = None
    query = "select * from users where id={}".format(id)
    try:
        conn = psycopg2.connect("dbname=" + DBNAME + " user=" + DBUSER +" password=" +DBPASSWORD)
        cur = conn.cursor()
        cur.execute(query)
        result =  cur.fetchone()
        print(result)
        if(result==None):
            return {"error":"error"}
        return {"balance": result[4]}
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.close()
def decline(id):
    query =  "DELETE FROM campaign where id={}".format(id)
    conn = None
    try:
        conn = psycopg2.connect("dbname=" + DBNAME + " user=" + DBUSER +" password=" +DBPASSWORD)
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        return "campaign declined"
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.close()
        return False
def approve(id):
    query =  "update  campaign set approved={} where id={}".format(True,id)
    conn = None
    try:
        conn = psycopg2.connect("dbname=" + DBNAME + " user=" + DBUSER +" password=" +DBPASSWORD)
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        return "campaign Approved"
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.close()
        return False  