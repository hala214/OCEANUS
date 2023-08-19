from flask import Flask, render_template, request, redirect
import oceanus_db

app = Flask(__name__)

db = oceanus_db.initialize_db()

def valid_login(email, password):
    auth_service = oceanus_db.intialize_auth()
    try:
        auth_service.sign_in_with_email_and_password(email,password)
        return "succefully login"
    except:
        return "invalid email or password, try again"
@app.route("/")
@app.route("/dashboard")
def dashboard():
    return render_template("index.html")

@app.route("/charts")
def charts():
    return render_template("/chartjs.html")

@app.route("/login", methods=['POST', 'GET'])
def login():
    # error = None
    if request.method == 'POST':
        if valid_login(request.form['exampleInputEmail1'],
                       request.form['exampleInputPassword1']):
            return redirect("/dashboard")
    
    return render_template("login.html")

if __name__ == "__name__":
    app.run(debug=True)
    # app.run()
