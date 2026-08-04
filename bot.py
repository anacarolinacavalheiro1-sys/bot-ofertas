import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

app = Flask(__name__)

TOKEN = "8982941579:AAEG71e1MZk_RpzFebKhEc6Nltsf-lLfJL4"
URL_PROJETO = "https://onrender.com"

aplicativo = ApplicationBuilder().token(TOKEN).build()

async def iniciar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Olá! O bot está funcionando.\n\n"
        "Envie um link da Shopee, Mercado Livre, Amazon ou Magalu."
    )

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    texto_usuario = update.message.text
    print(f"Mensagem recebida: {texto_usuario}")
    await update.message.reply_text(f"Recebi seu link: {texto_usuario}")

aplicativo.add_handler(CommandHandler("start", iniciar))
aplicativo.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

@app.route('/', methods=['GET', 'POST'])
def home():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(aplicativo.bot.set_webhook(url=URL_PROJETO))
        print("Webhook configurado com sucesso!")
    except Exception as e:
        print(f"Erro no webhook: {e}")
    return "O bot está em execução!", 200

@app.route('/webhook', methods=['POST'])
def receber_mensagens():
    if request.method == "POST":
        try:
            dados = request.get_json()
            update = Update.de_json(dados, aplicativo.bot)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(aplicativo.process_update(update))
            return "OK", 200
        except Exception as e:
            print(f"Erro interno: {e}")
            return "Erro Interno", 500
    return "Metodo nao permitido", 405

if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=porta)
    
