from flask import Flask, render_template, request, redirect, url_for, jsonify
import random
from CRM import crm  # Importer le blueprint
import string
import json
import os

app = Flask(__name__)

# Charger les données JSON
DATA_FOLDER = 'data'


# Enregistrer le blueprint
app.register_blueprint(crm)


def load_data(filename):
    with open(os.path.join(DATA_FOLDER, filename), 'r') as file:
        return json.load(file)

def save_data(filename, data):
    with open(os.path.join(DATA_FOLDER, filename), 'w') as file:
        json.dump(data, file, indent=4)

products = load_data('products.json')
clients = load_data('clients.json')
orders = load_data('orders.json')

def generate_product_id():
    prefix = ''.join(random.choices(string.ascii_uppercase, k=2))
    number = str(random.randint(100, 999))
    return f"{prefix}{number}"


@app.after_request
def set_utf8(response):
    response.headers["Content-Type"] = "text/html; charset=utf-8"
    return response



@app.route("/")
def dashboard():
    # Chargement des données depuis les fichiers JSON
    with open("data/products.json", "r") as f:
        products = json.load(f)

    with open("data/clients.json", "r") as f:
        clients = json.load(f)

    with open("data/orders.json", "r") as f:
        orders = json.load(f)
    
  

    # Calcul du nombre total de produits, clients et commandes
    total_products = len(products)  # Nombre total de produits
    total_clients = len(clients)  # Nombre total de clients
    total_orders = len(orders)  # Nombre total de commandes

    # Répartition des commandes par statut
    statuses = [order["status"] for order in orders]
    order_status_labels = ["Livrée", "Annulée", "En cours", "En attente"]
    order_status_counts = [
        statuses.count("Livree"),
        statuses.count("Annulee"),
        statuses.count("En cours"),
        statuses.count("En attente"),
    ]

    # Produits les plus commandés
    product_quantities = {}
    for order in orders:
        product = order["product"]
        quantity = order["quantity"]
        product_quantities[product] = product_quantities.get(product, 0) + quantity

    top_products_labels = list(product_quantities.keys())
    top_products_counts = list(product_quantities.values())

    return render_template(
        "dashboard.html",
        total_products=total_products,
        total_clients=total_clients,
        total_orders=total_orders,
        order_status_labels=order_status_labels,
        order_status_counts=order_status_counts,
        top_products_labels=top_products_labels,
        top_products_counts=top_products_counts,
    )






@app.route('/products')
def product_list():
    return render_template('products.html', products=products)

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        new_product = {
            "id": generate_product_id(),
            "name": request.form['name'],
            "price": float(request.form['price']),
            "stock": int(request.form['stock']),
            "unit": request.form['unit']
        }
        # Ajout au fichier JSON
        products.append(new_product)
        with open('products.json', 'w') as f:
            json.dump(products, f)
        return redirect(url_for('product_list'))
    return render_template('add_product.html')




@app.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    # Chercher le produit par son ID
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return "Produit non trouvé", 404

    if request.method == 'POST':
        # Mettre à jour les données du produit
        product['name'] = request.form['name']
        product['price'] = float(request.form['price'])
        product['stock'] = int(request.form['stock'])
        product['unit'] = request.form['unit']
        # Sauvegarder les modifications dans le fichier JSON
        with open('data/products.json', 'w') as f:
            json.dump(products, f)
        return redirect(url_for('product_list'))

    return render_template('edit_product.html', product=product)


@app.route('/products/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    global products
    # Supprimer le produit par ID
    products = [p for p in products if p['id'] != product_id]
    # Sauvegarder les changements dans le fichier JSON
    with open('data/products.json', 'w') as f:
        json.dump(products, f)
    return redirect(url_for('product_list'))




@app.route('/clients')
def client_list():
    return render_template('clients.html', clients=clients)


@app.route("/marketing")
def marketing_dashboard():
    # Vérifiez si le fichier existe
    if os.path.exists('data/campaigns.json'):
        with open('data/campaigns.json', 'r') as f:
            campaigns = json.load(f)
    else:
        campaigns = []  # Si le fichier n'existe pas, initialisez une liste vide

    # Exemple d'analyse des campagnes
    success_rates = [c["success_rate"] for c in campaigns]

    return render_template(
        "marketing.html",
        campaigns=campaigns,
        success_rates=success_rates
    )


@app.route("/clients/analytics")
def client_analytics():
    # Charger les données des clients
    with open('data/client_orders.json', 'r') as f:
        clients = json.load(f)

    # Comptage par catégories
    categories = ["fidele", "nouveau", "inactif"]
    category_counts = {category: 0 for category in categories}

    for client in clients:
        category = client.get("category", "inconnu").lower()
        if category in category_counts:
            category_counts[category] += 1
        else:
            category_counts["inconnu"] = category_counts.get("inconnu", 0) + 1

    # Convertir dict_values en liste pour éviter les erreurs de sérialisation
    category_counts_list = list(category_counts.values())

    return render_template(
        "client_analytics.html",
        clients=clients,
        category_counts=category_counts_list,
    )





@app.route('/orders')
def order_list():
    # Construire le chemin vers le fichier orders.json dans le dossier data
    orders_file = os.path.join(os.path.dirname(__file__), 'data', 'orders.json')

    # Vérifie si le fichier existe
    if not os.path.exists(orders_file):
        # Créer un fichier vide si nécessaire
        with open(orders_file, 'w') as f:
            json.dump([], f)

    # Charger les commandes
    with open(orders_file, 'r') as f:
        orders = json.load(f)

    # Préparer les données pour le graphe
    clients = [order['client'] for order in orders]
    quantities = [order['quantity'] for order in orders]

    return render_template('orders.html', orders=orders, clients=clients, quantities=quantities)



@app.route('/orders/add', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        new_order = {
            "id": len(orders) + 1,
            "client": request.form['client'],
            "product": request.form['product'],
            "quantity": int(request.form['quantity']),
            "status": "En cours"
        }
        orders.append(new_order)
        save_data('orders.json', orders)
        return redirect(url_for('order_list'))
    return render_template('add_order.html', clients=clients, products=products)

if __name__ == '__main__':
    app.run(debug=True, port="5003")
