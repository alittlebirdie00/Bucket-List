from flask import Flask, render_template, request, json, current_app
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)
mysql = MySQL()


#MySQL configs
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'alittlebirdie00'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


with app.app_context():
    #create mysql connection
    conn = mysql.connect()
#once connection is made, a cursor is required to query the stored procedure
cursor = conn.cursor()


# When the "Sign Up" button is pressed
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

# Server-side method to interact with MySQL databas
@app.route('/signUp', methods=['POST'])
def signUp():
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    #using the salting module to create the hashed passoword.
    _hashed_password = generate_password_hash(_password)

    if _name and _email and _password:
        return json.dumps({'html':'<span>All fields are good !</span>'})
    else:
        return json.dumps({'html':'<span>Enter all required fields.</span>'})

    #call the stored procedure 'sp_createUser'
    cursor.callproc('sp_createUser', (_name, _email, _hashed_password))

    #if procedure is executed succe, commit the changes and return success message
    data = cursor.fetchall()

    if len(data) is 0:
        conn.commit()
        return json.dumps({'message':'User created successfully !'})
    else:
        return json.dumps({'error':str(data[0])})

# When the "Home" button is pressed
@app.route("/main")
def showHome():
    return render_template('index.html')

# When first loading the site
@app.route("/")
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
