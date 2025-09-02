import os
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أنا آلة حاسبة ابعثلي أي عملية حسابية كيما 5*5 ولا 100/2 و نعطيك النتيجة")

async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    try:
        result = eval(user_input, {"__builtins__": {}}, {})
        await update.message.reply_text(f"النتيجة: {result}")
    except Exception:
        await update.message.reply_text("اكتب عملية حسابية عليها القيمة يا حمار")

class Handler:
    async def fetch(self, request, env, ctx):
        try:
            BOT_TOKEN = env.BOT_TOKEN
            application = Application.builder().token(BOT_TOKEN).build()
            application.add_handler(CommandHandler("start", start_command))
            application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calculate))

            if request.method == 'POST':
                body = await request.json()
                update = Update.de_json(body, application.bot)
                await application.initialize()
                await application.process_update(update)
                await application.shutdown()
                return Response(status=200)
            return Response("OK", status=200)
        except Exception as e:
            return Response(str(e), status=500)
