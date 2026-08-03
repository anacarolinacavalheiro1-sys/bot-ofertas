from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Configuração do Token do Telegram
TOKEN = "8982941579:AAEG7le1MZk_RpzFebKhEc6Nltsf-lLfJL4"

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

def main() -> None:
    aplicativo = ApplicationBuilder().token(TOKEN).build()
    aplicativo.add_handler(CommandHandler("start", iniciar))
    aplicativo.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receber_mensagem))
    aplicativo.run_polling()

if __name__ == "__main__":
    main()
  
