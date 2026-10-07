from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # APK ve mobil istek izinlerini açar

# Global kilit durumu
kilitli_mi = False

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "ok", "message": "Besevler Jet Kurye Sunucusu Aktif!"})

@app.route('/durum', methods=['GET'])
def durum():
    return jsonify({
        "siparis_acik": not kilitli_mi,
        "kilitli": kilitli_mi
    })

@app.route('/kilitle', methods=['POST'])
def kilitle():
    global kilitli_mi
    data = request.get_json() or {}
    kilitli_mi = data.get('kilit', not kilitli_mi)
    return jsonify({"success": True, "kilitli": kilitli_mi})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
