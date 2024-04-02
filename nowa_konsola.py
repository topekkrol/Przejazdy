from flask import Flask, render_template, request,redirect
from trzeci_etap import dane_o_harmonogramie
from flota import Samochod

app = Flask(__name__, template_folder="templates")
import nowy_main_w_html
@app.route("/")
def index():
    return render_template("konsola.html")

@app.route("/harmonogram_dostaw")
def harmonogram_dostaw():
    return render_template('harmonogram_dostaw.html', harmonogram=dane_o_harmonogramie())

@app.route("/lista_pojazdow")
def lista_pojazdow():
    Samochod.odczytaj_z_pliku_wszystkie()
    return render_template('lista_samochodow.html', flota = Samochod.wyswietl_wszystkie())

@app.route("/dokumentacja")
def dokumentacja():
    return "podziekowania za skorzystanie z strony"

@app.route("/graf")
def graf():
    figma = 'https://www.figma.com/file/K2Yd5XsNd96LrkRdDtk5U2/Untitled?type=design&node-id=0%3A1&mode=design&t=M67qjXyQveTkXIZy-1'
    return redirect(figma)


if __name__ == "__main__":
    app.run(debug=True)
