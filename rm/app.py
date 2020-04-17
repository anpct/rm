from flask import Flask, Response, redirect, url_for, request, session, abort, render_template, flash
from flask_login import LoginManager, UserMixin, \
    login_required, login_user, logout_user
from db import *
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from emails import send_email
import h


def send_mail_m():
    send = ()
    cur = get_mails()
    for i in cur:
        send.append([i[0],i[1],i[2]])
    for j in send():
        send_email(j[2],[j[0], j[1]])
    


scheduler = BackgroundScheduler({'apscheduler.timezone': 'Asia/Calcutta'})
scheduler.add_job(send_mail_m, 'cron', hour='0')
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


app = Flask(__name__)

# config
app.config.update(
    DEBUG=True,
    SECRET_KEY='secret_xxx'
)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):

    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = ""

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)


# some protected url
@app.route('/home', methods=["GET", "POST"])
@login_required
def home():
    cur = get_related_rem(session["username"])
    if request.method == 'POST':
        add_rem(request.form["date"], request.form["rem"], session["username"], request.form["email"])
        cur = get_related_rem(session["username"])
        return render_template("main.html", cur=cur)
    else:
        return render_template("main.html", cur=cur)


# somewhere to login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if ck_details(username, password):
            session["username"] = username
            uid = username
            user = User(uid)
            login_user(user)
            return redirect(url_for("home"))
        else:
            return abort(401)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if ck_details(email, password):
            return render_template("index.html")
        else:
            add_user(email, password)
            return render_template("register.html", done=True)
    return render_template("register.html")


@app.route("/delete/<text>")
def delete(text):
    delete_rem(text)
    return redirect(url_for("home"))


# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    session["username"] = None
    logout_user()
    return redirect(url_for("login"))


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return render_template("index.html")



# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return User(userid)


if __name__ == "__main__":
    app.run()