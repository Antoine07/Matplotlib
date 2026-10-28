"""Sujet et correction formateur du TP préparatoire à Power BI."""

DATA_FILE = "ventes_reseau_powerbi.csv"
DATA_CODE = '''import pandas as pd
import matplotlib.pyplot as plt

ventes = pd.read_csv(
    "/workspace/data/ventes_reseau_powerbi.csv",
    parse_dates=["Date"]
)
'''
DATA_CHECK = '''ventes.info()
print("Lignes :", len(ventes))
print("Commandes distinctes :", ventes["Commande"].nunique())
print("Période :", ventes["Date"].min(), ventes["Date"].max())
print(ventes.isna().sum())'''

FIELDS = [
    ("Ligne", "Identifiant unique d’une ligne de commande."),
    ("Commande", "Identifiant de commande ; une commande peut contenir plusieurs lignes."),
    ("Date", "Date de commande au format AAAA-MM-JJ."),
    ("Region", "Région commerciale : Nord, Sud, Est ou Ouest."),
    ("Canal", "Canal de vente : Magasin ou En ligne."),
    ("Categorie", "Famille de produits : Maison, Sport, Informatique ou Accessoires."),
    ("Produit", "Produit vendu sur la ligne."),
    ("Quantite", "Nombre d’unités vendues sur la ligne."),
    ("Chiffre_affaires", "Montant de ventes de la ligne, après remise, en euros hors taxes."),
    ("Cout_achat", "Coût d’achat des produits vendus sur la ligne, en euros hors taxes."),
]

VISUALS = [
    ("Évolution mensuelle du chiffre d’affaires",
     "Représentez le chiffre d’affaires total de chaque mois de 2025 dans l’ordre chronologique."),
    ("Marge commerciale rapportée au chiffre d’affaires par catégorie",
     "Comparez les catégories avec un indicateur en pourcentage calculé sur leurs montants totaux."),
]

SOLUTION = '''# La marge commerciale est calculable car le coût d’achat est fourni.
ventes["Marge_commerciale"] = ventes["Chiffre_affaires"] - ventes["Cout_achat"]

# Graphique 1 — chiffre d’affaires mensuel
mensuel = ventes.set_index("Date").resample("MS")["Chiffre_affaires"].sum()
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(mensuel.index, mensuel.values, marker="o", color="#275c47")
ax.set(title="Chiffre d’affaires mensuel en 2025", ylabel="Chiffre d’affaires (€ HT)")
plt.tight_layout()
fig.savefig("/workspace/resultats/tp_01_ca_mensuel.png", dpi=160, bbox_inches="tight")
plt.show()

# Graphique 2 — marge commerciale / chiffre d’affaires par catégorie
categories = ventes.groupby("Categorie")[["Chiffre_affaires", "Marge_commerciale"]].sum()
categories["Marge_sur_CA_pct"] = categories["Marge_commerciale"] / categories["Chiffre_affaires"] * 100
taux_categories = categories["Marge_sur_CA_pct"].sort_values()
fig, ax = plt.subplots(figsize=(8, 4))
ax.barh(taux_categories.index, taux_categories.values, color="#275c47")
ax.set(title="Marge commerciale rapportée aux ventes", xlabel="Marge / chiffre d’affaires (%)")
plt.tight_layout()
fig.savefig("/workspace/resultats/tp_02_marge_categories.png", dpi=160, bbox_inches="tight")
plt.show()

# Valeurs servant à étayer les deux insights
evolution_janvier_decembre = (mensuel.iloc[-1] / mensuel.iloc[0] - 1) * 100
print("CA mensuel :", mensuel.round(2))
print("Évolution janvier-décembre (%) :", round(evolution_janvier_decembre, 2))
print("Bilan par catégorie :", categories.round(2))
'''

INSIGHTS = [
    "Le chiffre d’affaires passe de 21 864,40 € HT en janvier à 54 454,70 € HT en décembre, soit +149,06 %. Cette activité observée en fin d’année invite à anticiper les besoins en stocks et en ressources. Une seule année ne permet pas de conclure à une saisonnalité récurrente.",
    "Les Accessoires affichent une marge commerciale rapportée au chiffre d’affaires de 59,97 %, contre 20,14 % pour l’Informatique. Cette différence invite à étudier la place des accessoires dans l’offre commerciale, en tenant compte de la demande et des volumes. Ce ratio ne tient pas compte des autres charges de l’entreprise.",
]

TP = dict(
    file="tp_binomes",
    title="TP en binômes · préparer un tableau de bord Power BI",
    group="TP en binômes",
    intro="Vous analysez les ventes 2025 du réseau commercial fictif Nova. Préparez avec Pandas et Matplotlib deux graphiques et deux insights pour définir un futur tableau de bord Power BI.",
    question="Comment évolue le chiffre d’affaires et comment la marge commerciale rapportée aux ventes varie-t-elle selon les catégories ?",
    concepts=[],
    data_file=DATA_FILE,
    data_code=DATA_CODE,
    data_check=DATA_CHECK,
    fields=FIELDS,
    visuals=VISUALS,
    insights=INSIGHTS,
    example="ventes.head()",
    reading="Ce jeu pédagogique fictif est distinct de Superstore. Une ligne représente une ligne de commande. Les montants sont exprimés en euros hors taxes ; la marge commerciale correspond au chiffre d’affaires diminué du coût d’achat.",
    setup_solution=SOLUTION,
    exercises=[(
        "Deux graphiques et deux insights",
        "Construisez les deux graphiques du sujet, puis formulez exactement deux insights chiffrés qui expliquent ce que la responsable commerciale peut retenir de l’analyse.",
        "Un notebook reproductible, deux figures PNG et deux insights justifiés par les graphiques.",
        "",
        "\n\n".join(f"Insight {i} — {text}" for i, text in enumerate(INSIGHTS, 1)),
    )],
)

