from colorama import Fore
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import json


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



