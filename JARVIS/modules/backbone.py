import wikipedia
import pywhatkit
import google.generativeai as gemini
import requests

from modules import finance
from modules import listen
from modules import get_env 

def execute_command(comando):
    
    gemini.configure(api_key=get_env.print_env(['GEMINI_KEY'])['GEMINI_KEY'])
    model = gemini.GenerativeModel('gemini-pro')
   

    if 'procure por' in comando:
        resultado = model.generate_content(comando)
        resultado = resultado.text
        resultado = resultado.replace('*','')
        print(resultado)
        return resultado

    elif 'toque' in comando:
        musica = comando.replace('toque','')
        resultado = pywhatkit.playonyt(musica)
        resultado = f'Tocando {musica} no youtube!'
        return resultado
    
    elif 'cotação' in comando or 'cote' in comando or 'qual o valor da ação' in comando:
        symbol = comando.replace('cotação','').replace('cote','').replace('qual o valor da ação','').rstrip().strip().upper()
        try:
            resultado = finance.obter_cotacao_acao(symbol)
            return resultado
            
        except Exception as e:
            print(f'Erro ao obter cotação da ação {symbol}:{e}')
            return f'Erro ao obter cotação da ação'
        
    elif 'qual a previsão do tempo para hoje em' in comando or 'como está o clima hoje em' in comando or 'como está o tempo hoje em' in comando:
        resultado = model.generate_content(comando)
        resultado = resultado.text
        resultado = resultado.replace('*','').replace('km/h','quilometros por hora').replace('-', 'até')
        print(resultado)
        return resultado
    
    elif 'quais as notícias do dia' in comando or 'quais as principais notícias do dia' in comando:
        # Configuração da API de Notícias
        api_key = get_env.print_env(['GNEW_KEY'])['GNEW_KEY']
        url = f'https://gnews.io/api/v4/top-headlines?country=br&lang=pt&token={api_key}'
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Lança um erro para códigos de status HTTP 4xx/5xx
            news_data = response.json()
            print(news_data)  # Adicione este print para verificar a resposta completa

            # Verificar se a resposta contém notícias
            if 'articles' in news_data:
                # Extrair os títulos das notícias
                headlines = [article['title'] for article in news_data['articles']]
                
                # Juntar os títulos em uma string
                resultado = "\n".join(headlines)
                print(resultado)
                return resultado
            else:
                resultado = "Não foram encontradas notícias."
                return resultado
        except Exception as e:
            print(f"Erro ao obter notícias: {e}")
            return f"Erro ao obter notícias"

    elif comando == 'sair' or comando == 'fechar programa':
        return 'Desligando'
    else:
        listen.listen_function()