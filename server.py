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
    print(people)
    return render_template("index.html", all_people = people)


@app.route("/create", methods=["POST"])
def create():
    is_valid = True		
    if len(request.form['first_name']) < 1:
        is_valid = False 
        flash("Please enter a first name")
    if 'first_name'.isalpha() == True:
        print("All characters are alphabets")
    
    else:
        print("All characters are not alphabets.")

    if len(request.form['last_name']) < 1:
        is_valid = False 
        flash("Please enter a last name")
    if 'last_name'.isalpha() == True:
        print("All characters are alphabets.") 
    else:
        print("All characters are not alphabets.")
    
    if len(request.form['email']) < 2:
        is_valid = False
        flash("Please enter a valid email")
    elif not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Invalid email address!")
    # if (mysql_num_rows)


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
            "pass_hash" : pw_hash
        }
        db = connectToMySQL('registration')
        flash("Successfully added")
        id = db.query_db(query,data)
        # print(id)
        return redirect("/welcome/"+ str(id))
    else:
        return redirect("/")


@app.route("/welcome/<id>")
def welcome(id):
    print(id)
    query = "SELECT * FROM people WHERE id=%(id_num)s;"

    data = {
        "id_num": id
    }
    db = connectToMySQL('registration')
    userData = db.query_db(query, data)

    print(userData)
    return render_template("welcome.html", userData=userData[0])



if __name__ == "__main__":
    app.run(debug=True)
