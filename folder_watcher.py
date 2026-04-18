import time
import os
import requests
import smtplib
from email.message import EmailMessage
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ---------- CONFIG ----------
WATCH_FOLDER = os.path.join(os.getcwd(), "incoming")
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = ""   # leave empty to disable email
EMAIL_RECEIVER = "your_email@gmail.com"

# Create the folder if it doesn't exist
os.makedirs(WATCH_FOLDER, exist_ok=True)

def process_file(file_path):
    """Read file, send to AI, email or save result."""
    print(f"Processing {file_path}...")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Ask AI to summarize
    prompt = f"Summarize the following text:\n\n{content}"
    url = f"https://text.pollinations.ai/prompt?text={prompt}"
    try:
        resp = requests.get(url, timeout=30)
        if resp.status_code == 200:
            ai_result = resp.text.strip()
        else:
            ai_result = f"AI error: status {resp.status_code}"
    except Exception as e:
        ai_result = f"Request failed: {e}"

    # Email or save result
    if EMAIL_PASSWORD:
        msg = EmailMessage()
        msg.set_content(f"Original file: {os.path.basename(file_path)}\n\nAI Summary:\n{ai_result}")
        msg["Subject"] = f"AI Summary for {os.path.basename(file_path)}"
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                server.send_message(msg)
            print("Email sent.")
        except Exception as e:
            print(f"Email failed: {e}")
    else:
        output_file = file_path + ".summary.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(ai_result)
        print(f"Summary saved to {output_file}")

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".txt"):
            time.sleep(1)  # wait for file to finish writing
            process_file(event.src_path)

if __name__ == "__main__":
    print(f"Watching folder: {WATCH_FOLDER}")
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()