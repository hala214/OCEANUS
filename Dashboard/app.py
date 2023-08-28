from flask import Flask, render_template, request, redirect
import oceanus_db

app = Flask(__name__)

db = oceanus_db.initialize_db()

user_email = None
user_password = None

login_visit = False

def valid_login(email, password):
    global login_visit
    auth_service = oceanus_db.intialize_auth()
    try:
        auth_service.sign_in_with_email_and_password(email,password)
        login_visit = True
        return email,password
    except:
        return False

@app.route("/")
@app.route("/dashboard")
def dashboard():
    if login_visit:
        return render_template("index.html", user_data=user_data)
    else:
        return redirect("/login")

@app.route("/charts")
def charts():
    return render_template("chartjs.html")

@app.route("/login", methods=['POST', 'GET'])
def login():
    login_visit = False
    # error = None
    if request.method == 'POST':
        user_email = request.form['exampleInputEmail1']
        user_password = request.form['exampleInputPassword1']
        global user_data
        
        user_data = {"email": user_email}

        if valid_login(user_email, user_password):
            return redirect("/dashboard")
    
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
    # app.run()
