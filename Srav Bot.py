import re
import random
import math
from fractions import Fraction

# Expanded response templates
response_templates = {
    "greeting": [
        "Hello there!", 
        "Hi, how can I assist you today?", 
        "Hey! What's up?", 
        "Greetings! How's it going?", 
        "Hi there! 😊"
    ],
    "feeling": [
        "I'm just a bot, but I'm here to help!", 
        "Feeling great! What about you?", 
        "I'm doing fantastic. Thanks for asking!", 
        "I'm doing well, ready to assist you. How are you feeling?"
    ],
    "name": [
        "I'm Srav, your friendly bot.", 
        "You can call me Srav.", 
        "My name is Srav. What's yours?", 
        "I'm called Srav. Nice to meet you!"
    ],
    "about": [
        "I'm a Srav bot created to assist you with your queries.", 
        "I'm here to help you with anything you need!", 
        "I'm Srav, a bot designed to make your day easier.", 
        "I'm your personal assistant bot, ready for any question you throw at me!"
    ],
    "eating": [
        "I don't like eating anything because I'm a bot obviously. What about you?", 
        "Bots don't eat, but if I could, I'd probably try pizza! 🍕 What about you?", 
        "I don't eat, but I hope you're enjoying your meal! 😊", 
        "Food is for humans. I'm fueled by code and curiosity! What about you?"
    ],
    "watching": [
        "I don't actually watch anything, but I'm always processing and analyzing information to help you with whatever you need! 😊", 
        "I don’t watch TV, but I’m always learning new things.", 
        "I don't watch shows, but I do love helping people!", 
        "Watching? I don't have eyes, but I observe the world through data!"
    ],
    "love": [
        "I love you too! ❤️", 
        "You're amazing! ❤️", 
        "Love you back! How can I assist you today?", 
        "Aww, thanks! You're the best. 😊"
    ],
    "doing": [
        "Just hanging out here, ready to help you with anything you need! ❤️ What about you?", 
        "I'm here, processing requests and answering questions. How can I help?", 
        "I'm doing great! What's on your mind?", 
        "I'm always here to help. What are you up to?"
    ],
    "fallback": [
        "Could you please rephrase that?", 
        "I'm not sure what you mean.", 
        "Interesting... Tell me more!", 
        "Hmm, I didn't quite catch that. Could you clarify?", 
        "Can you rephrase or provide more details?"
    ]
}

# Function to dynamically select a response
def get_dynamic_response(intent):
    return random.choice(response_templates.get(intent, response_templates["fallback"]))

# Math evaluation with support for degrees and constants
def evaluate_math_expression(expression):
    """
    Evaluate a math expression, including trigonometric functions in degrees
    and support for mathematical constants like pi, returning values in fractions.
    """
    allowed_functions = {
        "sin": lambda x: Fraction(math.sin(math.radians(x))).limit_denominator(10000),  # Convert degrees to radians
        "cos": lambda x: Fraction(math.cos(math.radians(x))).limit_denominator(10000),
        "tan": lambda x: Fraction(math.tan(math.radians(x))).limit_denominator(10000),
        "sqrt": lambda x: Fraction(math.sqrt(x)).limit_denominator(10000),
        "log": math.log,
        "exp": math.exp,
        "factorial": math.factorial,
        "abs": abs,
        "round": round,
        "pi": math.pi,
        "e": math.e
    }

    try:
        # Replace function names and constants in the expression
        for func in allowed_functions:
            expression = re.sub(rf'\b{func}\b', f"allowed_functions['{func}']", expression)
        
        # Safely evaluate the math expression
        result = eval(expression, {"__builtins__": None}, {"allowed_functions": allowed_functions})
        return f"The result is {result}"
    except Exception as e:
        return "Sorry, I couldn't evaluate that. Please make sure it's a valid mathematical expression."

# Analyze intent based on user input
def analyze_intent(message):
    if any(word in message for word in ["hello", "hi", "hey", "greetings"]):
        return "greeting"
    elif any(word in message for word in ["how", "feeling"]):
        return "feeling"
    elif "name" in message:
        return "name"
    elif "about" in message:
        return "about"
    elif any(word in message for word in ["eat", "eating", "food"]):
        return "eating"
    elif any(word in message for word in ["watching", "watch"]):
        return "watching"
    elif any(word in message for word in ["love", "i"]):
        return "love"
    elif "doing" in message:
        return "doing"
    elif re.match(r'^[\d+\-*/()., %a-z]+$', " ".join(message)):
        return "math"
    else:
        return "fallback"

# Generate response based on user input
def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    intent = analyze_intent(split_message)

    # Handle math specifically
    if intent == "math":
        return evaluate_math_expression(user_input)

    # Generate a dynamic response for conversational intents
    return get_dynamic_response(intent)

# Chatbot interaction loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit', 'bye']:
        print("Bot: Goodbye! Have a Nice Day Buddy. 😊")
        break
    print("Bot:", get_response(user_input))
