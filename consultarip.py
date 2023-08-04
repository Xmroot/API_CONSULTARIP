import requests
from flask import Flask, request, jsonify, escape

app = Flask(__name__)
port = 3000

def obter_mais_informacoes(data):
    mais_info = {}
    if 'org' in data:
        mais_info['🏢 As'] = data['org']
        mais_info['💼 ISP'] = data['org']

    if 'city' in data:
        mais_info['📌 Cidade'] = data['city']

    if 'country' in data:
        mais_info['🌍 País'] = data['country']

    if 'countryCode' in data:
        mais_info['🌐 Código do País'] = data['countryCode']

    if 'loc' in data:
        latitude, longitude = data['loc'].split(',')
        mais_info['📍 Latitude'] = latitude
        mais_info['📍 Longitude'] = longitude

        latitude_encoded = escape(latitude)
        longitude_encoded = escape(longitude)

        google_maps_url = f"https://www.google.com.br/maps/place/{latitude_encoded},{longitude_encoded}"
        mais_info['🌐 Google Maps'] = google_maps_url

    if 'hostname' in data:
        mais_info['🏠 Hostname'] = data['hostname']

    if 'region' in data:
        mais_info['🚩 Região'] = data['region']

    if 'regionName' in data:
        mais_info['🏢 Nome da Região'] = data['regionName']

    if 'timezone' in data:
        mais_info['⏰ Fuso Horário'] = data['timezone']

    return mais_info

def formatar_resultado(data):
    formatted_info = ""
    for key, value in data.items():
        formatted_info += f"{key}: {value}\n"
    return formatted_info

def geolocalizar_ip(ip):
    api_url = f'http://ipinfo.io/{ip}/json'
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': 'Erro ao consultar API de geolocalização.'}

@app.route('/')
def index():
    return 'Servidor proxy rodando em http://localhost:' + str(port)

@app.route('/consultar-ip')
def consultar_ip():
    ip = request.args.get('ip')

    if not ip:
        return 'Por favor, forneça um endereço IP válido.', 400

    data = geolocalizar_ip(ip)

    if 'error' in data:
        return 'Erro ao consultar a API. Verifique o console para mais informações.', 500

    if 'bogon' in data and data['bogon']:
        return 'Endereço IP local não é permitido.', 400

    mais_info = obter_mais_informacoes(data)

    formatted_info = formatar_resultado(mais_info)

    return formatted_info, 200

if __name__ == '__main__':
    app.run(port=port)