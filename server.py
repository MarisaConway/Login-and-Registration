from flask import Flask, render_template, request, redirect, session, flash
from mysqlconn import connectToMySQL
from flask_bcrypt import Bcrypt 
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe'
bcrypt = Bcrypt(app)
@app.route("/")
def index():
    db= connectToMySQL('registration')
    people = db.query_db('SELECT * FROM people;')
    return render_template("index.html", all_people = people)
    



@app.route("/create", methods=["POST"])
def create():
    is_valid = True		
    if len(request.form['first_name']) < 1:
        is_valid = False 
        flash("Please enter a first name")
    elif 'first_name'.isalpha() == True:
        is_valid = False
        flash("All characters are not alphabets")
    
    else:
        print("All characters are alphabets.")

    if len(request.form['last_name']) < 1: 
        is_valid = False 
        flash("Please enter a last name")
    elif 'last_name'.isalpha() == True:  
        is_valid = False
        flash("All characters are not alphabets.") 
    else:
        print("All characters are alphabets.")
    
    if len(request.form['email']) < 2:
        is_valid = False
        flash("Please enter a valid email")
    elif not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Invalid email address!")

        # User.objects.all()
        # User.objects.get(ID=5)
        # if not User.objects.filter(email="asdf"):
    else:
        db = connectToMySQL("registration")
        query = "SELECT email from people WHERE email = %(email)s;"
        data = {
            "email": request.form['email']

        }
        result = db.query_db(query,data)
        print(result)
        if len(result) > 0:
            is_valid = False
            flash("Email already exists!")

    if len(request.form['password']) < 8:
        flash("Please enter a valid password")

    if request.form['c_password'] != request.form['password']:
        is_valid = False
        flash("Password does not match")
    
    if is_valid==True:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])  
        print(pw_hash) 
        query = "INSERT INTO people (first_name, last_name, email, password, created_on, updated_on) VALUES (%(fn)s, %(ln)s, %(email)s, %(pass_hash)s, NOW(), NOW());"
        data = {
            "fn": request.form["first_name"],
            "ln": request.form["last_name"],
            "email": request.form["email"],
            "pass_hash" : pw_hash.decode('utf-8')
        }
        db = connectToMySQL('registration')
        flash("Successfully added")
        userid = db.query_db(query,data)
        # print(id)
        session['userid'] = userid
        return redirect("/welcome")
    else:
        return redirect("/")


@app.route("/login", methods=["POST"])
def login():
    # match = True
    db = connectToMySQL("registration")
    query = "SELECT * from people WHERE email = %(email)s;"
    data = {
        "email": request.form["email"]

    }
    result = db.query_db(query,data)

    print(result)

    if len(result) == 0:
        flash("Email not found, please register!")
        return redirect("/")

    else:
        if bcrypt.check_password_hash(result[0]['password'], request.form['password']) == True:
            session['userid'] = result[0]['id']
            return redirect("/welcome")
        else:
            flash("Password does not match!")
            return redirect("/")
            
@app.route("/welcome")
def welcome():
    if 'userid' not in session:
        flash("you must log in first")
        return redirect("/")

    query = "SELECT * FROM people WHERE id=%(id)s;"
    data = {
        "id": session['userid']
    }
    db = connectToMySQL('registration')
    userData = db.query_db(query, data)
    return render_template("welcome.html", userData=userData[0])

        


@app.route("/logout", methods=["POST"])
def logout():
    query = "SELECT * FROM people WHERE id=%(id)s;"

    data = {
        "id": session['userid']
    }
    db = connectToMySQL('registration')
    userData = db.query_db(query, data)
    
    session.clear()
    return redirect("/")








if __name__ == "__main__":
    app.run(debug=True)



#pull up all the emails in database
#scond query is to find out if the users email is in the database.
#compare password with password in the system