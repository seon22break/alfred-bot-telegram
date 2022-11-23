#!/usr/bin/env python
from colorama import Fore
from telegram.ext import filters,ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler,CallbackContext,ConversationHandler
from telegram import KeyboardButton, ReplyKeyboardMarkup, Update,Chat
import json

class Alfred(object):

    def __init__(self, token : str = None, questions : dict = None):
        self.__version__ = "0.0.1"
        self.token= token
        self.questions = questions
        self.startMessage = "Hola, me presento, mi nombre es Alfred 🤖\. \n\nSoy un bot diseñado para ayudarte a realizar un *pre\-diagnóstico* en el desarrollo morfosintáctico de niños de 3\-6 años\.\n\nNuestra prueba se basa en el estándar *TSA*\.\nQue consta de una parte de comprensión 📖 y otra de expresión 💬\.\n\nAl finalizar el proceso obtendrás un resultado con observaciones acerca de la prueba realizada\.\n\n\n ``` Recuerda que este resultado es una aproximación y siempre deberías acudir a un especialista```"
        self.helpMessage = "Según la parte de la prueba, la tarea del niño será:\n\n *Compresión* 📖: tras visualizar la lámina, se le dirá una frase y deberá elegir que letra corresponde y después se dirá otra frase y deberá elegir otra letra\. La respuesta a una misma lámina nunca serán las mismas\. Cuando hayan contestado se pasará a la siguiente lámina\. \n\n *Expresión* 💬: \n\n \* *Expresión 1*: junto con la lámina se le enviarán dos audios\. \n\n \* *Expresión 2*: se le enviará un audio con una frase inacabada, tras escucharlo deberá enviar un audio con la palabra correspondiente\."
        self.actualQuestion = 0
        print(Fore.CYAN+" [Alfred] - Iniciando Alfred")
        print(Fore.CYAN+" [Alfred] - Version: "+ self.__version__)
        print(Fore.CYAN+" [Alfred] - Token: " + self.token)
    
    async def button(self,update: Update, context: ContextTypes) -> None:
        print(Fore.CYAN + " [Alfred] - Button")
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text=f"Selected option: {query.data}")

    def run(self):
        bot = ApplicationBuilder().token(self.token).build()
        bot.add_handler(MessageHandler(filters.ALL , self.allMessagesHander))
        bot.run_polling()

    async def allMessagesHander(self,update: Update, context: ContextTypes):
        print(Fore.CYAN + " [Alfred] - All messages handler "+ str(update.message.text))
        
        await context.bot.delete_message(update.message.chat_id,update.message.message_id)

        if update.message.text.startswith("Respuesta: ") and self.actualQuestion > 0:

            if(self.actualQuestion == len(self.questions)):
                await update.message.reply_text("¡¡¡Gracias por realizar la prueba!!!")
                await update.message.reply_text("En breve recibirás el resultado")
                self.actualQuestion = 0
                return

            await self.getNewQuestion(update,context)
            self.actualQuestion += 1

        if update.message.text == "/start":
            await self.startCommand(update,context)
        
        if update.message.text == "🚀 Comenzar Test 🚀" or update.message.text == "/go":
            await self.goCommand(update,context)

        pass

    async def startCommand(self,update: Update, context: ContextTypes) -> None:
        print(Fore.CYAN + " [Alfred] - Welcome tutor message")
        await update.message.reply_text(str(self.startMessage),parse_mode="MarkdownV2")
        await update.message.reply_text(str(self.helpMessage),parse_mode="MarkdownV2")
        reply_markup = ReplyKeyboardMarkup([[KeyboardButton("🚀 Comenzar Test 🚀")]],resize_keyboard=True,one_time_keyboard=True)
        await update.message.reply_text("¿Estás preparado?", reply_markup=reply_markup)
    
    async def goCommand(self,update: Update, context: ContextTypes):
        print(Fore.CYAN + " [Alfred] - [BETA] Delete previous messages ")

        if self.questions == None:
            print(Fore.RED + " [Alfred] - Questions are not valid")
            exit(1)

        await update.message.reply_text("Comenzamos con la prueba 🚀")
        await update.message.reply_text(self.questions[0]["question"],parse_mode="MarkdownV2")
        reply_markup = ReplyKeyboardMarkup([
            [KeyboardButton("Respuesta: A")],
            [KeyboardButton("Respuesta: B")],
            [KeyboardButton("Respuesta: C")],
            [KeyboardButton("Respuesta: D")],
            ],resize_keyboard=True,one_time_keyboard=True)

        await update.message.reply_text("Selecciona tu respuesta", reply_markup=reply_markup)

        self.actualQuestion += 1
        pass

    async def getNewQuestion(self,update,context):
        await update.message.reply_text(self.questions[self.actualQuestion]["question"],parse_mode="MarkdownV2")
        reply_markup = ReplyKeyboardMarkup([
            [KeyboardButton("Respuesta: A")],
            [KeyboardButton("Respuesta: B")],
            [KeyboardButton("Respuesta: C")],
            [KeyboardButton("Respuesta: D")],
            ],resize_keyboard=True,one_time_keyboard=True)

        await update.message.reply_text("Selecciona tu respuesta", reply_markup=reply_markup)
        
    








