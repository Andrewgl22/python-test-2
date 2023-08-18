from flask import render_template,redirect,request,session,flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.magazine import Magazine
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/new")
def new_mag():
    if 'user_id' not in session:
        flash("Please log in")
        return redirect('/')
    user = User.get_by_id({"id": session['user_id']})
    return render_template("create.html", user=user)

@app.route("/mag/create", methods=['POST'])
def create_mag():
    if 'user_id' not in session:
        flash("Please log in")
        return redirect('/')
    if not Magazine.validate_mag(request.form):
        return redirect('/new')
    data = {
        "title": request.form['title'],
        "description": request.form['description'],
        "creator_id": session['user_id']
    }
    Magazine.save(data)
    return redirect("/dashboard")

@app.route("/show/<int:id>")
def show_mag(id):
    if 'user_id' not in session:
        flash("Please log in")
        return redirect('/')
    data = {
        "id": id
    }
    mag = Magazine.get_one(data)
    return render_template("one_mag.html",mag=mag)

@app.route("/mag/delete/<int:id>")
def delete_mag(id):
    if 'user_id' not in session:
        flash("Please log in")
        return redirect('/')
    data = {
        "id": id
    }
    Magazine.delete(data)
    return redirect("/dashboard")