import os
import asyncio
from flask import Flask, request

# Inicializa o servidor Flask
app = Flask(__name__)

# IMPORTANTE: Substitua a linha abaixo pela forma exata como o seu robô é importado/inicializado
# Exemplo: de telegram import Bot -> aplicacao = Bot(token="SEU_TOKEN")
# Como não vejo o topo do seu arquivo, certifique-se de manter a sua variável 'aplicacao' aqui!

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        sucesso = loop.run_until_complete(aplicacao.bot.set_webhook(url="https://onrender.com"))
        if sucesso:
            return "Webhook configurado com sucesso!", 200
        return "Falha ao configurar Webhook", 400
    except Exception as e:
        return f"Erro: {str(e)}", 500

@app.route('/')
def home():
    return "Bot is running!", 200

if __name__ == "__main__":
    try:
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(aplicacao.bot.set_webhook(url="https://onrender.com"))
        print("Webhook configurado com sucesso!")
    except Exception as e:
        print(f"Erro ao configurar webhook: {e}")

        porta = int(os.environ.get("PORT", 5000))
        app.run(host="0.0.0.0", port=porta)
    
