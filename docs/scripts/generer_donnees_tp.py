"""Créer le jeu fictif du TP de préparation à un tableau de bord Power BI."""

from calendar import monthrange
import csv
from datetime import date
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "ventes_reseau_powerbi.csv"
SEED = 20261027

# Prix et coûts unitaires en centimes, montants hors taxes.
PRODUCTS = [
    ("Maison", "Lampe", 6500, 3700),
    ("Maison", "Chaise", 14000, 9500),
    ("Maison", "Étagère", 19000, 12900),
    ("Sport", "Gourde", 2500, 1100),
    ("Sport", "Tapis", 4500, 2300),
    ("Sport", "Sac", 7000, 3800),
    ("Informatique", "Écran", 24000, 19200),
    ("Informatique", "Clavier", 8500, 5500),
    ("Informatique", "Casque", 11000, 7200),
    ("Accessoires", "Câble", 1800, 500),
    ("Accessoires", "Support", 2800, 1000),
    ("Accessoires", "Souris", 3500, 1500),
]
MONTH_ORDERS = [70, 66, 80, 86, 95, 105, 99, 94, 110, 123, 160, 185]
FIELDS = [
    "Ligne", "Commande", "Date", "Region", "Canal", "Categorie",
    "Produit", "Quantite", "Chiffre_affaires", "Cout_achat",
]


def generate():
    rng = random.Random(SEED)
    rows = []
    order_number = 0
    for month, count in enumerate(MONTH_ORDERS, 1):
        for _ in range(count):
            order_number += 1
            day = rng.randint(1, monthrange(2025, month)[1])
            region = rng.choices(["Nord", "Sud", "Est", "Ouest"], weights=[27, 23, 15, 35])[0]
            online_share = 0.34 if month < 10 else 0.56
            channel = "En ligne" if rng.random() < online_share else "Magasin"
            line_count = rng.choices([1, 2, 3], weights=[4, 4, 2])[0]
            weights = [1, 1, 1, 1, 1, 1, 2.2, 2.2, 2.2, 1.5, 1.5, 1.5]
            for _ in range(line_count):
                category, product, price, cost = rng.choices(PRODUCTS, weights=weights)[0]
                quantity = rng.randint(1, 3)
                discount = rng.choice([0, 0, 5, 10]) + (5 if channel == "En ligne" else 0)
                if month in (11, 12):
                    discount += 5
                sales_cents = (quantity * price * (100 - discount) + 50) // 100
                cost_cents = quantity * cost
                rows.append({
                    "Ligne": f"L{len(rows) + 1:05d}",
                    "Commande": f"C2025-{order_number:05d}",
                    "Date": date(2025, month, day).isoformat(),
                    "Region": region,
                    "Canal": channel,
                    "Categorie": category,
                    "Produit": product,
                    "Quantite": quantity,
                    "Chiffre_affaires": f"{sales_cents / 100:.2f}",
                    "Cout_achat": f"{cost_cents / 100:.2f}",
                })
    rows.sort(key=lambda row: (row["Date"], row["Commande"], row["Ligne"]))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} lignes et {order_number} commandes fictives écrites dans {OUTPUT.relative_to(ROOT)}.")


if __name__ == "__main__":
    generate()

