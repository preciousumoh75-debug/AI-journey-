import requests
import os

# File to save conversation
history_file = "chat_history.txt"
system_file = "system_prompt.txt"

# Default system prompt
default_system = "You are a helpful assistant specializing in AI automation."

# Load system prompt if exists
if os.path.exists(system_file):
    with open(system_file, "r", encoding="utf-8") as f:
        system_prompt = f.read().strip()
else:
    system_prompt = default_system
    with open(system_file, "w", encoding="utf-8") as f:
        f.write(system_prompt)

# Conversation list: first message is system prompt
conversation = [{"role": "system", "content": system_prompt}]

# Load previous history if exists
try:
    with open(history_file, "r", encoding="utf-8") as f:
        lines = f.read().strip().split("\n")
        for line in lines:
            if line.startswith("You: "):
                conversation.append({"role": "user", "content": line[5:]})
            elif line.startswith("AI: "):
                conversation.append({"role": "assistant", "content": line[4:]})
except FileNotFoundError:
    pass

print("Chatbot ready! Type 'exit' to quit.")
print("Type '/system' to change the AI's personality.")
print("Type '/history' to show conversation summary.")
print()

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    elif user_input.lower() == "/system":
        print("Current system prompt:")
        print(system_prompt)
        new_prompt = input("Enter new system prompt (or press Enter to keep): ")
        if new_prompt.strip():
            system_prompt = new_prompt.strip()
            # Update the first message in conversation list
            if conversation and conversation[0]["role"] == "system":
                conversation[0]["content"] = system_prompt
            else:
                conversation.insert(0, {"role": "system", "content": system_prompt})
            with open(system_file, "w", encoding="utf-8") as f:
                f.write(system_prompt)
            print("System prompt updated.\n")
        continue
    elif user_input.lower() == "/history":
        print("\n--- Conversation so far ---")
        for msg in conversation[1:]:  # skip system prompt
            print(f"{msg['role'].capitalize()}: {msg['content']}")
        print("--------------------------\n")
        continue

    # Add user message
    conversation.append({"role": "user", "content": user_input})

    # Build prompt for API: system + last few exchanges (up to 10)
    # We'll combine all messages into a single text block
    # Keep only the last 10 exchanges (excluding system) to avoid token limits
    recent = conversation[1:]  # exclude system
    if len(recent) > 10:
        recent = recent[-10:]

    prompt = f"{system_prompt}\n\n"
    for msg in recent:
        prompt += f"{msg['role'].capitalize()}: {msg['content']}\n"
    prompt += "Assistant:"

    url = f"https://text.pollinations.ai/prompt?text={prompt}"

    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            ai_reply = response.text.strip()
            print(f"AI: {ai_reply}\n")
            conversation.append({"role": "assistant", "content": ai_reply})
        else:
            print(f"Error: {response.status_code}\n")
    except Exception as e:
        print(f"Request failed: {e}\n")

# Save conversation to file
with open(history_file, "w", encoding="utf-8") as f:
    for msg in conversation[1:]:  # skip system prompt (we save it separately)
        if msg["role"] == "user":
            f.write(f"You: {msg['content']}\n")
        elif msg["role"] == "assistant":
            f.write(f"AI: {msg['content']}\n")

print("\nChat saved to chat_history.txt. Goodbye!")