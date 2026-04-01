import requests 

prompt = input("What do you want the AI to say? ")

url = f"https://text.pollinations.ai/prompt?text={prompt}"

try:
    response = requests.get(url, timeout=30)
    if response.status_code == 200:
        print("\nAI says:")
        print(response.text.strip())
    else:
        print(f"Error: {response.status_code}")
except Exception as e:
    print(f"Request failed: {e}")