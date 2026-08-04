import asyncio
import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8982941579:AAEG7le1MZk_RpzFebKhEc6Nltsf-lLfJL4"
URL_RENDER = os.environ.get("RENDER_EXTERNAL_URL")
URL_PROJETO = f"{URL_RENDER}/webhook"

# Variável que o servidor precisa encontrar
app = Flask(__name__)

# Inicializa o aplicativo do Telegram
aplicativo = ApplicationBuilder().token(TOKEN).build()

async def iniciar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Olá! O bot está funcionando.\n\n"
        "Envie um link da Shopee, Mercado Livre, Amazon ou Magalu."
    )

async def receber_mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    texto = update.message.text.strip()
    texto_minusculo = texto.lower()

    if not texto.startswith(("http://", "https://")):
        await update.message.reply_text("Envie um link começando com http:// ou https://")
        return

    if "shopee" in texto_minusculo:
        plataforma = "Shopee"
    elif "mercadolivre" in texto_minusculo or "mercadolibre" in texto_minusculo:
        plataforma = "Mercado Livre"
    elif "amazon" in texto_minusculo or "amzn" in texto_minusculo:
        plataforma = "Amazon"
    elif "magalu" in texto_minusculo or "magazineluiza" in texto_minusculo:
        plataforma = "Magalu"
    else:
        plataforma = "Plataforma não identificada"

    mensagem = (
        "🔥 OFERTA RECEBIDA!\n\n"
        f"🛍️ Plataforma: {plataforma}\n"
        f"🔗 Link: {texto}\n\n"
        "O link foi registrado com sucesso."
    )
    await update.message.reply_text(mensagem)

# Registra os handlers no aplicativo global
aplicativo.add_handler(CommandHandler("start", iniciar))
aplicativo.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receber_mensagem))

# Rota que receberá as mensagens do Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        update = Update.de_json(request.get_json(force=True), aplicativo.bot)
        loop.run_until_complete(aplicativo.initialize())
        loop.run_until_complete(aplicativo.process_update(update))
        return "OK", 200

# Rota para registrar o Webhook
@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    sucesso = loop.run_until_complete(aplicativo.bot.set_webhook(url=URL_PROJETO))
    if sucesso:
        return "Webhook configurado com sucesso!", 200
    return "Falha ao configurar Webhook.", 400
    
if __name__ == "__main__":
    import os
    porta = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=porta)
    
