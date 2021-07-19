import pymysql
from flask import Flask, flash, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np

import time
import datetime
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'TIGER'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ashish111@'
app.config['MYSQL_DB'] = 'database1'

mysql = MySQL(app)
ts = time.time()
timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


@app.route('/')
def index():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM customers")

    data1 = cursor.fetchall()

    return render_template('index.html', data=data1)


@app.route('/transaction', methods=['GET', 'POST'])
def make():
    msg = 'Please enter details to be added'
    if request.method == 'POST' and 'cid' in request.form and 'cname' in request.form and 'cemail' in request.form and 'cbal' in request.form:
        user = request.form['cname']
        id = request.form['cid']
        email = request.form['cemail']
        bal = request.form['cbal']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT cname,cid FROM customers WHERE cid=%s", (id,))
        pid = cursor.fetchall()
        return render_template('make.html',value=pid,value1=user,value2=id,value3=email,value4=bal)



@app.route("/transactions", methods=['GET', 'POST'])
def transact():
    id = np.random.randint(0,9000)
    if request.method == 'POST' and 'reciever' in request.form and 'amount' in request.form and 'pname' in request.form and 'pbal' in request.form:
        reciever = request.form['reciever']
        amount = float(request.form['amount'])
        amount1 = float(request.form['amount'])
        sender = request.form['pname']
        scurrbal = float(request.form['pbal'])
        cursor = mysql.connection.cursor()
        sbal = scurrbal - amount
        cursor.execute("SELECT balance FROM customers WHERE cname=%s", (reciever,))
        rcurr_bal = cursor.fetchone()
        rcurrbal = float(rcurr_bal[0])
        rbal = rcurrbal + amount1
        print(rcurrbal)
        print(rbal)
        cursor.execute("SELECT * FROM transactions WHERE sender=%s", (sender,))

        tid = cursor.fetchall()
        if scurrbal >= amount:
            cursor.execute("UPDATE customers SET balance=%s where cname=%s", (rbal, reciever,))
            cursor.execute("UPDATE customers SET balance=%s where cname=%s", (sbal, sender,))
            cursor.execute("INSERT INTO transactions(tid,sender,receiver,amount,currbal) VALUES (%s, %s, %s,%s,%s)",(id, sender, reciever, amount,amount))
            id +=1
            mysql.connection.commit()
        else:
            return "Insufficient Funds!"
        return redirect(url_for('transhis'))
        # return render_template('transact.html',value=tid)


@app.route('/history')
def transhis():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM transactions')
    data1 = cursor.fetchall()
    return render_template('tranhis.html', data=data1)


if __name__ == "__main__":
    app.run(debug=True);
