import json
from difflib import get_close_matches
from parsivar import Normalizer
from parsivar import Tokenizer

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as file:
        data: dict = json.load(file)
        return data
    
def save_knowledge_base(file_path: str, data: dict): 
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)        
        
def find_best_match(user_question: str, questions: list) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
        
def Tokenize_Input(user_input: str):
    tokenized_input : list = Tokenizer().tokenize_words(Normalizer().normalize(user_input))
    return tokenized_input
     
def classify_input(words_list: list, data: dict) -> str | None:
    
    #data = load_knowledge_base("D:\Daneshgah\Term5\AI\Project\.vscode\Knowledge_base.json")
    
    for chitChatQuestion in data["ChitChat"]:
        for word in words_list:
            if word == chitChatQuestion["question"]:
                return "ChitChat"
            
    for item in data["Inventory"]:
        for word in words_list:
            if word == item["name"]:
                return "Inventory"    
    
         
        
def chat_bot():
    knowledge_base: dict = load_knowledge_base("D:\Daneshgah\Term5\AI\Project\.vscode\Knowledge_base.json")
    #Inventory_data: dict = load_knowledge_base("D:\Daneshgah\Term5\AI\Project\.vscode\Inventory.json")
    while True:
        raw_user_input: str = input("چه کمکی ازم برمیاد؟ ")
        
        if(raw_user_input.lower == "خروج" or raw_user_input.lower == "exit"):
            break
        input_words_list = Tokenize_Input(raw_user_input)
        
        #TODO decide witch scope to search in 
        chosenScope = classify_input(input_words_list,knowledge_base)
        print(chosenScope)
        best_match: str | None = find_best_match(raw_user_input,[q["question"] for q in knowledge_base["ChitChat"]])
        
        #if best_match:
            #answer : str = get_answer_for_question(best_match,knowledge_base)
            #print(f"Bot: {answer}")
            #print(Normalizer().normalize(answer))
        #else:
            #print("Bot : I don\'t knwo the answer , can you teach me?")
            #print(Normalizer().normalize("پاسخی یافت نشد"))
           #new_answer: str = input("Type the answer or 'skip' to skip : ")
            
        '''if new_answer.lower() != "skip":
                knowledge_base["ChitChat"].append({"question":user_input,"answer":new_answer})
                save_knowledge_base("knowledge_base.json",knowledge_base)
                #print("Bot: Thanks for teaching me a new thing")
                print(Normalizer().normalize("ممنون که چیز جدیدی یادم دادی"))'''
        
if __name__ == "__main__":
    chat_bot()