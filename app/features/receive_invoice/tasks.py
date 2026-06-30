import requests
import base64  # <--- Importa esto al inicio

def process_invoice_async(message_content: dict, sender: str, message_id: str):
    url_evolution = "https://demo-humaniz-evolution-api-gateway.onrender.com/chat/getBase64FromMediaMessage/my_first_test"
    headers = {
        "apikey": "MySecureInvoiceToken2026",
        "Content-Type": "application/json"
    }
    payload = { "message": message_content }
    
    response = requests.post(url_evolution, json=payload, headers=headers)
    
    if response.ok:
        base64_data = response.json().get("base64") 
        print(f"[Task] Successfully downloaded image buffer from message {message_id}")
        
        #1. Converts the Base64 text back into binary image bytes.
        image_bytes = base64.b64decode(base64_data)
        
        # 2. Creates a physical file (e.g., factura_584128050120.jpg).
        filename = f"factura_{message_id}.jpg"
        with open(filename, "wb") as file:
            file.write(image_bytes)
            
        print(f"[Task] ¡Imagen guardada físicamente en el servidor como: {filename}!")
        
        return base64_data
    else:
        print(f"[Task] Failed to download media from Evolution API. Status: {response.status_code}")