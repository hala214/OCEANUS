from flask import Flask, render_template
app = Flask(__name__)

project_name = "BlaBla"
ourteam = ["Hala", "Aya", "Zaina"]
@app.route("/")
def home():
    return render_template("index.html", title=project_name, team=ourteam)

if __name__ == '__main__':
   app.run(debug = True)