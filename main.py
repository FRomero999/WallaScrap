from flask import Flask, render_template, session, request
import requests
import json
from requests.structures import CaseInsensitiveDict
from pyjsonq import JsonQ
import os

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'
max_page = 10
keywords=None

@app.before_request
def before_request_func():
    return

@app.route('/', methods=['GET', 'POST'])
def main():

    if "keywords" in session:
        keywords = session["keywords"];
    else:
        keywords = ["playmobil+medieval"]
        session["keywords"] = keywords

    if request.method == 'POST':
        print(request.form)
        keywords=(request.form['keyword'].split(","))
        session["keywords"]=keywords

    return render_template('index.html', listado=",".join(keywords), keywords=keywords)


@app.route('/results')
def results():

    max_page = 10
    resultados = [];

    if "keywords" in session:
        keywords = session["keywords"];
    else:
        keywords = ["playmobil+medieval"]
        session["keywords"] = keywords

    for keyword in keywords:
        print(keyword)
        for page in range(0,max_page):
            url = "https://api.wallapop.com/api/v3/general/search?country_code=ES&density_type=20&filters_source=search_box&keywords="
            url = url + keyword +"&language=es_ES&latitude=36.71847&longitude=-4.41965&order=closest&search_id=a5e5f67b-a5c3-4f0d-ab94-d7203d7f09fd&start="
            url = url + str(40*page) + "&step=7&user_city=M%C3%A1laga&user_province=M%C3%A1laga"
            headers = CaseInsensitiveDict()
            headers["Accept"] = "application/json"

            resp = requests.get(url, headers=headers)
            data = json.loads(resp.text)

            productos = len(data["search_objects"])
            print("    pagina "+str(page) +": "+str(productos))

            resultados = resultados + data["search_objects"]

            if productos<30:
                break

    q=JsonQ(data=resultados)
    salida=q.sort_by('price').get()

    return render_template('results.html', data=salida, cantidad=len(salida), cantidad_claves=len(keywords))


port = int(os.environ.get('PORT', 5000))
server=app.run(host="localhost", port=port)