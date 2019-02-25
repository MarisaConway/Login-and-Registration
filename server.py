from flask import Flask, render_template, request, redirect, session, flash
from mysqlconn import connectToMySQL

app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe'
@app.route("/")
def index():
    mysql= connectToMySQL('registration')
    people = mysql.query_db('SELECT * FROM people;')
    print(people)
    return render_template("index.html", all_people = people)


@app.route("/create", methods=["POST"])
def create():
    is_valid = True		
    if len(request.form['first_name']) < 1:
        is_valid = False 
        flash("Please enter a first name")
    if len(request.form['last_name']) < 1:
        is_valid = False 
        flash("Please enter a last name")
    if len(request.form['email']) < 2:
        is_valid = False
        flash("Please enter a valid email")
    if len(request.form['password']) < 2:
        flash("Please enter a valid password")
    
    if is_valid==True:
        query = "INSERT INTO people (first_name, last_name, email, password, created_on, updated_on) VALUES (%(fn)s, %(ln)s, %(email)s, %(pass)s, NOW(), NOW());"
        data = {
            "fn": request.form["first_name"],
            "ln": request.form["last_name"],
            "email": request.form["email"],
            "pass": request.form["password"]
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
