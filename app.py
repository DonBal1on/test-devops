import secrets
import sqlite3
from datetime import datetime
from passlib.hash import sha256_crypt
from forms import createPostForm, signUpForm, loginForm
from flask import Flask, render_template, redirect, flash, request, session


app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)
app.config["SESSION_PERMANENT"] = True


def message(color, message):
    print(
        f'\n\033[94m[{datetime.now().strftime("%d.%m.%y")}\033[0m'
        f'\033[95m {datetime.now().strftime("%H:%M:%S")}]\033[0m'
        f"\033[9{color}m {message}\033[0m\n"
    )


def addPoints(points, userSession):
    conn = sqlite3.connect("db/users.db")
    cur = conn.cursor()
    cur.execute(
        f'UPDATE users set points = points+{points} where userName = "{userSession}"'
    )
    conn.commit()
    message("2", f'{points} POINTS ADDED TO "{userSession}"')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "userName" in session:
        message("1", f'"{session["userName"]}" ALREADY LOGGED IN')
        return redirect("/")
    else:
        form = signUpForm(request.form)
        if request.method == "POST":
            userName = request.form["userName"]
            email = request.form["email"]
            password = request.form["password"]
            passwordConfirm = request.form["passwordConfirm"]
            if passwordConfirm == password:
                password = sha256_crypt.hash(password)
                conn = sqlite3.connect("db/users.db")
                cur = conn.cursor()
                cur.execute(
                    f"""
                    INSERT INTO  users(userName,email,password,role,points,creationDate,creationTime) 
                    VALUES("{userName}","{email}","{password}","user",0,
                    "{datetime.now().strftime("%d.%m.%y")}",
                    "{datetime.now().strftime("%H:%M")}")
                    """
                )
                conn.commit()
                message("2", f'"{userName}" ADDED TO DATABASE')
                return redirect("/")
            elif passwordConfirm != password:
                message("1", " PASSWORDS MUST MATCH ")
                flash("password must match", "error")
        return render_template("signup.html", form=form, hideSignUp=True)


@app.route("/login", methods=["GET", "POST"])
def login():
    if "userName" in session:
        message("1", f'"{session["userName"]}" ALREADY LOGGED IN')
        return redirect("/")
    else:
        form = loginForm(request.form)
        if request.method == "POST":
            userName = request.form["userName"]
            password = request.form["password"]
            conn = sqlite3.connect("db/users.db")
            cur = conn.cursor()
            cur.execute(f'SELECT * from users WHERE userName = "{userName}"')
            user = cur.fetchone()
            if not user:
                message("1", f'"{userName}" NOT FOUND')
                flash("user not found", "error")
            else:
                if sha256_crypt.verify(password, user[3]):
                    session["userName"] = userName
                    # addPoints(1, session["userName"])
                    message("2", f'"{userName}" LOGGED IN')
                    flash("user found", "success")
                    return redirect("/")
                else:
                    message("1", "WRONG PASSWORD")
                    flash("wrong  password", "error")
        return render_template("login.html", form=form, hideLogin=True)


@app.route("/logout")
def logout():
    if "userName" in session:
        message("2", f'"{session["userName"]}" LOGGED OUT')
        session.clear()
        return redirect("/")
    else:
        message("1", f"USER NOT LOGGED IN")
        return redirect("/")


@app.route("/createpost", methods=["GET", "POST"])
def createPost():
    if "userName" in session:
        form = createPostForm(request.form)
        if request.method == "POST":
            postTitle = request.form["postTitle"]
            postTags = request.form["postTags"]
            postContent = request.form["postContent"]
            conn = sqlite3.connect("db/posts.db")
            cur = conn.cursor()
            cur.execute(
                f"""
                INSERT INTO posts(title,tags,content,author,views,date,time) 
                VALUES("{postTitle}","{postTags}","{postContent}",
                "{session["userName"]}",0,
                "{datetime.now().strftime("%d.%m.%y")}",
                "{datetime.now().strftime("%H:%M")}")
                """
            )
            conn.commit()
            message("2", f"'{postTitle}' POSTED")
            addPoints(10, session["userName"])
            return redirect("/")
        return render_template("createPost.html", form=form)
    else:
        message("1", "USER NOT LOGGED IN")
        flash("you need login for create a post", "error")
        return redirect("/login")


@app.route("/<postID>", methods=["GET", "POST"])
def post(postID):
    conn = sqlite3.connect("db/posts.db")
    cur = conn.cursor()
    cur.execute(f"SELECT id from posts")
    posts = str(cur.fetchall())
    if postID in posts:
        message("2", f'"{postID}" FOUND')
        conn = sqlite3.connect("db/posts.db")
        cur = conn.cursor()
        cur.execute(f'SELECT * from posts WHERE id = "{postID}"')
        post = cur.fetchone()
        return render_template(
            "post.html",
            id=post[0],
            title=post[1],
            tags=post[2],
            content=post[3],
            views=post[4],
            author=post[5],
            date=post[6],
        )
    else:
        message("1", "404")
        return render_template("404.html", notFound=postID)


if __name__ == "__main__":
    app.run(debug=True)
