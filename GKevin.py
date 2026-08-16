import requests

# Aho ubutumwa bwakirwa na POST:
data = request.json
try:
    # Gukuramo ubutumwa n' nimero y'uwabwoherereje binyuze kuri Meta Webhook payload
    entry = data.get('entry', [])
    if entry:
        changes = entry[0].get('changes', [])
        if changes:
            value = changes[0].get('value', {})
            messages = value.get('messages', [])
            if messages:
                sender_phone = messages[0].get('from') # Nimero y'uwanditse
                incoming_msg = messages[0].get('text', {}).get('body', '') # Ubutumwa bwe
                
                if incoming_msg:
                    # 1. Guhamagara Groq AI ngo itange igisubizo
                    api_key = os.getenv("GROQ_API_KEY") or "gsk_..."
                    groq_client = Groq(api_key=api_key)
                    completion = groq_client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "You are GKevin AI, an AI assistant speaking Kinyarwanda."},
                            {"role": "user", "content": incoming_msg}
                        ]
                    ]
                    ai_reply = completion.choices[0].message.content
                    
                    # 2. Kohereza igisubizo kuri WhatsApp ukoresha Meta Graph API
                    WHATSAPP_TOKEN = os.getenv("WHTS_ACCESS_TOKEN", "SHYIRAMO_ACCESS_TOKEN_YAWE_HANO")
                    PHONE_NUMBER_ID = "1230588350137931" # ID yawe wabonye kuri ifoto
                    
                    headers = {
                        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
                        "Content-Type": "application/json"
                    }
                    payload = {
                        "messaging_product": "whatsapp",
                        "to": sender_phone,
                        "text": {"body": ai_reply}
                    }
                    
                    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
                    requests.post(url, json=payload, headers=headers)

except Exception as e:
    print(f"Ikibazo cyabaye: {e}")
