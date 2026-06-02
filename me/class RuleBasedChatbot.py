import re
from datetime import datetime

class RuleBasedChatbot:
    def __init__(self):

        self.rules = [
            (r"are you (.+[\.\?\!]?)|what is your name", "Yes, I'm called the Pattern-Based Chatbot. You can just call me PBC!"),           
            
            (r"I need to know the time(date)?", "The current date and time is {datetime}"),

            (r"hello|hi|hey|greetings|hola|yo", "Hello there! How can I help you today? 😊"),
            
            (r"sorry|i am sorry", "No worries, let's keep things positive! 💪"),
            
            (r"bye|goodbye|see ya later", "Goodbye! Feel free to ask questions anytime. 👋"),
         
            (r"thanks|thank you", "You're welcome! 🙏"),
            
            (r"how are you?|how is it going\??|what's up", 
             "I'm doing well, thanks for asking! What can I help you with today? 😊"),
            
            (r"I don't understand|can you explain|help me(.+[\.\?\!]?)",
             "I'm designed to follow rules and patterns. I respond based on what you say rather than deep understanding."),
            
            (None, "That's interesting! Could you tell me more? 💡")
        ]
        
        self.compiled_rules = []
        for pattern, response in self.rules:
            if pattern:
                self.compiled_rules.append((re.compile(pattern), response))
            else:
                self.compiled_rules.append((None, response))
    
    def get_response(self, user_input):
        lower_input = user_input.lower()
        
        for pattern, response in self.compiled_rules:
            if pattern: 
                if pattern.search(lower_input):

                    return response.format(datetime=self.get_current_datetime())
            else: 

                return response
        
        return self.compiled_rules[-1][1] 
    
    def get_current_datetime(self):
        return datetime.now().strftime("%B %d, %Y | %I:%M %p")

if __name__ == "__main__":
    chatbot = RuleBasedChatbot()

    print("Simple Pattern-Based Chatbot")
    print("-" * 40 + "\n")
    print("You can type 'quit' or 'exit' to stop the conversation.\n")

    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
            print("\nChatbot:\t\tFarewell! It was nice chatting with you!")
            break
        
        response = chatbot.get_response(user_input)
        
        print(f"\nChatbot:\t\t{response}\n")