"""
Products Repository - CRUD operations for produits table
"""
import mysql.connector
from database.connection import get_connection, close_connection


class ProductsRepository:
    """Handle all product-related database operations"""

    @staticmethod
    def create(nom, categorie_id, fournisseur_id, quantite_stock, prix_unitaire, prix_achat):
        """
        Create a new product
        Returns: product_id if successful, None if failed
        """
        try:
            conn = get_connection('gestion_stock')
            cursor = conn.cursor()

            sql = """INSERT INTO produits (nom, categorie_id, fournisseur_id, quantite_stock, prix_unitaire, prix_achat)
                     VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (nom, categorie_id, fournisseur_id, quantite_stock, prix_unitaire, prix_achat))

            product_id = cursor.lastrowid
            cursor.close()
            close_connection(conn)
            return product_id

        except mysql.connector.Error as e:
            print(f"❌ Error creating product: {e}")
            return None

    @staticmethod
    def read(product_id):
        """
        Get product by ID
        Returns: dict with product data or None
        """
        try:
            conn = get_connection('gestion_stock')
            cursor = conn.cursor(dictionary=True)

            sql = """SELECT p.*, c.nom as categorie_nom, f.nom as fournisseur_nom
                     FROM produits p
                              LEFT JOIN categories c ON p.categorie_id = c.id
                              LEFT JOIN fournisseurs f ON p.fournisseur_id = f.id
                     WHERE p.id = %s"""
            cursor.execute(sql, (product_id,))

            result = cursor.fetchone()
            cursor.close()
            close_connection(conn)
            return result

        except mysql.connector.Error as e:
            print(f"❌ Error reading product: {e}")
            return None

    @staticmethod
    def read_all():
        """
        Get all products with category and supplier names
        Returns: list of dicts
        """
        try:
            conn = get_connection('gestion_stock')
            cursor = conn.cursor(dictionary=True)

            sql = """SELECT p.*, c.nom as categorie_nom, f.nom as fournisseur_nom
                     FROM produits p
                              LEFT JOIN categories c ON p.categorie_id = c.id
                              LEFT JOIN fournisseurs f ON p.fournisseur_id = f.id
                     ORDER BY p.id"""
            cursor.execute(sql)

            result = cursor.fetchall()
            cursor.close()
            close_connection(conn)
            return result if result else []

        except mysql.connector.Error as e:
            print(f"❌ Error reading products: {e}")
            return []

    @staticmethod
    def update(product_id, nom, categorie_id, fournisseur_id, quantite_stock, prix_unitaire, prix_achat):
        """
        Update product information
        Returns: True if successful, False otherwise
        """
        try:
            conn = get_connection('gestion_stock')
            cursor = conn.cursor()

            sql = """UPDATE produits
                     SET nom            = %s, \
                         categorie_id   = %s, \
                         fournisseur_id = %s, \
                         quantite_stock = %s,
                         prix_unitaire  = %s, \
                         prix_achat     = %s
                     WHERE id = %s"""
            cursor.execute(sql,
                           (nom, categorie_id, fournisseur_id, quantite_stock, prix_unitaire, prix_achat, product_id))

            cursor.close()
            close_connection(conn)
            return cursor.rowcount > 0

        except mysql.connector.Error as e:
            print(f"❌ Error updating product: {e}")
            return False

    @staticmethod
    def delete(product_id):
        """
        Delete product by ID
        CASCADE will delete all orders with this product
        Returns: True if successful, False otherwise
        """
        try:
            conn = get_connection('gestion_stock')
            cursor = conn.cursor()

            sql = "DELETE FROM produits WHERE id = %s"
            cursor.execute(sql, (product_id,))

            cursor.close()
            close_connection(conn)
            return cursor.rowcount > 0

        except mysql.connector.Error as e:
            print(f"❌ Error deleting product: {e}")
            return False

    @staticmethod
    def search(search_term):
        """
        Search products by name
        Returns: list of dicts matching the search term
        """
        try:
            conn = get_connection('gestion_stock')
            cursor = conn.cursor(dictionary=True)

            search_param = f"%{search_term}%"
            sql = """SELECT p.*, c.nom as categorie_nom, f.nom as fournisseur_nom
                     FROM produits p
                              LEFT JOIN categories c ON p.categorie_id = c.id
                              LEFT JOIN fournisseurs f ON p.fournisseur_id = f.id
                     WHERE p.nom LIKE %s
                     ORDER BY p.id"""
            cursor.execute(sql, (search_param,))

            result = cursor.fetchall()
            cursor.close()
            close_connection(conn)
            return result if result else []

        except mysql.connector.Error as e:
            print(f"❌ Error searching products: {e}")
            return []

    @staticmethod
    def get_by_category(category_id):
        """
        Get all products in a specific category
        Returns: list of dicts
        """
        try:
            conn = get_connection('gestion_stock')
            cursor = conn.cursor(dictionary=True)

            sql = """SELECT p.*, c.nom as categorie_nom, f.nom as fournisseur_nom
                     FROM produits p
                              LEFT JOIN categories c ON p.categorie_id = c.id
                              LEFT JOIN fournisseurs f ON p.fournisseur_id = f.id
                     WHERE p.categorie_id = %s
                     ORDER BY p.id"""
            cursor.execute(sql, (category_id,))

            result = cursor.fetchall()
            cursor.close()
            close_connection(conn)
            return result if result else []

        except mysql.connector.Error as e:
            print(f"❌ Error getting products by category: {e}")
            return []

    @staticmethod
    def update_quantity(product_id, quantity_change):
        """
        Update product stock quantity (increment/decrement)
        quantity_change: positive to add stock, negative to subtract stock
        Returns: True if successful, False otherwise
        """
        try:
            conn = get_connection('gestion_stock')
            cursor = conn.cursor()

            sql = """UPDATE produits 
                     SET quantite_stock = quantite_stock + %s 
                     WHERE id = %s"""
            cursor.execute(sql, (quantity_change, product_id))

            cursor.close()
            close_connection(conn)
            return cursor.rowcount > 0

        except mysql.connector.Error as e:
            print(f"❌ Error updating product quantity: {e}")
            return False

    @staticmethod
    def get_low_stock(threshold):
        """
        Get products below a stock threshold
        Returns: list of dicts with low stock
        """
        try:
            conn = get_connection('gestion_stock')
            cursor = conn.cursor(dictionary=True)

            sql = """SELECT p.*, c.nom as categorie_nom, f.nom as fournisseur_nom
                     FROM produits p
                              LEFT JOIN categories c ON p.categorie_id = c.id
                              LEFT JOIN fournisseurs f ON p.fournisseur_id = f.id
                     WHERE p.quantite_stock < %s
                     ORDER BY p.quantite_stock ASC"""
            cursor.execute(sql, (threshold,))

            result = cursor.fetchall()
            cursor.close()
            close_connection(conn)
            return result if result else []

        except mysql.connector.Error as e:
            print(f"❌ Error getting low stock products: {e}")
            return []
