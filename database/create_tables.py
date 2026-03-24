"""
Create database and tables
"""
from database.connection import get_connection, close_connection


def create_database():
    """Create the database"""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS gestion_stock CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("✅ Database created")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close()
        close_connection(conn)


def create_tables():
    """Create all tables"""
    conn = get_connection('gestion_stock')
    cursor = conn.cursor()

    try:
        # Fournisseurs
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS fournisseurs
                       (
                           id
                           INT
                           AUTO_INCREMENT
                           PRIMARY
                           KEY,
                           nom
                           VARCHAR
                       (
                           100
                       ) UNIQUE NOT NULL,
                           contact VARCHAR
                       (
                           100
                       ),
                           email VARCHAR
                       (
                           100
                       ) UNIQUE,
                           telephone VARCHAR
                       (
                           20
                       ),
                           adresse TEXT,
                           date_creation DATETIME DEFAULT CURRENT_TIMESTAMP
                           )
                       """)
        print("✅ Table fournisseurs created")

        # Categories
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS categories
                       (
                           id
                           INT
                           AUTO_INCREMENT
                           PRIMARY
                           KEY,
                           nom
                           VARCHAR
                       (
                           100
                       ) UNIQUE NOT NULL,
                           description TEXT,
                           date_creation DATETIME DEFAULT CURRENT_TIMESTAMP
                           )
                       """)
        print("✅ Table categories created")

        # Produits
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS produits
                       (
                           id
                           INT
                           AUTO_INCREMENT
                           PRIMARY
                           KEY,
                           nom
                           VARCHAR
                       (
                           100
                       ) NOT NULL,
                           categorie_id INT NOT NULL,
                           fournisseur_id INT NOT NULL,
                           quantite_stock INT NOT NULL DEFAULT 0,
                           prix_unitaire DECIMAL
                       (
                           10,
                           2
                       ),
                           prix_achat DECIMAL
                       (
                           10,
                           2
                       ),
                           date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
                           FOREIGN KEY
                       (
                           categorie_id
                       ) REFERENCES categories
                       (
                           id
                       ) ON DELETE CASCADE,
                           FOREIGN KEY
                       (
                           fournisseur_id
                       ) REFERENCES fournisseurs
                       (
                           id
                       )
                         ON DELETE CASCADE
                           )
                       """)
        print("✅ Table produits created")

        # Commandes
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS commandes
                       (
                           id
                           INT
                           AUTO_INCREMENT
                           PRIMARY
                           KEY,
                           produit_id
                           INT
                           NOT
                           NULL,
                           fournisseur_id
                           INT
                           NOT
                           NULL,
                           quantite
                           INT
                           NOT
                           NULL,
                           date_commande
                           DATETIME
                           DEFAULT
                           CURRENT_TIMESTAMP,
                           date_livraison
                           DATE,
                           prix_total
                           DECIMAL
                       (
                           10,
                           2
                       ),
                           statut ENUM
                       (
                           'En attente',
                           'Livrée',
                           'Annulée'
                       ) DEFAULT 'En attente',
                           FOREIGN KEY
                       (
                           produit_id
                       ) REFERENCES produits
                       (
                           id
                       ) ON DELETE CASCADE,
                           FOREIGN KEY
                       (
                           fournisseur_id
                       ) REFERENCES fournisseurs
                       (
                           id
                       )
                         ON DELETE CASCADE
                           )
                       """)
        print("✅ Table commandes created")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close()
        close_connection(conn)
