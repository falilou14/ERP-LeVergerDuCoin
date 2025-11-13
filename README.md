# 🌿 ERP - LeVergeDuCoin

Ce projet est une application **ERP (Enterprise Resource Planning)** développée en **Flask**, permettant de gérer les produits, les clients, les commandes et les campagnes marketing d’une petite entreprise locale.  
Il offre une interface simple, dynamique et extensible pour centraliser la gestion commerciale de LeVergeDuCoin.

---

## 🧠 Description du projet

L’objectif de ce projet est de créer un **mini système de gestion intégré** permettant à une entreprise de :

- Suivre ses **produits** : ajout, modification, suppression et visualisation des stocks.
- Gérer ses **clients** et analyser leur comportement (fidèles, nouveaux, inactifs).
- Administrer ses **commandes**, avec suivi du statut et des produits les plus demandés.
- Superviser les **campagnes marketing** et leurs taux de réussite.
- Visualiser des **statistiques globales** via un tableau de bord dynamique.

L’ensemble des données est stocké sous **format JSON**, rendant le projet portable et facile à exécuter sans base de données externe.

---

## ⚙️ Technologies utilisées

- **Python 3**
- **Flask** (backend & gestion des routes)
- **Jinja2** (templates HTML)
- **JSON** (stockage des données)
- **Bootstrap / Chart.js** (pour l’affichage et les graphiques du tableau de bord)

---

## 🚀 Installation

###  Cloner le dépôt
```bash
git clone https://github.com/<ton-utilisateur>/LeVergeDuCoin.git
cd LeVergeDuCoin

### Créer un environnement virtuel et l'activer 
```bash
python -m venv venv

# Sous macOS / Linux :
source venv/bin/activate

# Sous Windows :
venv\Scripts\activate


###  Installer les dépendances nécessaires
```bash
pip install flask

###  Lancer l’application
```bash
python app.py













