import os
import asyncio
from flask import Flask, request
from telegram.ext import ApplicationBuilder

# Inicializa o servidor Flask
app = Flask(__name__)

# Configurações de URL do Render
URL_RENDER = os.environ.get("RENDER_EXTERNAL_URL")
URL_PROJETO = f"{URL_RENDER}/webhook" if URL_RENDER else "https://onrender.com"

# Puxa o Token do Telegram configurado nas variáveis de ambiente
TOKEN = os.environ.get("TELEGRAM_TOKEN")

# Inicializa o aplicativo do Telegram usando a sua estrutura original
aplicativo = ApplicationBuilder().token(TOKEN).build()

@app.route('/', methods=['GET', 'POST'])
def home():
    # Toda vez que a raiz for acessada, força a reconfiguração do Webhook
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(aplicativo.bot.set_webhook(url=URL_PROJETO))
        print("Webhook configurado com sucesso via rota home!")
    except Exception as e:
        print(f"Erro ao configurar webhook na home: {e}")
        
    if request.method == 'POST':
        return "OK", 200
    return "O bot está em execução e o webhook está configurado!", 200

@app.route('/webhook', methods=['POST'])
def receber_mensagens():
    if request.method == "POST":
        try:
            print("Nova mensagem recebida do Telegram!")
            dados = request.get_json()
            
            # Converte os dados recebidos para o formato que o Telegram entende
            from telegram import Update
            update = Update.de_json(dados, aplicativo.bot)
            
            # Envia a mensagem para o robô processar e responder
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(aplicativo.process_update(update))
            
            return "OK", 200
        except Exception as e:
            print(f"Erro ao processar mensagem no webhook: {e}")
            return "Erro Interno", 500
            
    return "Metodo nao permitido", 405

if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=porta)
            
