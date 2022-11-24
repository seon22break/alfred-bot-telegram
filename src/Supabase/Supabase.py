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
            print(Fore.RED + " [Supabase] - Error: " + e.message)
            return []

    def insert_question_answer(self,chat_id : int, question: object, answer : str):
        data = self.supabase.table("students").select("questions").eq("chatID",chat_id).limit(1).order("created_at").execute()
        dataStored = data.data[0]
        question['user-answer'] = answer.strip().capitalize()

        if(dataStored["questions"] == None):
            dataStored["questions"] = [question]
        else:
            dataStored["questions"]["answers"].append(question)
        
        self.supabase.table("students").update(json.dumps(dataStored)).eq("chatID",chat_id).execute()



