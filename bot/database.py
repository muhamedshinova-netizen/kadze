from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY, FREE_GENERATIONS_PER_DAY
from datetime import date

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_user(user_id: int):
    user = supabase.table("users").select("*").eq("telegram_id", user_id).execute()
    if not user.data:
        supabase.table("users").insert({
            "telegram_id": user_id,
            "generations_today": 0,
            "last_reset": str(date.today())
        }).execute()
        return {"telegram_id": user_id, "generations_today": 0, "is_premium": False}
    return user.data[0]

def can_generate(user_id: int):
    user = get_user(user_id)
    today = str(date.today())
    if user.get("last_reset") != today:
        supabase.table("users").update({
            "generations_today": 0,
            "last_reset": today
        }).eq("telegram_id", user_id).execute()
        user["generations_today"] = 0
    if user.get("is_premium"):
        return True
    return user["generations_today"] < FREE_GENERATIONS_PER_DAY

def increment_generation(user_id: int):
    user = get_user(user_id)
    supabase.table("users").update({
        "generations_today": user["generations_today"] + 1
    }).eq("telegram_id", user_id).execute()
