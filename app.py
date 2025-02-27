# app.py - Initialise l'application Flask et enregistre les routes
from flask import Flask
from routes import bp  # Import des routes

app = Flask(__name__)

# Enregistrement des routes dans l'application
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True, port=8080)  # Lancer le serveur
