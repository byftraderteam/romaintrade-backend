from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "JSON attendu."}), 400

    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if username and password and email:
        # (optionnel : ici tu peux connecter à IBKR)
        return jsonify({"status": "success", "message": "Connexion réussie."})
    else:
        return jsonify({"status": "error", "message": "Tous les champs sont requis."}), 400

if __name__ == '__main__':
    app.run()
