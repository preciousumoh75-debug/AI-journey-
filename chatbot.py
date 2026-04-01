import requests

#file to save conversation
history_file = "chat_history.txt"

#Initialize conversation list
conversation = []

#Load previous history if exists
try:
    with open(history_file, "r", encoding="utf-8") as f:
        lines = f.read().strip().split("\n")
        for line in lines:
            if line.startswith("You:"):
                conversation.append({"role": "user", "content": line[4:]})
except FileNotFoundError:
        pass
print("Chatbot ready! type 'exit' to quit.")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    #Add user message to history
    conversation.append({"role": "user", "content": user_input})
    #Build prompt from last few exchanges (up to 10 messages to keep it short)
    prompt = ""
    for message in conversation[-10:]:
        prompt += f"{message['role']}: {message['content']}\n"
    prompt += "assistant:"
    #Call API to get response
    url = "https://text.pollinations.ai/prompt?text={prompt}"
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            ai_reply = response.text.strip()
            print(f"A: {ai_reply}")
            #Add AI response to conversation
            conversation.append({"role": "assistant", "content": ai_reply})
        else:
            print(f"Error: {response.status_code}\n")
    except Exception as e:
        print(f"Request failed: {e}\n")
    
    #Save conversation to file
    with open(history_file, "w", encoding="utf-8") as f:
        for message in conversation:
            if message["role"] == "user":
                f.write(f"You: {message['content']}\n")
            else:
                f.write(f"AI: {message['content']}\n")
    
    print("\nChat saved to chat_history.txt. Goodbye!")