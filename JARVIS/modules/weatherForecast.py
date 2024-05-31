import requests

# Chave da API do OpenWeatherMap
API_KEY = 'c8baa4d044c089e1989e7b17384f7dfc'

def obter_clima(cidade):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&units=metric'
    print(url)
    res = requests.get(url)
    data = res.json()

    temperatura = data['main']['temp']
    velocidadeDoVento = data['wind']['speed']

    return(f'Para {cidade}, o clima esta com temperatura de {temperatura} graus celsius, com ventos de {velocidadeDoVento} quilometros por hora')
