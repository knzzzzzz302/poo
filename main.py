from flask import Flask, render_template
from src.routes.user_routes import user_bp
from src.routes.product_routes import product_bp
from src.routes.cart_routes import cart_bp
from src.routes.order_routes import order_bp
from src.services.user_service import UserService
from src.services.product_service import ProductService
from src.models.user import RegularUser, PremiumUser
import logging

logging.basicConfig(level=logging.INFO,
format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(product_bp, url_prefix='/products')
app.register_blueprint(cart_bp, url_prefix='/cart')
app.register_blueprint(order_bp, url_prefix='/orders')

user_service = UserService()
product_service = ProductService()

@app.route('/')
def index():
    products = product_service.get_all_products()
    return render_template('index.html', products=products)

def add_demo_data():
    try:
        user1 = user_service.register("user1", "user1@example.com", "Password123!", "regular")
        user2 = user_service.register("user2", "user2@example.com", "Password123!", "premium")
        
        product_service.add_product("Smartphone", "Un smartphone de dernière génération", 799.99, 10)
        product_service.add_product("Ordinateur portable", "Ordinateur portable pour professionnels", 1299.99, 5)
        product_service.add_product("Casque audio", "Casque audio sans fil", 199.99, 20)
        logger.info("Données de démonstration ajoutées avec succès.")
    except Exception as e:
        logger.error(f"Erreur lors de l'ajout des données de démonstration: {str(e)}")
        raise

if __name__ == '__main__':
    print("Ajout de données de démonstration...")
    try:
        add_demo_data()
    except Exception as e:
        print(f"Erreur lors de l'ajout des données de démonstration: {str(e)}")
        
    app.run(debug=True)