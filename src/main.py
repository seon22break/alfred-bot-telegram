#!/usr/bin/env python
import os
from dotenv import load_dotenv
from colorama import Fore, init
from Alfred.Alfred import *

load_dotenv()
init()

if __name__ == "__main__":
    
    TOKEN_TELEGRAM_BOT = os.getenv('TOKEN_TELEGRAM_BOT')
    
    if(TOKEN_TELEGRAM_BOT == None):
        print(Fore.RED + "Token bot is not valid")
        exit(1)    

    with open("src/assets/questions.json") as f:
        questions = json.load(f)
    Alfred(TOKEN_TELEGRAM_BOT,questions).run()