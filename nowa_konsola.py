from flask import Flask, render_template, redirect, request, url_for
from subprocess import call

app = Flask(__name__, template_folder="templates")
import nowy_main_w_html
@app.route("/")
def index():
    return render_template("konsola.html")


@app.route("/handle_input", methods=["POST"])
def handle_input():
    choice = request.form['choice']
    #choice = request.form.get("choice")
    if choice == "1":
        return redirect(url_for("trasy_do_realizacji"))
    else:
        return "Incorrect value, please try again."

if __name__ == "__main__":
    app.run(debug=True)
