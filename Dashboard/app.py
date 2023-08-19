from flask import Flask, render_template
app = Flask(__name__)

project_name = "OCEANUS"
@app.route("/")

def index():
   return render_template("index.html", title=project_name)

if __name__ == '__main__':
   app.run(debug = True)