import os
import asyncio
from flask import Flask, request

# Inicializa o servidor Flask
app = Flask(__name__)

# --- CONFIGURAÇÃO DO SEU BOT ---
# IMPORTANTE: Caso seu arquivo original tivesse chaves de Token ou importações
# específicas de bibliotecas no topo, certifique-se de mantê-las ativas.
# O objeto 'aplicacao' abaixo precisa representar o seu gerenciador do bot.

@app.route('/', methods=['GET', 'POST'])
def home():
    # Rota raiz blindada: Sempre que o Render ou o Telegram baterem aqui,
    # o webhook será forçado a se reconfigurar de forma automática.
    try:
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        # Configura o Webhook apontando direto para a rota de recebimento (/webhook)
        loop.run_until_complete(aplicacao.bot.set_webhook(url="https://onrender.com"))
        print("Webhook reconfigurado com sucesso na raiz!")
    except Exception as e:
        print(f"Aviso de inicialização do webhook: {e}")
        
    if request.method == 'POST':
        return "OK", 200
    return "Bot is running e Webhook configurado!", 200

@app.route('/webhook', methods=['POST'])
def receber_mensagens():
    if request.method == "POST":
        print("Nova mensagem recebida do Telegram!")
        dados = request.get_json()
        update = aplicacao.update.de_json(dados, aplicacao.bot)
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(aplicacao.process_update(update))
        
        return "OK", 200
    return "Metodo nao permitido", 405



if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=porta)
    
