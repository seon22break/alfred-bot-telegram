#!/usr/bin/env python
from colorama import Fore
from telegram.ext import filters,ApplicationBuilder, ContextTypes, MessageHandler,CommandHandler
from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
import json
import os

class Alfred(object):

    def __init__(self, token : str = None, questions : dict = None):
        self.__version__ = "0.0.1"
        self.token= token
        self.questions = questions
        self.actualQuestion = 0
        self.actualSchema = "compression"

        print(Fore.CYAN+" [Alfred] - Iniciando Alfred")
        print(Fore.CYAN+" [Alfred] - Version: "+ self.__version__)
        print(Fore.CYAN+" [Alfred] - Token: " + self.token)

    def run(self):
        bot = ApplicationBuilder().token(self.token).build()
        
        bot.add_handler(CommandHandler("start",self.startCommand,filters=None))
        bot.add_handler(CommandHandler("go",self.goCommand,filters=None))

        bot.add_handler(MessageHandler(filters.TEXT , self.allMessagesHander))
        bot.run_polling()

    async def allMessagesHander(self,update: Update, context: ContextTypes):
        print(Fore.CYAN + " [Alfred] - All messages handler "+ str(update.message.text))
        print(Fore.CYAN + " [Alfred] - All messages handler chatID: " + str(update.message.chat.id))

        if update.message.text == "/start" or update.message.text == "/go":
            pass

        if update.message.text == "🚀 Comenzar Test 🚀":
            await self.goCommand(update,context)
            pass

        if update.message.text.startswith("Respuesta: ") and self.actualQuestion > 0:

            if(self.actualQuestion == len(self.questions)):
                await update.message.reply_text("¡¡¡Gracias por realizar la prueba!!!")
                await update.message.reply_text("En breve recibirás el resultado")
                self.actualQuestion = 0
                return

            await self.getQuestion(update)

        pass

    async def startCommand(self,update: Update, context: ContextTypes):

        print(Fore.CYAN + " [Alfred] - WELCOME "+ str(update.message.chat_id))

        await update.message.reply_text(str(os.getenv('START_MESSAGE')),parse_mode="MarkdownV2")

        await update.message.reply_text(str(os.getenv('HELP_MESSAGE')),parse_mode="MarkdownV2")

        reply_markup = ReplyKeyboardMarkup([[KeyboardButton("🚀 Comenzar Test 🚀")]],resize_keyboard=True,one_time_keyboard=False)

        await update.message.reply_text("¿Estás preparado?", reply_markup=reply_markup)
    
    async def goCommand(self,update: Update, context: ContextTypes):

        if self.questions == None:
            print(Fore.RED + " [Alfred] - Questions are not valid")
            exit(1)

        await self.getQuestion(update)

        self.actualQuestion += 1
        pass

    async def getQuestion(self,update):
        if self.actualQuestion == 0 and self.actualSchema=="compression":
            await update.message.reply_text("Comenzamos con la prueba 🚀")

        await update.message.reply_photo(os.getenv("HOST_IMAGES")+"/"+self.questions[self.actualQuestion]["resource"])
        await update.message.reply_text(self.questions[self.actualQuestion]["question"],parse_mode="MarkdownV2")

        reply_markup = ReplyKeyboardMarkup(
                [
                    [KeyboardButton("Respuesta: A"),KeyboardButton("Respuesta: B")],
                    [KeyboardButton("Respuesta: C"),KeyboardButton("Respuesta: D")],
                ]
                
            ,resize_keyboard=True,one_time_keyboard=True)

        await update.message.reply_text("Selecciona tu respuesta", reply_markup=reply_markup)

        self.actualQuestion += 1

    








