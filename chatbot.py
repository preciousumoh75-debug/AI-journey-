import requests
import os

history_file = "chat_history.txt"
system_file = "system_prompt.txt"
default_system = "You are a helpful assistant specializing in AI automation. You can answer weather questions by fetching real data."

if os.path.exists(system_file):
    with open(system_file, "r", encoding="utf-8") as f:
        system_prompt = f.read().strip()
else:
    system_prompt = default_system
    with open(system_file, "w", encoding="utf-8") as f:
        f.write(system_prompt)

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

def get_weather(city="Ikot Ekpene"):
    """Fetch weather from wttr.in"""
    url = f"http://wttr.in/{city}?format=%l:+%t+%C"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.text.strip()
        else:
            return f"Weather service returned status {response.status_code}."
    except Exception as e:
        return f"Error fetching weather: {e}"

print("Chatbot ready! Type 'exit' to quit.")
print("Type '/system' to change the AI's personality.")
print("Type '/history' to show conversation summary.")
print("Ask about weather and I'll fetch it!\n")

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
        for msg in conversation[1:]:
            print(f"{msg['role'].capitalize()}: {msg['content']}")
        print("--------------------------\n")
        continue

    # Check if user is asking about weather
    lower_input = user_input.lower()
    if "weather" in lower_input or "temperature" in lower_input or "rain" in lower_input or "forecast" in lower_input:
        # Extract city if mentioned (simple heuristic)
        words = user_input.split()
        city = "Ikot Ekpene"  # default
        for w in words:
            if w.istitle() and len(w) > 2 and w.lower() not in ["what", "the", "weather", "temperature", "rain", "forecast"]:
                city = w
                break
        weather_info = get_weather(city)
        print(f"AI: {weather_info}\n")
        conversation.append({"role": "user", "content": user_input})
        conversation.append({"role": "assistant", "content": weather_info})
        continue

    # Otherwise, use the AI generator
    conversation.append({"role": "user", "content": user_input})

    # Build prompt from recent messages (excluding system, keep last 10 exchanges)
    recent = conversation[1:]  # skip system
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

# Save conversation
with open(history_file, "w", encoding="utf-8") as f:
    for msg in conversation[1:]:
        if msg["role"] == "user":
            f.write(f"You: {msg['content']}\n")
        elif msg["role"] == "assistant":
            f.write(f"AI: {msg['content']}\n")

print("\nChat saved to chat_history.txt. Goodbye!")