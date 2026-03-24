"""
Insert test data
"""
from database.connection import get_connection, close_connection


def insert_data():
    """Insert test data into all tables"""
    conn = get_connection('gestion_stock')
    cursor = conn.cursor()

    try:
        # Insert Fournisseurs
        fournisseurs = [
            ('TechCore Electronics', 'John Smith', 'john.smith@techcore.com', '+33612345678',
             '123 Tech Avenue, Paris, 75001'),
            ('Global Imports Ltd', 'Marie Dupont', 'marie.dupont@globalimports.fr', '+33745678901',
             '456 Business Park, Lyon, 69000'),
            ('Quality Supplies Co', 'Pierre Laurent', 'pierre@qualitysupplies.com', '+33678901234',
             '789 Industrial Zone, Marseille, 13000'),
            ('Premium Products Inc', 'Sophie Martin', 'sophie.martin@premium.fr', '+33712345678',
             '321 Commerce Street, Toulouse, 31000'),
            ('EcoGreen Distributors', 'Marc Benoit', 'marc.benoit@ecogreen.com', '+33634567890',
             '654 Green Valley, Bordeaux, 33000'),
            ('SmartTech Solutions', 'Isabelle Moreau', 'isabelle@smarttech.fr', '+33656789012',
             '987 Innovation Drive, Nantes, 44000'),
            ('Universal Supply Chain', 'Claude Rousseau', 'claude.rousseau@universal.com', '+33698765432',
             '159 Supply Road, Lille, 59000'),
            ('Direct From China', 'Wei Zhang', 'wei@directfromchina.cn', '+33678123456',
             '753 Import Street, Grenoble, 38000'),
        ]
        cursor.executemany(
            "INSERT INTO fournisseurs (nom, contact, email, telephone, adresse) VALUES (%s, %s, %s, %s, %s)",
            fournisseurs
        )
        print(f"✅ Inserted {len(fournisseurs)} suppliers")

        # Insert Categories
        categories = [
            ('Électronique', 'Appareils électriques et électroniques'),
            ('Informatique', 'Ordinateurs, périphériques et accessoires'),
            ('Télécom', 'Téléphones, tablettes et accessoires'),
            ('Électroménager', 'Appareils électroménagers'),
            ('Accessoires', 'Accessoires divers et produits complémentaires'),
            ('Logiciels', 'Licences logicielles et applications'),
            ('Hardware', 'Composants matériels et pièces informatiques'),
        ]
        cursor.executemany(
            "INSERT INTO categories (nom, description) VALUES (%s, %s)",
            categories
        )
        print(f"✅ Inserted {len(categories)} categories")

        # Insert Products
        products = [
            ('Dell Laptop XPS 13', 2, 1, 45, 1299.99, 950.00),
            ('Apple MacBook Pro', 2, 1, 28, 1999.99, 1400.00),
            ('HP Printer LaserJet', 2, 2, 15, 399.99, 280.00),
            ('USB-C Cables (10 pack)', 5, 3, 150, 19.99, 8.00),
            ('Wireless Mouse Logitech', 2, 2, 85, 49.99, 25.00),
            ('Monitor LG 27" 4K', 1, 1, 22, 499.99, 350.00),
            ('Keyboard Mechanical RGB', 5, 3, 60, 129.99, 70.00),
            ('iPhone 15 Pro', 3, 4, 38, 1199.99, 800.00),
            ('Samsung Galaxy S24', 3, 4, 42, 999.99, 650.00),
            ('iPad Air', 3, 2, 25, 749.99, 500.00),
            ('Portable SSD 1TB', 2, 1, 110, 129.99, 75.00),
            ('Network Router WiFi 6', 1, 1, 30, 249.99, 150.00),
            ('Desk Lamp LED', 1, 7, 50, 59.99, 30.00),
            ('Phone Charger Fast 65W', 5, 2, 200, 39.99, 15.00),
            ('Webcam HD 1080p', 5, 2, 40, 79.99, 40.00),
        ]
        cursor.executemany(
            "INSERT INTO produits (nom, categorie_id, fournisseur_id, quantite_stock, prix_unitaire, prix_achat) VALUES (%s, %s, %s, %s, %s, %s)",
            products
        )
        print(f"✅ Inserted {len(products)} products")

        # Insert Orders
        orders = [
            (1, 1, 10, '2024-03-15 09:00:00', '2024-03-22', 9500.00, 'Livrée'),
            (2, 1, 5, '2024-03-16 10:30:00', '2024-03-25', 7000.00, 'Livrée'),
            (3, 2, 8, '2024-03-17 14:15:00', '2024-03-24', 2240.00, 'Livrée'),
            (4, 3, 50, '2024-03-18 11:00:00', '2024-03-21', 400.00, 'Livrée'),
            (5, 2, 25, '2024-03-19 15:45:00', '2024-03-26', 625.00, 'En attente'),
            (6, 1, 12, '2024-03-20 09:15:00', '2024-03-28', 4200.00, 'En attente'),
            (7, 3, 20, '2024-03-21 13:30:00', None, 1400.00, 'En attente'),
            (8, 4, 15, '2024-03-22 10:00:00', '2024-04-01', 12000.00, 'En attente'),
            (9, 4, 18, '2024-03-23 16:20:00', '2024-04-02', 11700.00, 'En attente'),
            (10, 2, 10, '2024-03-24 11:30:00', '2024-04-05', 5000.00, 'Annulée'),
            (11, 1, 30, '2024-03-25 14:00:00', '2024-04-03', 2250.00, 'En attente'),
            (12, 1, 5, '2024-03-26 09:45:00', '2024-04-02', 750.00, 'En attente'),
            (13, 7, 20, '2024-03-24 10:15:00', '2024-03-30', 600.00, 'Livrée'),
            (14, 2, 100, '2024-03-25 13:45:00', '2024-03-31', 1500.00, 'Livrée'),
            (15, 2, 15, '2024-03-26 15:00:00', None, 600.00, 'En attente'),
        ]
        cursor.executemany(
            "INSERT INTO commandes (produit_id, fournisseur_id, quantite, date_commande, date_livraison, prix_total, statut) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            orders
        )
        print(f"✅ Inserted {len(orders)} orders")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close()
        close_connection(conn)
