# Python
import random

# Store inventory
inventory = {
    "Soap": {"quantity": 100, "price": 1000},
    "Shampoo": {"quantity": 32, "price": 2000},
    "Detergent A": {"quantity": 15, "price": 3000},
    "Detergent B": {"quantity": 45, "price": 5000},
    "Oil P": {"quantity": 5, "price": 10000},
    "Oil T": {"quantity": 16, "price": 10000},
}

# Small talk responses
small_talk_responses = {
    "Hello": ["Hi", "Hello", "Hey"],
    "How_are_you": ["I'm good, thank you!", "Doing well! How can I assist you today?"],
    "Goodbye": ["Bye", "See you later"],
    "Whats_up": ["Nothing much, just assisting users like you."],
    "Name": ["I'm GitHub Copilot, your AI assistant."],
    "Job": ["I'm an AI assistant designed to help with programming tasks."],
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
            return f"You've added {user_input} to your cart. It costs {item['price']}."
        else:
            return f"Sorry, {user_input} is out of stock."
    elif classification == "small_talk":
        return random.choice(small_talk_responses[user_input])
    else:
        return "I'm sorry, I didn't understand that. Can you please rephrase?"

while True:
    user_input = input("How can I assist you today? ")
    print(handle_input(user_input))