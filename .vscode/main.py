import json
from difflib import get_close_matches
from parsivar import Normalizer
from parsivar import Tokenizer

def load_data(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as file:
        data: dict = json.load(file)
        return data
    
def save_knowledge_base(file_path: str, data: dict): 
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)        
        
def find_best_match(user_question: str, questions: list) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(founded_word: str, chosenDict: str) -> str | None:
    data = load_data("D:\Daneshgah\Term5\AI\Project\.vscode\Knowledge_base.json")
    if chosenDict in data:
        for q in data[chosenDict]["questions"]:
            if q["question"] == founded_word:
                return q["answer"]
    return None       
    #TODO implement for inventory too        
        
def Tokenize_Input(user_input: str):
    tokenized_input : list = Tokenizer().tokenize_words(Normalizer().normalize(user_input))
    return tokenized_input
     
def classify_input(words_list: list, data: dict) -> tuple | None:
    
    #data = load_knowledge_base("D:\Daneshgah\Term5\AI\Project\.vscode\Knowledge_base.json")
    
    for chitChatQuestion in data["ChitChat"]:
        for word in words_list:
            if word == chitChatQuestion["question"]:
                return ("ChitChat" , word)
            
    for item in data["Inventory"]:
        for word in words_list:
            if word == item["name"]:
                return ("Inventory" , word)    
    
def ChooseProperDict(scope : str, loadedData : dict) -> dict :
    if scope is "ChitChat" :
        return loadedData["ChitChat"]
    
    elif scope is "Inventory" :
        return loadedData["Inventory"]
        
def chat_bot():
    loaded_data: dict = load_data("D:\Daneshgah\Term5\AI\Project\.vscode\Knowledge_base.json")
    while True:
        raw_user_input: str = input("چه کمکی ازم برمیاد؟ ")
        
        if(raw_user_input.lower == "خروج" or raw_user_input.lower == "exit"):
            break
        input_words_list = Tokenize_Input(raw_user_input)
        chosenTuple = classify_input(input_words_list,loaded_data)
        founded_word = chosenTuple[1]
        chosen_scope = chosenTuple[0]
        chosenDict = ChooseProperDict(chosen_scope, loaded_data)
        
       # best_match: str | None = find_best_match(chosenTuple[0],[q["question"] for q in chosenDict])
        
        #if best_match:
        answer : str = get_answer_for_question(founded_word, chosen_scope)
        #print(f"Bot: {answer}")
        #print(Normalizer().normalize(answer))
        print(answer)
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