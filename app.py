import requests

from simpleeval import simple_eval
from flask import Flask, request, Response


app = Flask(__name__)

@app.route("/")
def respond():
    args = request.args
    result = "undefined value"
    if len(args) != 1:
        return Response(f'<result>{result}</result>', mimetype='application/xml', status=200)

    keys = args.keys()
    if 'queryAirportTemp' in keys:
        result = queryAirportTemp(args.get('queryAirportTemp'))
    elif 'queryStockPrice' in keys:
        result = queryStock(args.get('queryStockPrice'))
    elif 'queryEval' in keys:
        result = queryEval(args.get('queryEval'))
    
    return Response(f'<result>{result}</result>', mimetype='application/xml', status=200)


def queryAirportTemp(iata):
    airport_data_url = f" https://www.airport-data.com/api/ap_info.json?iata={iata}"
    response = requests.get(airport_data_url)
    rjson = response.json()
    latitude = rjson['latitude']
    longitude = rjson['longitude']
    print(f"longitude: {longitude}, latitude: {latitude}")
    
    
    temperature_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    response = requests.get(temperature_url)
    rjson = response.json()
    temperature = rjson['current_weather']['temperature']
    print("temperature:", temperature)
    return temperature


def queryStock(param):
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-summary"
    querystring = {"symbol": f"{param}"}
    headers = {
        "X-RapidAPI-Key": '507639d100mshab107bf5d579e59p11cbc7jsn9cec1f47e8e2',
        "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    price = response.json()['price']['regularMarketPrice']['raw']
    return price

def queryEval(param):
    result = simple_eval(param)
    return result

if __name__ == '__main__':
    app.run(debug=True)
