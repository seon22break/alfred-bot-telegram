#!/usr/bin/env python
from colorama import Fore
from telegram.ext import filters,ApplicationBuilder, ContextTypes, MessageHandler,CommandHandler
from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
import json
import os
from Supabase.Supabase import *
from Voice.VoiceToText import *

class Alfred(object):

    def __init__(self, token : str = None, questions : dict = None):
        self.__version__ = "0.0.1"
        self.token= token
        self.questions = questions
        self.actualQuestion = 0
        self.actualSchema = "compression"
        self.years = 0
        self.months = 0

        print(Fore.CYAN+" [Alfred] - Iniciando Alfred")
        print(Fore.CYAN+" [Alfred] - Version: "+ self.__version__)
        print(Fore.CYAN+" [Alfred] - Token: " + self.token)

    def run(self):
        bot = ApplicationBuilder().token(self.token).build()
        bot.add_handler(CommandHandler("start",self.startCommand,filters=None))
        bot.add_handler(CommandHandler("go",self.goCommand,filters=None))
        bot.add_handler(MessageHandler(filters.VOICE, self.voiceHandler))
        bot.add_handler(MessageHandler(filters.TEXT , self.allMessagesHander))
        bot.run_polling()

    async def voiceHandler(self, update: Update, context: ContextTypes):
        print(Fore.CYAN + " [Alfred] - Voice handler "+ str(update.message.voice))
        print(Fore.CYAN + " [Alfred] - Voice handler chatID: " + str(update.message.chat.id))

        if(self.actualQuestion == len(self.questions)):
            await update.message.reply_text("¡¡¡Gracias por realizar la prueba!!!")
            await update.message.reply_text("En breve recibirás el resultado")
            self.actualQuestion = 0
            return

        if self.questions[self.actualQuestion]["schema"] == "compression":
            print(Fore.RED + " [Alfred] - Voice delete is not allowed")
            await context.bot.deleteMessage (message_id = update.message.message_id, chat_id = update.message.chat.id)
            return
        
        file = await context.bot.getFile(update.message.voice.file_id)
        
        await file.download(str(pathlib.Path().resolve())+"/cache/tmp_voice.mp3")
        
        text = VoiceToText().convert()

        saved = Supabase().insert_question_answer(chat_id=update.message.chat.id, question = self.questions[self.actualQuestion],answer=text,page=self.actualQuestion)
        
        if not saved:
            await update.message.reply_text("Ha ocurrido un error en la base de datos\. Por favor vuelva a intentarlo, presionando /start", reply_markup=None)
            return
        
        await self.getQuestion(update)

    async def allMessagesHander(self,update: Update, context: ContextTypes):
        print(Fore.CYAN + " [Alfred] - All messages handler "+ str(update.message.text))
        print(Fore.CYAN + " [Alfred] - All messages handler chatID: " + str(update.message.chat.id))

        if update.message.text == "/start" or update.message.text == "/go":
            pass

        if "," in update.message.text:

            self.years = update.message.text.split(",")[0]
            self.months = update.message.text.split(",")[1]

            if int(self.years) < 4 and int(self.years) > 7:
                await update.message.reply_text("La edad minima es 4 años y la maxima son 7\. Vuelve a comenzar presionando /start", reply_markup=None)
                return

            await update.message.reply_text("Edad: "+str(self.years)+" años y "+str(self.months)+" meses")

            # Show button to start test
            reply_markup = ReplyKeyboardMarkup([[KeyboardButton("🚀 Comenzar Test 🚀")]],resize_keyboard=True,one_time_keyboard=True)
            await update.message.reply_text("¿Estás preparado?", reply_markup=reply_markup)

        # Save user if the data is correct
        if update.message.text == "🚀 Comenzar Test 🚀":
            Supabase().insert_new_user(update.message.chat.id,self.years,self.months)
            await self.goCommand(update,context)
            pass

        if update.message.text.startswith("Respuesta: ") and self.actualQuestion > 0:
            
            saved = Supabase().insert_question_answer(update.message.chat.id,self.questions[self.actualQuestion],update.message.text.split(":")[1],self.actualQuestion)

            if not saved:
                await self.startCommand(update,context)
                return
            
            await self.getQuestion(update)

    async def startCommand(self,update: Update, context: ContextTypes):
        self.actualQuestion = 0
        self.actualSchema = "compression"
        self.years = 0
        self.months = 0
        print(Fore.CYAN + " [Alfred] - WELCOME "+ str(update.message.chat_id))

        await update.message.reply_text(str(os.getenv('START_MESSAGE')),parse_mode="MarkdownV2")

        await update.message.reply_text(str(os.getenv('HELP_MESSAGE')),parse_mode="MarkdownV2")

        await update.message.reply_text("Por favor, antes de comenzar el test es necesario que especifiques la edad del niño: 4,5",parse_mode="MarkdownV2")

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

        if self.questions[self.actualQuestion]["schema"] == "compression":
            self.actualSchema = "compression"
        
        if self.questions[self.actualQuestion]["schema"] == "expression1":
            self.actualSchema = "expression1"

        if self.questions[self.actualQuestion]["schema"] == "expression2":
            self.actualSchema = "expression2"
        
        if self.actualSchema == "compression":
            await self.getQuestionCompression(update)
        
        if self.actualSchema == "expression1":
            await self.getQuestionExpression1(update)
        
        if(self.actualSchema == "expression2"):
            await self.getQuestionExpression2(update)


        self.actualQuestion += 1
    
    async def getQuestionCompression(self,update):
        await update.message.reply_photo(os.getenv("HOST_IMAGES")+"/compression/"+self.questions[self.actualQuestion]["resource"])
        await update.message.reply_text(self.questions[self.actualQuestion]["question"].replace(".",""),parse_mode="MarkdownV2")

        reply_markup = ReplyKeyboardMarkup(
                [
                    [KeyboardButton("Respuesta: A"),KeyboardButton("Respuesta: B")],
                    [KeyboardButton("Respuesta: C"),KeyboardButton("Respuesta: D")],
                ]
                
            ,resize_keyboard=True,one_time_keyboard=True)

        await update.message.reply_text("Selecciona tu respuesta", reply_markup=reply_markup)
        pass

    async def getQuestionExpression1(self,update):
        await update.message.reply_photo(os.getenv("HOST_IMAGES")+"/expression1/"+self.questions[self.actualQuestion]["resource"])

        pathToAudio = str(pathlib.Path().resolve())+"/src/assets/audios/expression1/"+self.questions[self.actualQuestion]["audio"]
        pathFile = pathlib.PosixPath(pathToAudio)
        await update.message.reply_audio(open(pathFile, 'rb'))


        await update.message.reply_photo(os.getenv("HOST_IMAGES")+"/expression1/"+self.questions[self.actualQuestion]["resource-selected"])
        await update.message.reply_text("Te estamos escuchando",reply_markup=None)        

    async def getQuestionExpression2(self,update):
        pathToAudio = str(pathlib.Path().resolve())+"/src/assets/audios/expression2/"+self.questions[self.actualQuestion]["audio"]
        pathFile = pathlib.PosixPath(pathToAudio)
        await update.message.reply_audio(open(pathFile, 'rb'))
        await update.message.reply_text("Te estamos escuchando",reply_markup=None)
