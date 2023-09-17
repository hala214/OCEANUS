
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
    except Exception:
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
    ships_items = db.child("Raspberry Pi Data").child("Ships").get()
    weather_items = db.child("Raspberry Pi Data").child("dht").get()
    ships = []
    weather_data = []
    allowed_ships = ["Passenger Ship", "Naval Ship", "Navile Ship",]
    not_allowed = [ "Container Ship","Fishing Ship" ]
    allowed_not = ["container", "fishing",]
    allowed = ["passenger", "navy"]


    for i in ships_items.each():
        # print(i.val())
        ship_item = i.val()
        ship_name = ship_item["name"].capitalize()
        ship_timestamp = ship_item["timestamp"]
        ship_timestamp = str(datetime.fromtimestamp(ship_timestamp))
        date_object = datetime.strptime(ship_timestamp, "%Y-%m-%d %H:%M:%S.%f")
        formatted_date = date_object.strftime(
            "Date: %Y-%m-%d / Time: %H:%M:%S.%f")[:-4]
        ships.append({"name": f"{ship_name} Ship", "time": formatted_date})


    for i in weather_items.each():
        weather_item = i.val()
        humidity = weather_item["humidity"]
        temperature = weather_item["temperature"]
        weather_timestamp = weather_item["timestamp"]
        weather_timestamp = str(datetime.fromtimestamp(weather_timestamp))
        date_object = datetime.strptime(
            weather_timestamp, "%Y-%m-%d %H:%M:%S.%f")
        formatted_date = date_object.strftime(
            "Date: %Y-%m-%d / Time: %H:%M:%S.%f")[:-4]
        weather_data.append({"humidity": humidity,
                             "temperature": temperature,
                             "time": formatted_date})


    return render_template("table.html", dhts=weather_data[-20:], not_allowed=not_allowed, allowed_ships=allowed_ships, ships=ships[-20:])




@app.route("/all_ships")
def all_ships_table():
    i = 0
    firebase_items = db.child("Raspberry Pi Data").child("Ships").get()
    ships = []
    allowed_ships = ["Passenger Ship", "Naval Ship", "Navile Ship",]
    not_allowed = [ "Container Ship","Fishing Ship" ]
    allowed_not = ["container", "fishing",]
    allowed = ["passenger", "navy"]



   
    for i in firebase_items.each():
        if  firebase_items in allowed or allowed_not :
            print(i.val())
        ship_item = i.val()
        ship_name = ship_item["name"].capitalize()
        ship_timestamp = ship_item["timestamp"]
        ship_timestamp = str(datetime.fromtimestamp(ship_timestamp))
        date_object = datetime.strptime(ship_timestamp, "%Y-%m-%d %H:%M:%S.%f")
        formatted_date = date_object.strftime(
            "Date: %Y-%m-%d / Time: %H:%M:%S.%f")[:-4]
        ships.append({"name": f"{ship_name} Ship", "time": formatted_date})


    return render_template("allships.html", ships=ships[:], not_allowed=not_allowed, allowed_ships=allowed_ships, allowd=allowed, allowed_not=allowed_not)




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

