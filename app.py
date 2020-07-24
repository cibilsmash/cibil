from flask import Flask,render_template,request,session,url_for,redirect

from flask_mysqldb import MySQL

import MySQLdb.cursors



app = Flask(__name__)

app.secret_key = '9486'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Mariaselvam@96'
app.config['MYSQL_DB'] = 'pythonlogin'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])

def index():

    if request.method == 'POST':

        username = request.form['user']

        password = request.form['pass']



        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cur.execute("select * from accounts where username = %s AND password = %s", (username,password))

        account = cur.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']

        return redirect(url_for('home'))

    return render_template('index.html')


@app.route('/pythonlogin/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('index'))


@app.route('/pythonlogin/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page





        return render_template('home.html',username = session['username'])

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/register/', methods=['GET', 'POST'])

def register():


      
      if request.method == 'POST':

          username = request.form['user']

          password = request.form['pass']

          email = request.form['email']
          cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

          cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
          mysql.connection.commit()




      return redirect(url_for('list'))


@app.route('/list/')
def list():

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cur.execute("select * from accounts")

    account = cur.fetchall()

    return render_template("list.html", employess=account)


@app.route('/delete/<int:id>/')

def delete(id):



    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("DELETE FROM accounts WHERE id = %s", (id,))
    mysql.connection.commit()

    return redirect(url_for('list'))


@app.route('/update/', methods=['GET', 'POST'])

def update():
    if request.method == 'POST':

        id = request.form['user_id']

        username = request.form['username']

        password = request.form['password']

        email = request.form['email']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('UPDATE accounts SET username = %s, password = %s, email = %s where id = %s', (username, password, email,id))
        mysql.connection.commit()

        return redirect(url_for('list'))
    else:
        return redirect(url_for('list'))
