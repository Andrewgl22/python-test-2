from flask import render_template,redirect,request,session,flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.magazine import Magazine
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("login.html")

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : pw_hash,
        "confirm_pw": request.form['confirm_pw']
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect("/dashboard")

@app.route('/login', methods=['POST'])
def login():
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect("/dashboard")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/dashboard')
def success():
    if 'user_id' not in session:
        flash("Please log in")
        return redirect('/')
    user = User.get_by_id({"id": session['user_id']})
    magazines = Magazine.get_all()
    return render_template("dashboard.html",user=user,magazines=magazines)

@app.route('/user/account')
def account():
    if 'user_id' not in session:
        flash("Please log in")
        return redirect('/')
    user = User.get_by_id({"id": session['user_id']})
    data = {
        id: session['user_id']
    }
    magazines = Magazine.get_all_w_count(data)
    return render_template("account.html",user=user,magazines=magazines)

@app.route('/user/edit', methods=['POST'])
def update():
    if 'user_id' not in session:
        flash("Please log in")
        return redirect('/')
    if not User.validate_update(request.form):
        return redirect('/user/account')
    User.update(request.form)
    return redirect("/dashboard")

@app.route('/mag/<int:id>/subscribe')
def subscribe(id):
    if 'user_id' not in session:
        flash("Please log in")
        return redirect('/')
    data = {
        "user_id": session['user_id'],
        "magazine_id": id  
    }
    Magazine.subscribe(data)
    return redirect("/dashboard")

