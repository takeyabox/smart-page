import uuid
from flask import Flask, session, request, redirect, url_for, render_template 

app = Flask(__name__, static_folder='.', static_url_path='')

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SESSION_PERMANENT'] = False

@app.route('/')
def index():
    if 'username' not in session:
        print("Guest not found")
        session['username'] = str(uuid.uuid4())
    else:
        print(f"Guest found. {session["username"]}")

    session['visits'] = session.get('visits', 0) + 1

    return render_template('index.html', message=f"こんにちは{session["username"]}.{session["visits"]}回目の訪問じゃな。")

@app.route("/user/<username>")
def show_user_profile(username):
    return "UserName: " + str(username)

@app.route("/post/<int:post_id>")
def show_post(post_id):
    return "Post" + str(post_id)


app.run(port=1313, debug=True)

