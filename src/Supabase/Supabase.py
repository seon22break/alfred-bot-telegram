from colorama import Fore
from supabase import create_client, Client
import os
from dotenv import load_dotenv

supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def obtain_data_student(id:int):
    try:
        return supabase.table("students").select().eq("id", id).execute()
    except Exception as e:
        print(Fore.RED + " [Supabase] - Error: " + e.message)
        return []

def insert_data_by_user(age : int ,questions : object):
    try:
        return supabase.table("students").insert([
            {
                "age": age,
                "questions": questions,
                "points" : 0
            }
        ]).execute()
    except Exception as e:
        print(Fore.RED + " [Supabase] - Error: " + e.message)
        return []

