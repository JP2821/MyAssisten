# J.A.R.V.I.S - Just A Rather Very Intelligent System

## Descrição

J.A.R.V.I.S é um assistente pessoal inteligente capaz de executar diversas funções, incluindo busca de informações, tocar músicas, obter cotações de ações, verificar previsões do tempo, e obter as principais notícias do dia. O sistema foi desenvolvido em Python e utiliza diversas APIs e bibliotecas para fornecer essas funcionalidades.

## Funcionalidades

- **Busca de informações**: Utiliza a API do Gemini para buscar informações e responder perguntas.
- **Tocar músicas**: Toca músicas no YouTube utilizando o PyWhatKit.
- **Cotação de ações**: Obtém cotações de ações utilizando um módulo de finanças personalizado.
- **Previsão do tempo**: Obtém previsões do tempo utilizando a API do Gemini.
- **Notícias do dia**: Obtém as principais notícias do dia utilizando a API do GNews.
- **Reconhecimento de fala**: Utiliza a biblioteca SpeechRecognition para reconhecer comandos de voz.
- **Síntese de fala**: Utiliza a biblioteca Pyttsx3 para falar os resultados dos comandos.

## Instalação

### Pré-requisitos

- Python 3.6 ou superior
- Instalar bibliotecas necessárias

```bash
pip install wikipedia
pip install pywhatkit
pip install google-generativeai
pip install requests
pip install SpeechRecognition
pip install pyttsx3
```

### Clonar o repositório

```bash
git clone https://github.com/seu_usuario/jarvis.git
cd jarvis
```

## Configuração

### API Keys

Você precisará de chaves de API para o Gemini e GNews. Adicione suas chaves de API no arquivo `.env` no formato:

```
GEMINI_KEY=your_gemini_api_key
GNEWS_KEY=your_gnews_api_key
```

### Estrutura de Diretórios

```
jarvis/
│
├── modules/
│   ├── __init__.py
│   ├── backbone.py
│   ├── finance.py
│   ├── createSomething.py
│   ├── listen.py
│   ├── speak.py
│   ├── weatherForecast.py
│   └── get_env.py
│
├── jarvis.py
├── requirements.txt
└── README.md
```

## Uso

Para iniciar o J.A.R.V.I.S, execute o script `jarvis.py`:

```bash
python jarvis.py
```

O assistente ficará ativo aguardando por comandos de voz. Você pode utilizar comandos como:

- "Jarvis, procure por Albert Einstein"
- "Jarvis, toque Bohemian Rhapsody"
- "Jarvis, qual o valor da ação da AAPL?"
- "Jarvis, qual a previsão do tempo para hoje em São Paulo?"
- "Jarvis, quais as notícias do dia?"

### Exemplo de Comando

