# Python
import random

# فهرست فروشگاه
inventory = {
    "صابون": {"quantity": 100, "price": 1000},
    "شامپو": {"quantity": 32, "price": 2000},
    "مایع دستشویی A": {"quantity": 15, "price": 3000},
    "مایع دستشویی B": {"quantity": 45, "price": 5000},
    "روغن P": {"quantity": 5, "price": 10000},
    "روغن T": {"quantity": 16, "price": 10000},
}

# پاسخ های گپ زدن
small_talk_responses = {
    "سلام": ["سلام", "درود", "عرض سلام"],
    "حالت چطوره": ["من خوبم, ممنون!", "خوبم! چطور میتوانم به شما کمک کنم؟"],
    "خداحافظ": ["خداحافظ", "به امید دیدار"],
    "چه خبر": ["چیز خاصی نیست, فقط در حال کمک به کاربران مثل شما."],
    "اسمت چیه": ["اسم من GitHub Copilot, دستیار هوشمند شماست."],
    "شغلت چیه": ["من یک دستیار هوشمند هستم که برای کمک به وظایف برنامه نویسی طراحی شده ام."],
}

def classify_input(user_input):
    # This is a simple classifier. In a real-world application, you would use NLP techniques.
    if user_input in inventory:
        return "shopping"
    elif user_input in small_talk_responses:
        return "small_talk"
    else:
        return "out_of_scope"

def handle_input(user_input):
    classification = classify_input(user_input)
    if classification == "shopping":
        item = inventory[user_input]
        if item["quantity"] > 0:
            item["quantity"] -= 1
            return f"{user_input} را به سبد خرید اضافه کردید. قیمت آن {item['price']} است."
        else:
            return f"متاسفم, {user_input} موجود نیست."
    elif classification == "small_talk":
        return random.choice(small_talk_responses[user_input])
    else:
        return "متاسفم, من متوجه نشدم. میتوانید آن را بازنویسی کنید؟"

while True:
    user_input = input("چطور میتوانم به شما کمک کنم؟ ")
    print(handle_input(user_input))