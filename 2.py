def chatbot():
    print("Hello! I am your friendly chatbot 🤖")
    print("I can remember your preferences like favorite color, hobby, etc.")
    print("Type 'exit' to end the chat.\n")

    memory = {}  # Dictionary to store user preferences

    while True:
        user_input = input("You: ").strip().lower()

        if user_input == "exit":
            print("Bot: Goodbye! I’ll remember our chat 😊")
            break

        # Store preference
        elif user_input.startswith("my"):
            try:
                parts = user_input.split(" is ")
                key = parts[0].replace("my ", "")
                value = parts[1]
                memory[key] = value
                print(f"Bot: Got it! I'll remember your {key} is {value}.")
            except:
                print("Bot: Please use the format: My <preference> is <value>")

        # Recall preference
        elif user_input.startswith("what is my"):
            key = user_input.replace("what is my ", "")
            if key in memory:
                print(f"Bot: Your {key} is {memory[key]}.")
            else:
                print(f"Bot: I don't know your {key} yet.")

        # Show all remembered preferences
        elif user_input == "show my preferences":
            if memory:
                print("Bot: Here’s what I remember about you:")
                for k, v in memory.items():
                    print(f" - {k}: {v}")
            else:
                print("Bot: I don’t have any preferences saved yet.")

        else:
            print("Bot: I didn’t understand that. Try:")
            print("     'My favorite color is blue'")
            print("     'What is my favorite color?'")
            print("     'Show my preferences'")

# Run chatbot
chatbot()
