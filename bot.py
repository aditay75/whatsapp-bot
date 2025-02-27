import requests
import json
import os
from flask import Flask, request
from gtts import gTTS

# WhatsApp API Credentials (Replace with your values)
ACCESS_TOKEN = "EAAZAIDDrSZBZBcBOwez7pU7CiUCSmSKWULnZAvjL7u5tJe8jE0V525LZA8jo4U80T54GgVrMJm6CCt0eCFJUMASfm7r8fLzZBuD2WA2vjIPoDY7pIE22FZA2BiQvNUGK1DMIbEZBpLZAT3erz3ayWhdDDalsXbgAi1utCiyrwpakttREBjOT02jrQ1sGO3Q9dF15jAL6qB6QffSjFYcQiHsHIczKRZCd0QdwZDZD"
PHONE_NUMBER_ID = "8010127704"
VERIFY_TOKEN = "start"

# Flask App
app = Flask(__name__)

# Face Exercise Instructions
exercises = {
    "/morning": "Morning Routine:\n1️⃣ Jawline Toner - Open your mouth wide, hold for 5 sec, repeat 10 times.\n"
                "2️⃣ Cheek Lifter - Smile as wide as possible while pressing fingers on cheeks. Hold 5 sec, repeat 10 times.\n"
                "3️⃣ Neck Tightener - Tilt head back, press tongue to roof, hold 5 sec, repeat 10 times.",
    
    "/workout": "Face Workout:\n1️⃣ Fish Face - Suck in cheeks, hold for 10 sec, repeat 10 times.\n"
                "2️⃣ Chin Lifts - Look up, pucker lips, hold 10 sec, repeat 10 times.\n"
                "3️⃣ Eyebrow Lifts - Place fingers above brows, raise brows while resisting. Hold 5 sec, repeat 10 times.",
    
    "/night": "Night Routine:\n1️⃣ Face Massage - Use hands or a roller to massage jawline & cheekbones.\n"
              "2️⃣ Lymphatic Drainage - Gently massage from chin up towards ears.\n"
              "3️⃣ Cold Water Splash - Wash face with cold water to tighten skin."
}

# Function to Send WhatsApp Messages
def send_whatsapp_message(to, text):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
    data = {"messaging_product": "whatsapp", "to": to, "text": {"body": text}}
    requests.post(url, headers=headers, json=data)

# Function to Send Voice Messages
def send_voice_message(to, text):
    tts = gTTS(text=text, lang="en")
    audio_file = "exercise.mp3"
    tts.save(audio_file)
    
    # Upload audio file to a free file host (e.g., file.io, Firebase)
    audio_url = "YOUR_FILE_HOSTING_URL/exercise.mp3"

    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "audio",
        "audio": {"link": audio_url}
    }
    requests.post(url, headers=headers, json=data)

# Webhook for WhatsApp Messages
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Verification Failed", 403

    data = request.get_json()
    if "messages" in data.get("entry", [{}])[0].get("changes", [{}])[0].get("value", {}):
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        sender = message["from"]
        text = message.get("text", {}).get("body", "").lower()

        if text in exercises:
            send_whatsapp_message(sender, exercises[text])
            send_voice_message(sender, exercises[text])  # Send voice guide

    return "OK", 200

# Run Flask App
if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000, debug=True)
