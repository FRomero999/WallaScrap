from flask import Flask, render_template
import requests
import json
from requests.structures import CaseInsensitiveDict
from pyjsonq import JsonQ

app = Flask(__name__)

@app.route('/')
def hello_world():

    keywords=["playmovil+medieval",
              "playmobil+medieval",
              "playmobil+knights",
              "playmovil+caballeros",
              "playmobil+castillos",
              "famobil+medieval"
             ]
    max_page = 10
    resultados = [];


    for keyword in keywords:
        for page in range(0,max_page):
            url = "https://api.wallapop.com/api/v3/general/search?country_code=ES&density_type=20&filters_source=search_box&keywords="
            url = url + keyword +"&language=es_ES&latitude=36.71847&longitude=-4.41965&order=closest&search_id=a5e5f67b-a5c3-4f0d-ab94-d7203d7f09fd&start="
            url = url + str(40*page) + "&step=7&user_city=M%C3%A1laga&user_province=M%C3%A1laga"
            headers = CaseInsensitiveDict()
            headers["Accept"] = "application/json"

            resp = requests.get(url, headers=headers)
            data = json.loads(resp.text)

            print("pagina "+str(page))
            productos = len(data["search_objects"])
            print(productos)
            print(url)

            resultados = resultados + data["search_objects"]

            if productos<30:
                break


    q=JsonQ(data=resultados)
    salida=q.sort_by('price').get()

    print(salida)

    return render_template('index.html', data=salida)


app.run(debug=True, port=33507)