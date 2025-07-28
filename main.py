from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

app = Flask(__name__)

# Config JWT
app.config["JWT_SECRET_KEY"] = "your-secret-key"  # change en vrai mot de passe secret
jwt = JWTManager(app)

# Config Email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'tonemail@gmail.com'  # remplace par ton email
app.config['MAIL_PASSWORD'] = 'motdepasseapp'       # mot de passe d’application
mail = Mail(app)

# Simulons une base de données
users_db = {}

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data['email']
    username = data['username']
    password = generate_password_hash(data['password'])
    seuil_achat = data.get('seuil_achat', '<10')
    users_db[username] = {'email': email, 'password': password, 'seuil_achat': seuil_achat}
    return jsonify({"msg": "Utilisateur enregistré"}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    user = users_db.get(username)
    if not user or not check_password_hash(user['password'], password):
        return jsonify({"msg": "Login invalide"}), 401
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

@app.route('/portfolio', methods=['GET'])
@jwt_required()
def portfolio():
    username = get_jwt_identity()
    user = users_db.get(username)
    portefeuille = {
        "solde": 3280.10,
        "investissement": 1200.00,
        "actions": ["Amazon - 2", "Tesla - 1"]
    }

    # Simulation de bot : gain aléatoire → envoie une alerte
    send_alert_email(user['email'], "+5$ de profit généré sur votre compte.")
    return jsonify({"utilisateur": username, "portefeuille": portefeuille})

def send_alert_email(to_email, message):
    msg = Message("Alerte de Trading 💹", sender=app.config['MAIL_USERNAME'], recipients=[to_email])
    msg.body = message
    mail.send(msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)