```python
import wikipedia
import pywhatkit
import google.generativeai as gemini
import requests

from modules import finance
from modules import createSomething
from modules import listen
from modules import weatherForecast
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

    elif 'toque' em comando:
        musica = comando.replace('toque','')
        resultado = pywhatkit.playonyt(musica)
        resultado = f'Tocando {musica} no youtube!'
        return resultado
    
    elif 'cotação' em comando or 'cote' em comando or 'qual o valor da ação' em comando:
        symbol = comando.replace('cotação','').replace('cote','').replace('qual o valor da ação','').rstrip().strip().upper()
        try:
            resultado = finance.obter_cotacao_acao(symbol)
            return resultado
            
        except Exception as e:
            print(f'Erro ao obter cotação da ação {symbol}:{e}')
            return f'Erro ao obter cotação da ação'
        
    elif 'qual a previsão do tempo para hoje em' em comando or 'como está o clima hoje em' em comando or 'como está o tempo hoje em' em comando:
        resultado = model.generate_content(comando)
        resultado = resultado.text
        resultado = resultado.replace('*','').replace('km/h','quilometros por hora').replace('-', 'até')
        print(resultado)
        return resultado
    
    elif 'quais as notícias do dia' em comando or 'quais as principais notícias do dia' em comando:
        # Configuração da API de Notícias
        api_key = get_env.print_env(['GNEWS_KEY'])['GNEWS_KEY']
        url = f'https://gnews.io/api/v4/top-headlines?country=br&lang=pt&token={api_key}'
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Lança um erro para códigos de status HTTP 4xx/5xx
            news_data = response.json()
            print(news_data)  # Adicione este print para verificar a resposta completa

            # Verificar se a resposta contém notícias
            if 'articles' em news_data:
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

    elif comando == 'sair' or 'fechar programa':
        return 'Desligando'
    else:
        listen.listen_function()

import speech_recognition as sr
from modules import speak

def listen_function():
    try: 
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.pause_threshold = 1  # Define a pausa mínima entre as palavras
            print('JARVIS> ')
            audio = r.listen(source)
            comando = r.recognize_google(audio, language='pt-br')
            comando = comando.lower()
            if 'jarvi' em comando or 'jarvis' em comando or 'jarwis' em comando:
                comando = comando.replace('jarvis', '').replace('jarvi','').replace('jarwis','')
                speak.speak_function(comando)
                return comando
                
    except Exception as e:
        print(e)  # Imprime o erro para fins de depuração
        return 'Não entendi, poderia repetir?'

import pyttsx3

def speak_function(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    volume = engine.getProperty('volume')
    rate = engine.getProperty('rate')

    engine.setProperty('voice', voices[0].id)
    engine.setProperty('volume', volume-0.10)
    engine.setProperty('rate', rate-10)
    if text == None:
        text = ''

    engine.say(text)
    engine.runAndWait()
    
from modules import listen, backbone,speak
if __name__ == "__main__":
    print('Eu sou: J.A.R.V.I.S > Just A Rather Very Intelligent System')
    while True:
        comando = listen.listen_function()
        if comando != None:
            response = backbone.execute_command(comando)
            speak.speak_function(response)
        
            if response == 'Desligando':
                speak.speak_function('Sequência de desligamento iniciada!')
                speak.speak_function('Até logo, Senhor!')
                break
        else:
            print('comando não encontrado')
            pass
```

## Features
- [ ] Criação de GUI

- [ ] Criar configurações de inicialização
   - [ ] Login
   - [ ] Senha
   - [ ] FaceID
   - [ ] Voz ID

- [ ] Criar função de criação de venv

- [ ] Criar função de instalação de preparação do ambiente

- [ ] Criar módulos de testes

- [ ] Criar documentação para todos os módulos e classes

- [ ] Criar sistema de logs

- [ ] Abertura de págins web / sites específicos

- [X] Previsão do tempo

- [X] Notícias do dia 

- [ ] escreva um nota

- [ ] DistÂncia entre duas localizações

- [ ] Minha cocalização 

- [ ] Eventos em calendários

- [ ] Informações sobre filmes ou séries: Integrar o assistente com uma API de dados sobre filmes e séries para fornecer informações sobre lançamentos, elenco, sinopse e avaliações.

- [ ] Comandos de controle do computador: Permitir que o assistente execute tarefas no computador, como abrir programas, criar lembretes, agendar eventos ou fazer capturas de tela.

- [ ] Tradução de idiomas: Adicionar a funcionalidade de tradução para permitir que o assistente traduza palavras ou frases para outros idiomas.

- [X] Pesquisa em outros mecanismos de busca: Além da pesquisa no Wikipedia, permitir que o assistente pesquise em outros mecanismos de busca, como o Google, para fornecer resultados mais abrangentes.

- [ ] Lembrete de compromissos: Implementar uma funcionalidade para agendar e lembrar compromissos ou tarefas importantes.

- [ ] Suporte a comandos personalizados: Implementar a capacidade de adicionar comandos personalizados para tarefas específicas, de acordo com as necessidades do usuário.

## Contato

Se você tiver alguma dúvida ou problema, sinta-se à vontade para abrir uma issue no repositório ou entrar em contato comigo.

---
