#!/usr/bin/env python
import os,sys
from dotenv import load_dotenv
from colorama import Fore, init
from Alfred.Alfred import *
from Supabase.Supabase import *
load_dotenv()
init()

if __name__ == "__main__":
    
    TOKEN_TELEGRAM_BOT = os.getenv('TOKEN_TELEGRAM_BOT')
    
    if(TOKEN_TELEGRAM_BOT == None):
        print(Fore.RED + "Token bot is not valid")
        exit(1)    

    with open("src/assets/questions.json") as f:
        questions = json.load(f)
    
    Supabase().insert_question_answer(12,questions[3],"Adios",3)
    data = Supabase().get_data_by_user(12)
    print(data)
    #data[3] = questions[3]
    #Supabase().insert_question_answer(12,data,"P",2)

    #Alfred(TOKEN_TELEGRAM_BOT,questions).run()
