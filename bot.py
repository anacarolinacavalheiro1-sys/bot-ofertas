import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# 1. Inicializa o servidor de internet Flask
app = Flask(__name__)

# 2. Configurações essenciais de conexões
TOKEN = "8982941579:AAEG71e1MZk_RpzFebKhEc6Nltsf-lLfJL4"
URL_PROJETO = "https://onrender.com"

# 3. Inicializa o cérebro do Telegram
aplicativo = ApplicationBuilder().token(TOKEN).build()

# --- SUA LÓGICA DE REGRAS E MENSAGENS DO ROBÔ ---
async def iniciar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Mensagem de boas-vindas quando o usuário digita /start
    await update.message.reply_text(
        "Olá! O bot de ofertas está funcionando perfeitamente.\n\n"
        "Envie um link da Shopee, Mercado Livre, Amazon ou Magalu para começar."
    )

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Captura a mensagem de texto enviada pelo usuário no chat
    texto_usuario = update.message.text
    print(f"Link recebido no servidor: {texto_usuario}")
    
    # Resposta padrão enviada de volta ao usuário confirmando o recebimento
    await update.message.reply_text(f"Recebi seu link com sucesso: {texto_usuario}")

# 4. Registra os comandos e regras de texto dentro do robô
aplicativo.add_handler(CommandHandler("start", iniciar))
aplicativo.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

# --- ROTAS DE INFRAESTRUTURA PARA O RENDER ---
@app.route('/', methods=['GET', 'POST'])
def home():
    # Toda vez que a raiz do site for carregada, força o registro do Webhook
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(aplicativo.bot.set_webhook(url=URL_PROJETO))
        print("Webhook sincronizado com sucesso na rota raiz!")
    except Exception as e:
        print(f"Aviso de sincronização do webhook: {e}")
    return "O bot de ofertas está ativo e em execução contínua!", 200

@app.route('/webhook', methods=['POST'])
def receber_mensagens():
    # Rota secreta que recebe os envios do Telegram e repassa para o robô processar
    if request.method == "POST":
        try:
            dados = request.get_json()
            update = Update.de_json(dados, aplicativo.bot)
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(aplicativo.process_update(update))
            return "OK", 200
        except Exception as e:
            print(f"Erro interno de processamento: {e}")
            return "Erro Interno", 500
    return "Método não permitido", 405

if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=porta)
    
