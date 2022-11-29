from colorama import Fore
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import json
import numpy as np

class Supabase():
    def __init__(self) -> None:
        self.supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
        pass

    def insert_new_user(self,chat_id,age,month):
        try:
            return self.supabase.table("students").insert([
                {
                    "chatID": chat_id,
                    "years": age,
                    "month": month,
                }   
            ]).execute()
        except Exception as e:
            print(Fore.RED + " [Supabase] - Error: " + str(e.message))
            return False

    def insert_question_answer(self,chat_id : int, question: object, answer : str, page: int):
        
        data = self.get_data_by_user(chat_id)
        if data == None:
            data = {}

        question['user-answer'] = answer.strip()
        
        data[page] = question

        try:
            return self.supabase.table("students").update({
                "questions" : data
                }).eq("chatID",chat_id).execute()
        except Exception as e:
            print(Fore.RED + " [Supabase] - Error: " + str(e))
            return False

    def get_data_by_user(self,chat_id):
        try:
            data = self.supabase.table("students").select("questions").eq("chatID",chat_id).limit(1).order("created_at").execute()
            return data.data[0]['questions']
        except Exception as e:
            print(Fore.RED + " [Supabase] - Error: " + str(e))
            return {}

    def results_by_age(self,chat_id,age,month):
        ages = float("{0}.{1}".format(age,month))
        totalAllowned = 0

        if ages in np.arange(4.0,4.3,0.1):
             totalAllowned = 12

        if ages in np.arange(4.3,4.6,0.1):
             print("hello")
             totalAllowned = 16
        
        if ages in np.arange(4.6,4.9,0.1):
             totalAllowned = 15
        
        if ages in np.arange(4.9,5.0,0.1):
             totalAllowned = 17
                
        if ages in np.arange(5.0,5.3,0.1):
             totalAllowned = 17
        
        if ages in np.arange(5.3,5.6,0.1):
             totalAllowned = 18
        
        if ages in np.arange(5.6,5.9,0.1):
             totalAllowned = 19
        
        if ages in np.arange(5.9,6.0,0.1):
             totalAllowned = 18
        
        if ages in np.arange(6.0,6.3,0.1):
             totalAllowned = 19
        
        if ages in np.arange(6.3,6.6,0.1):
             totalAllowned = 19
        
        if ages in np.arange(6.6,6.9,0.1):
             totalAllowned = 20
        
        if ages in np.arange(6.9,7.0,0.1):
             totalAllowned = 21

        data = self.get_data_by_user(chat_id)
        totalUser = 0
        for answer in data.values():
            if answer['schema'] == "comprenssion":
                if answer['correct-answer'] == answer['user-answer']:
                    totalUser += 1
            
            if answer['schema'] == "expression1" or answer['schema'] == "expression2":
                if answer['user-answer'] in answer['correct-answer']:
                    totalUser += 1
        
        return totalUser






