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
    ("Chiffre d’affaires par région",
     "Comparez les quatre régions dans un graphique trié."),
    ("Marge commerciale rapportée au chiffre d’affaires par catégorie",
     "Comparez les catégories avec un indicateur en pourcentage calculé sur leurs montants totaux."),
    ("Chiffre d’affaires et marge commerciale par canal",
     "Comparez les deux canaux avec des barres groupées, en euros, pour les ventes et la marge commerciale."),
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

# Graphique 2 — chiffre d’affaires régional
ca_regions = ventes.groupby("Region")["Chiffre_affaires"].sum().sort_values()
fig, ax = plt.subplots(figsize=(8, 4))
ax.barh(ca_regions.index, ca_regions.values, color="#275c47")
ax.set(title="Chiffre d’affaires par région", xlabel="Chiffre d’affaires (€ HT)")
plt.tight_layout()
fig.savefig("/workspace/resultats/tp_02_ca_regions.png", dpi=160, bbox_inches="tight")
plt.show()

# Graphique 3 — marge commerciale / chiffre d’affaires par catégorie
categories = ventes.groupby("Categorie")[["Chiffre_affaires", "Marge_commerciale"]].sum()
categories["Marge_sur_CA_pct"] = categories["Marge_commerciale"] / categories["Chiffre_affaires"] * 100
taux_categories = categories["Marge_sur_CA_pct"].sort_values()
fig, ax = plt.subplots(figsize=(8, 4))
ax.barh(taux_categories.index, taux_categories.values, color="#275c47")
ax.set(title="Marge commerciale rapportée aux ventes", xlabel="Marge / chiffre d’affaires (%)")
plt.tight_layout()
fig.savefig("/workspace/resultats/tp_03_marge_categories.png", dpi=160, bbox_inches="tight")
plt.show()

# Graphique 4 — comparaison des deux mesures par canal
canaux = ventes.groupby("Canal")[["Chiffre_affaires", "Marge_commerciale"]].sum()
y = range(len(canaux))
fig, ax = plt.subplots(figsize=(9, 4))
b1 = ax.barh([i + 0.18 for i in y], canaux["Chiffre_affaires"], height=0.36, label="Chiffre d’affaires", color="#275c47")
b2 = ax.barh([i - 0.18 for i in y], canaux["Marge_commerciale"], height=0.36, label="Marge commerciale", color="#b5cf66")
ax.set_yticks(list(y), canaux.index)
ax.set(title="Ventes et marge commerciale par canal", xlabel="Montant (€ HT)")
ax.legend()
plt.tight_layout()
fig.savefig("/workspace/resultats/tp_04_canaux.png", dpi=160, bbox_inches="tight")
plt.show()

# Valeurs servant à étayer les deux insights
evolution_janvier_decembre = (mensuel.iloc[-1] / mensuel.iloc[0] - 1) * 100
canaux["Marge_sur_CA_pct"] = canaux["Marge_commerciale"] / canaux["Chiffre_affaires"] * 100
print("CA mensuel :", mensuel.round(2))
print("Évolution janvier-décembre (%) :", round(evolution_janvier_decembre, 2))
print("Bilan par canal :", canaux.round(2))
'''

INSIGHTS = [
    "Le chiffre d’affaires passe de 21 864,40 € HT en janvier à 54 454,70 € HT en décembre, soit +149,06 %. Cette activité observée en fin d’année invite à anticiper les besoins en stocks et en ressources. Une seule année ne permet pas de conclure à une saisonnalité récurrente.",
    "Le canal Magasin réalise 244 662,55 € HT de ventes pour 71 445,55 € HT de marge commerciale, soit 29,20 % du chiffre d’affaires. En ligne, le ratio est de 23,90 %, soit 5,30 points de moins. Il faut examiner le mix produits et les remises avant de décider comment développer ce canal ; les graphiques seuls n’expliquent pas cet écart.",
]

TP = dict(
    file="tp_binomes",
    title="TP en binômes · préparer un tableau de bord Power BI",
    group="TP en binômes",
    intro="Vous analysez les ventes 2025 du réseau commercial fictif Nova. Préparez avec Pandas et Matplotlib quatre graphiques et deux insights pour définir un futur tableau de bord Power BI.",
    question="Comment les ventes et la marge commerciale varient-elles dans le temps, selon les régions, les catégories et les canaux ?",
    concepts=[],
    data_file=DATA_FILE,
    data_code=DATA_CODE,
    data_check=DATA_CHECK,
    fields=FIELDS,
    visuals=VISUALS,
    insights=INSIGHTS,
    optional_question={
        "title": "Croiser région et canal",
        "prompt": "Le canal qui présente le plus fort ratio marge commerciale/chiffre d’affaires est-il le même dans toutes les régions ? Justifiez votre réponse avec un tableau de calculs.",
        "solution": '''bilan_region_canal = ventes.groupby(["Region", "Canal"])[["Chiffre_affaires", "Marge_commerciale"]].sum()
bilan_region_canal["Marge_sur_CA_pct"] = bilan_region_canal["Marge_commerciale"] / bilan_region_canal["Chiffre_affaires"] * 100
print(bilan_region_canal[["Marge_sur_CA_pct"]].round(2))''',
        "answer": "Magasin présente le ratio le plus élevé dans les quatre régions : Est (28,09 % contre 23,28 % en ligne), Nord (29,72 % contre 25,50 %), Ouest (28,32 % contre 23,64 %) et Sud (30,89 % contre 22,98 %). La comparaison reste descriptive ; elle ne démontre pas la cause des écarts.",
    },
    example="ventes.head()",
    reading="Ce jeu pédagogique fictif est distinct de Superstore. Une ligne représente une ligne de commande. Les montants sont exprimés en euros hors taxes ; la marge commerciale correspond au chiffre d’affaires diminué du coût d’achat.",
    setup_solution=SOLUTION,
    exercises=[(
        "Quatre graphiques et deux insights",
        "Construisez les quatre graphiques du sujet, puis formulez exactement deux insights chiffrés qui expliquent ce que la responsable commerciale peut retenir de l’analyse.",
        "Un notebook reproductible, quatre figures PNG et deux insights justifiés par les graphiques.",
        "",
        "\n\n".join(f"Insight {i} — {text}" for i, text in enumerate(INSIGHTS, 1)),
    )],
)

