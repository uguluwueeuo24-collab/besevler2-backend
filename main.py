import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # APK ve tarayıcı erişim izni

SISTEM_KILITLI = False

# Ana sayfa isteği (Render ve APK kontrolü için)
@app.route('/', methods=['GET'])
def anasayfa():
    return jsonify({
        "status": "ok",
        "mesaj": "Beşevler Jet Kurye Sunucusu Çalışıyor!"
    })

# Durum kontrolü
@app.route('/durum', methods=['GET'])
def durum_kontrol():
    acik_mi = not SISTEM_KILITLI
    return jsonify({
        "siparis_acik": acik_mi,
        "kilitli": SISTEM_KILITLI,
        "mesaj": "Siparişler açık!" if acik_mi else "Şu an sipariş kabul edilmiyor."
    })

# Kilit değiştirme
@app.route('/kilitle', methods=['POST'])
def kilit_degistir():
    global SISTEM_KILITLI
    data = request.json or {}
    SISTEM_KILITLI = data.get("kilit", True)
    return jsonify({"durum": "Başarılı", "kilitli": SISTEM_KILITLI})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    
