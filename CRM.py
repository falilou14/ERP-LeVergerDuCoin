from flask import Blueprint, render_template, request, redirect, url_for
import json

crm = Blueprint("crm", __name__)

# Charger les clients et interactions
with open('data/clients.json', 'r') as f:
    clients = json.load(f)

with open('data/interactions.json', 'r') as f:
    interactions = json.load(f)
    
    

@crm.route("/clients/<client_id>/interactions")
def client_interactions(client_id):
    client = next((c for c in clients if c["id"] == client_id), None)
    client_interactions = next((i["interactions"] for i in interactions if i["client_id"] == client_id), [])
    return render_template("interactions.html", client=client, interactions=client_interactions)

@crm.route("/clients/<client_id>/interactions/add", methods=["POST"])
def add_interaction(client_id):
    interaction_type = request.form["type"]
    note = request.form["note"]
    new_interaction = {"date": "2025-01-25", "type": interaction_type, "note": note}

    for i in interactions:
        if i["client_id"] == client_id:
            i["interactions"].append(new_interaction)
            break
    else:
        interactions.append({"client_id": client_id, "interactions": [new_interaction]})

    # Sauvegarder dans le fichier JSON
    with open('data/interactions.json', 'w') as f:
        json.dump(interactions, f)
        
        
        

    return redirect(url_for('crm.client_interactions', client_id=client_id))
