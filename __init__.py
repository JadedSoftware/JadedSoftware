from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta, datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime

app = Flask(__name__)
# Session Setup
app.secret_key = "jadedsoftware"
app.permanent_session_lifetime = timedelta(hours=1)

# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(100))
    address = db.Column("address", db.String(100))
    phone = db.Column("phone", db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email


@app.route("/login", methods=["POST", "GET"])
def login():
    # Create Session
    if request.method == "POST":
        name = request.form["nm"]
        session["user"] = name
        # Get User from DB
        found_user = users.query.filter_by(name=name).first()
        if found_user:
            session["email"] = found_user.email
        else:
            # Add user to DB
            usr = users(name, "")
            db.session.add(usr)
            db.session.commit()
        flash("Login successful")
        return redirect(url_for("user"))
    else:
        # If already logged in send to user page
        if "user" in session:
            flash("Already logged in")
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route("/logout")
def logout():
    # Clear Session Variables
    if "user" in session:
        user_name = session["user"]
        flash(f"{user_name} successfully logged out", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))


@app.route("/user", methods=["POST", "GET"])
def user():
    # Get session or send to login screen
    email = None
    address = None
    phone = None
    if "user" in session:
        user_name = session["user"]
        if request.method == "POST":
            email = request.form["email"]
            address = request.form["address"]
            phone = request.form["phone"]
            session["email"] = email
            # Get User from DB
            found_user = users.query.filter_by(name=user_name).first()
            found_user.email = email
            found_user.address = address
            found_user.phone = phone
            db.session.commit()
            flash("Info was saved")
        else:
            if "email" in session:
                email = session["email"]
                found_user = users.query.filter_by(name=user_name).first()
                address = found_user.address
                phone = found_user.phone
        return render_template("user.html", email=email, address=address, phone=phone)
    else:
        flash("You are not logged in")
        return redirect(url_for("login"))


@app.route("/view_users")
def view_users():
    return render_template("view_users.html", values=users.query.all())

@a
 pp.route("/")
def home():
    return render_template('index.html')


if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
