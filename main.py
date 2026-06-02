import requests
import os
import datetime
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse


# API_KEY - env variable name
API_KEY = os.getenv("API_KEY")



miasta = {
    "Lublin" : [51.21, 22.55],
    "Warszawa" : [52.22, 21.01],
    "Paryz" : [48.85, 2.35],
    "Nicea" : [43.70, 7.26]
}

print(f"Data uruchomienia: {datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}", flush=True)
print("Autor: Lambert Górski", flush=True)
print("Aplikacja nasłuchuje na portcie 8000", flush=True)



def zwroc_pogode(lat, lon, appid):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    lang = "pl"
    slownik_z_query_parameters = {
        "lat" : lat,
        "lon" : lon,
        "appid" : appid,
        "lang" : lang,
        "units": "metric"
    }
    response = requests.get(base_url, params=slownik_z_query_parameters)
    response_dict = response.json()
    temperatura = response_dict["main"]["temp"]
    wilgotnosc = response_dict["main"]["humidity"]
    cisnienie = response_dict["main"]["pressure"]
    return [temperatura, wilgotnosc, cisnienie]
    

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def strona_glowna():
    return """ <!DOCTYPE html>
    <html lang="pl">
    <head>
        <meta charset="UTF-8">
        <title>Sprwadź aktualną pogodę</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; margin-top: 50px; background-color: #f0f2f5; }
            .box { background: white; padding: 30px; display: inline-block; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
            h1 { color: #1a73e8; }
            select, button { padding: 12px; margin: 10px; border-radius: 8px; border: 1px solid #ddd; font-size: 16px; }
            button { background-color: #1a73e8; color: white; border: none; cursor: pointer; transition: 0.3s; }
            button:hover { background-color: #1557b0; }
            label { display: block; font-weight: bold; margin-top: 10px; }
        </style>
    </head>
    <body>
        <div class="box">
            <h1>Sprawdź pogodę</h1>
            <form action="/kraj" method="get">
                
                <label for="country">Wybierz kraj:</label>
                <select name="country" id="country">
                    <option value="Polska">Polska</option>
                    <option value="Francja">Francja</option>
                </select>

                <br>
                <button type="submit">Pokaż dostępne miasta</button>
            </form>
            </div>
        </div>
    </body>
    </html>"""
   
@app.get("/kraj", response_class=HTMLResponse)
def zwroc_liste_miast(country: str | None = None):
    if country == "Polska":
        return """<!DOCTYPE html>
    <html lang="pl">
    <head>
        <meta charset="UTF-8">
        <title>Sprwadź aktualną pogodę</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; margin-top: 50px; background-color: #f0f2f5; }
            .box { background: white; padding: 30px; display: inline-block; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
            h1 { color: #1a73e8; }
            select, button { padding: 12px; margin: 10px; border-radius: 8px; border: 1px solid #ddd; font-size: 16px; }
            button { background-color: #1a73e8; color: white; border: none; cursor: pointer; transition: 0.3s; }
            button:hover { background-color: #1557b0; }
            label { display: block; font-weight: bold; margin-top: 10px; }
        </style>
    </head>
    <body>
        <div class="box">
            <h1>Sprawdź pogodę</h1>
            <form action="/miasto" method="post">
                <label for="city">Wybierz miasto:</label>
                <select name="city" id="city">
                    <option value="Lublin">Lublin</option>
                    <option value="Warszawa">Warszawa</option>
                </select>

                <br>
                <button type="submit">Wyświelt pogodę</button>
            </form>
            </div>
        </div>
    </body>
    </html>"""

    elif country == "Francja":
        return """<!DOCTYPE html>
    <html lang="pl">
    <head>
        <meta charset="UTF-8">
        <title>Sprwadź aktualną pogodę</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; margin-top: 50px; background-color: #f0f2f5; }
            .box { background: white; padding: 30px; display: inline-block; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
            h1 { color: #1a73e8; }
            select, button { padding: 12px; margin: 10px; border-radius: 8px; border: 1px solid #ddd; font-size: 16px; }
            button { background-color: #1a73e8; color: white; border: none; cursor: pointer; transition: 0.3s; }
            button:hover { background-color: #1557b0; }
            label { display: block; font-weight: bold; margin-top: 10px; }
        </style>
    </head>
    <body>
        <div class="box">
            <h1>Sprawdź pogodę</h1>
            <form action="/miasto" method="post">
                <label for="city">Wybierz miasto:</label>
                <select name="city" id="city">
                    <option value="Paryz">Paryż</option>
                    <option value="Nicea">Nicea</option>
                </select>

                <br>
                <button type="submit">Wyświelt pogodę</button>
            </form>
            </div>
        </div>
    </body>
    </html>"""

    else:
        return strona_glowna()

@app.post("/miasto", response_class=HTMLResponse)
def wygeneruj_pogode(city: str | None = Form(...)):
    if city == None:
        return strona_glowna()
    
    lat = miasta[city][0]
    lon = miasta[city][1]
    pogoda = zwroc_pogode(lat, lon, API_KEY)
    html_head ="""<!DOCTYPE html>
    <html lang="pl">
    <head>
        <meta charset="UTF-8">
        <title>Sprwadź aktualną pogodę</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; margin-top: 50px; background-color: #f0f2f5; }
            .box { background: white; padding: 30px; display: inline-block; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
            h1 { color: #1a73e8; }
            select, button { padding: 12px; margin: 10px; border-radius: 8px; border: 1px solid #ddd; font-size: 16px; }
            button { background-color: #1a73e8; color: white; border: none; cursor: pointer; transition: 0.3s; }
            button:hover { background-color: #1557b0; }
            label { display: block; font-weight: bold; margin-top: 10px; }
        </style>
    </head>

    """
    html_body = f"""<body>
        <div class="box">
            <h1>Pogoda w {city}</h1>
            <br>
            <label>Temperatura: {pogoda[0]}</label>
            <br>
            <label>Wilgotność: {pogoda[1]}</label>
            <br>
            <label>Ciśnienie: {pogoda[2]}</label>
            </div>
            <form action="/" method="get">
                <button type="submit">Powrót na stronę główną</button>
            </form>
        </div>
    </body>
    </html>"""

    return html_head + html_body

