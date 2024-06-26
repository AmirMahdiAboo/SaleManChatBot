import json
from difflib import get_close_matches
from parsivar import Normalizer
from parsivar import Tokenizer
from fuzzywuzzy import fuzz

def load_data(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as file:
        data: dict = json.load(file)
        return data
    
# def save_knowledge_base(file_path: str, data: dict): 
#     with open(file_path, 'w') as file:
#         json.dump(data, file, indent=2)        
        
# def find_best_match_sentence(user_question: str, questions: list) -> str | None:
#     matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
#     return matches[0] if matches else None

def get_answer_for_chitChat(founded_word: str, chosenDict: dict) -> str | None:
        for q in chosenDict:
            if q["question"] == founded_word:
                return q["answer"]        
        
def get_answer_for_inventory(founded_word: str, chosenDict: dict) -> tuple | None:
        for item in chosenDict:
            if item["name"] == founded_word:
                return (item["quantity"],item["price"])       
        
def Tokenize_Input(user_input: str):
    tokenized_input : list = Tokenizer().tokenize_words(Normalizer().normalize(user_input))
    return tokenized_input
     
def classify_input(words_list: list, data: dict) -> tuple | None:
    
    for chitChatQuestion in data["ChitChat"]:
        for word in words_list:
            if word == chitChatQuestion["question"]:
                return ("ChitChat" , word)
            
    for item in data["Inventory"]:
        for word in words_list:
            if word == item["name"]:
                return ("Inventory" , word)    
    
    for input in data["Cart"]:
        for word in words_list:
            if word == input["input"]:
                return ("Cart" , word)
    
def ChooseProperDict(scope : str, loadedData : dict) -> dict :
    if scope == "ChitChat" :
        return loadedData["ChitChat"]
    
    elif scope == "Inventory" :
        return loadedData["Inventory"]
    elif scope == "Cart" :
        return loadedData["Cart"]

def UpdateUserCart(user_cart : dict, requested_item : str, user_required_quantity : int, product_quantity : int, product_price : int):
    if user_required_quantity > product_quantity:
        raise ValueError("Requested quantity is more than available quantity")
    if requested_item in user_cart:
        user_cart[requested_item]['quantity'] += user_required_quantity
        user_cart[requested_item]['price'] = product_price
    else:
        user_cart[requested_item] = {'quantity': user_required_quantity, 'price': product_price}

def CalculateTotalPrice(user_cart: dict):
    total_price = 0
    for item in user_cart.values():
        total_price += item['quantity'] * item['price']
    return total_price

def UpdateLoadedData(loaded_data : dict, founded_word : str, user_required_quantity : int):
    for item in loaded_data["Inventory"]:
        if item["name"] == founded_word:
            if item["quantity"] < user_required_quantity:
                raise ValueError("درخواست شما بیشتر از موجودی است")
            item["quantity"] -= user_required_quantity
            return
    raise ValueError("Product not found in loaded data")

def ShowCart(user_cart : dict):
    if not user_cart:
        print("سبد خرید شما خالی است")
        return

    print("سبد خرید شما :\n")
    for item, details in user_cart.items():
        print(f" {item} : کالا")
        print(f" {details['quantity']} : تعداد")
        print("----------------")
    print( CalculateTotalPrice(user_cart) , " : قیمت کل  ")


def find_best_match_sentence(input_sentence, candidate_sentences):
    best_match_score = 0
    best_match_sentence = ""

    for candidate in candidate_sentences:
        similarity_score = fuzz.token_sort_ratio(input_sentence, candidate)
        if similarity_score > best_match_score:
            best_match_score = similarity_score
            best_match_sentence = candidate

    return best_match_sentence, best_match_score        

def get_answer_for_outOfScope(best_match, chosenDict) -> str | None:
    for q in chosenDict:
        if q["question"] == best_match:
            return q["answer"]    

def get_sentence_answer_chitChat(best_match, chosenDict, userInput) -> str | None:
    chitChat_questions : list = []
    for OutOfScopeQuestion in chosenDict:
        chitChat_questions.append(OutOfScopeQuestion["question"])
            
    best_match = find_best_match_sentence(userInput, chitChat_questions)
    for q in chosenDict:
        if q["question"] == best_match[0]:
            return q["answer"]

def chat_bot():
    loaded_data: dict = load_data("D:\Daneshgah\Term5\AI\Project\.vscode\Knowledge_base.json")
    user_cart : dict = {}
    while True:
        raw_user_input: str = input("شما : ")
        
        if(raw_user_input == "خروج" or raw_user_input == "exit"):
            break
        
        input_words_list = Tokenize_Input(raw_user_input)
        chosenTuple = classify_input(input_words_list,loaded_data)
        if(chosenTuple != None):
            founded_word = chosenTuple[1]
            chosen_scope = chosenTuple[0]
            chosenDict = ChooseProperDict(chosen_scope, loaded_data)
            if chosen_scope == "ChitChat":
                answer : str = get_answer_for_chitChat(founded_word, chosenDict)
                #answer : str = get_sentence_answer_chitChat(founded_word, chosenDict, raw_user_input)
                print(answer)
                
            elif chosen_scope == "Inventory":
                product_data : tuple = get_answer_for_inventory(founded_word, chosenDict)
                product_quantity : int = product_data[0]
                product_price : int = product_data[1]
                if product_quantity > 0:
                    print("{} تعداد این کالا ".format(product_quantity))
                    print("{}  قیمت هر عدد آن ".format(product_price))
                    print(Normalizer().normalize("تعداد کالا را وارد کنید :"))
                    user_required_quantity : int = int(input())
                    if(user_required_quantity > product_quantity):
                        print(Normalizer().normalize("درخواست شما بیشتر از موجودی است"))
                        continue
                    UpdateLoadedData(loaded_data, founded_word, user_required_quantity)
                    UpdateUserCart(user_cart, founded_word, user_required_quantity, product_quantity, product_price)
                    print(Normalizer().normalize("کالا به سبد خرید اضافه شد"))
                    print (Normalizer().normalize("آیا مورد دیگری نیاز دارید؟"))
                else:
                    print(Normalizer().normalize("موجودی کالا تمام شده است"))
                    
            elif chosen_scope == "Cart" :
                ShowCart(user_cart)
        else:
            chosen_scope = "OutOfScope"
            chosenDict = loaded_data["OutOfScope"]
            outOfScope_questions : list = []
            for OutOfScopeQuestion in chosenDict:
                outOfScope_questions.append(OutOfScopeQuestion["question"])
           
            best_match = find_best_match_sentence(raw_user_input, outOfScope_questions)
            if(best_match[0] == "" or best_match[0] == None or best_match[1] < 60):
                print(Normalizer().normalize("بات : متوجه نشدم"))
                continue
            else:
                answer = get_answer_for_outOfScope(best_match[0], chosenDict)
                print(answer)
        
if __name__ == "__main__":
    chat_bot()
