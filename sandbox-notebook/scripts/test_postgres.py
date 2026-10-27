"""Test de connexion réel depuis Jupyter : authentification et requête SQL."""
import os

import psycopg
from psycopg.rows import dict_row


def verifier_connexion():
    config = {
        "host": os.environ.get("PGHOST", "postgres"),
        "port": os.environ.get("PGPORT", "5432"),
        "dbname": os.environ.get("PGDATABASE", "formation"),
        "user": os.environ.get("PGUSER", "apprenant"),
        "password": os.environ.get("PGPASSWORD"),
        "connect_timeout": 5,
        "options": "-c statement_timeout=5000 -c default_transaction_read_only=on",
    }
    if not config["password"]:
        raise RuntimeError(
            "PGPASSWORD absent. Lancez ce test dans le service notebook de Docker Compose."
        )

    try:
        with psycopg.connect(**config, row_factory=dict_row) as connexion:
            resultat = connexion.execute(
                "SELECT current_database() AS base, current_user AS utilisateur, "
                "version() AS version, 1 + 1 AS resultat"
            ).fetchone()
    except psycopg.Error:
        raise RuntimeError(
            "Connexion ou requête PostgreSQL impossible. Vérifiez docker compose ps, "
            "docker compose logs postgres et les variables PG*. "
            "Depuis Jupyter Docker, PGHOST doit être postgres, pas localhost."
        ) from None

    if (
        resultat is None
        or resultat["resultat"] != 2
        or resultat["base"] != config["dbname"]
        or resultat["utilisateur"] != config["user"]
    ):
        raise RuntimeError("La réponse SQL ne correspond pas à la connexion attendue.")

    print("Connexion PostgreSQL OK")
    print(f"Serveur : {config['host']}:{config['port']}")
    print(f"Base : {resultat['base']} | Utilisateur : {resultat['utilisateur']}")
    print(f"Test SQL : 1 + 1 = {resultat['resultat']}")
    print(resultat["version"])
    return resultat


if __name__ == "__main__":
    verifier_connexion()
