import os
from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# Sunucu Kilit Durumu (Varsayılan: Açık)
SISTEM_KILITLI = False 

def calisma_saati_mi():
    now = datetime.now()
    gun = now.weekday() # 0-4 Hafta içi, 5-6 Hafta sonu
    saat = now.hour

    if gun in [5, 6]: # Hafta sonu (Cumartesi - Pazar: 13:00 - 20:00)
        return 13 <= saat < 20
    else: # Hafta içi (Pazartesi - Cuma: 19:00 - 21:00)
        return 19 <= saat < 21

@app.route('/durum', methods=['GET'])
def durum_kontrol():
    acik_mi = calisma_saati_mi() and not SISTEM_KILITLI
    return jsonify({
        "siparis_acik": acik_mi,
        "kilitli": SISTEM_KILITLI,
        "mesaj": "Siparişler açık!" if acik_mi else "Şu an sipariş kabul edilmiyor."
    })

@app.route('/kilitle', methods=['POST'])
def kilit_degistir():
    global SISTEM_KILITLI
    data = request.json or {}
    SISTEM_KILITLI = data.get("kilit", True)
    return jsonify({"durum": "Başarılı", "kilitli": SISTEM_KILITLI})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
  
