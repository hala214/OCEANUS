from flask import Flask, render_template, request, redirect
import oceanus_db
import rpi_mock
from datetime import datetime

app = Flask(__name__)

db = oceanus_db.initialize_db()

user_email = None
user_password = None

login_visit = False


def valid_login(email, password):
    global login_visit
    auth_service = oceanus_db.intialize_auth()
    try:
        auth_service.sign_in_with_email_and_password(email, password)
        login_visit = True
        return email, password
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


@app.route("/tables")
def tables():
    i = 0
    firebase_items = db.child("Raspberry Pi Data").child("Ships").get()
    ships = []
    allowed_ships = ["Passenger Ship", "Fishing Ship"]

    # for i in range(10):
    for i in firebase_items.each():
        print(i.val())
        ship_item = i.val()
        ship_name = ship_item["name"].capitalize()
        ship_timestamp = ship_item["timestamp"]
        # print("ship_name", ship_name)
        # print("ship_timestamp", ship_timestamp)
        # ship_name = str(i.val()["name"])
        # name = str(i.val()["name"])
        ship_timestamp = str(datetime.fromtimestamp(ship_timestamp))
        date_object = datetime.strptime(ship_timestamp, "%Y-%m-%d %H:%M:%S.%f")
        formatted_date = date_object.strftime(
            "Date: %Y-%m-%d / Time: %H:%M:%S.%f")[:-4]
        ships.append({"name": f"{ship_name} Ship", "time": formatted_date})

    # print("ships::::", ships[:20])
    return render_template("table.html", ships=ships[:20], allowed_ships=allowed_ships)


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
