"""
Orders Repository - CRUD operations for commandes table
"""
import mysql.connector
from database.connection import get_connection, close_connection


class OrdersRepository:
    """Handle all order-related database operations"""

    @staticmethod
    def create(produit_id, fournisseur_id, quantite, date_livraison, prix_total, statut='En attente'):
        """
        Create a new order
        Returns: order_id if successful, None if failed
        """
        try:
            conn = get_connection('gestion_stock')
            cursor = conn.cursor()

            sql = """INSERT INTO commandes (produit_id, fournisseur_id, quantite, date_livraison, prix_total, statut) 
                     VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (produit_id, fournisseur_id, quantite, date_livraison, prix_total, statut))

            order_id = cursor.lastrowid
            cursor.close()
            close_connection(conn)
            return order_id

        except mysql.connector.Error as e:
            print(f"❌ Error creating order: {e}")
            return None

    @staticmethod
    def read(order_id):
        """
        Get order by ID with related product and supplier info
        Returns: dict with order data or None
        """
        try:
            conn = get_connection('gestion_stock')
            cursor = conn.cursor(dictionary=True)

            sql = """SELECT c.*, p.nom as produit_nom, f.nom as fournisseur_nom 
                     FROM commandes c
                     LEFT JOIN produits p ON c.produit_id = p.id
                     LEFT JOIN fournisseurs f ON c.fournisseur_id = f.id
                     WHERE c.id = %s"""
            cursor.execute(sql, (order_id,))

            result = cursor.fetchone()
            cursor.close()
            close_connection(conn)
            return result

        except mysql.connector.Error as e:
            print(f"❌ Error reading order: {e}")
            return None

    @staticmethod
    def read_all():
        """
        Get all orders with product and supplier names
        Returns: list of dicts
        """
        try:
            conn = get_connection('gestion_stock')
            cursor = conn.cursor(dictionary=True)

            sql = """SELECT c.*, p.nom as produit_nom, f.nom as fournisseur_nom 
                     FROM commandes c
                     LEFT JOIN produits p ON c.produit_id = p.id
                     LEFT JOIN fournisseurs f ON c.fournisseur_id = f.id
                     ORDER BY c.date_commande DESC"""
            cursor.execute(sql)

            result = cursor.fetchall()
            cursor.close()
            close_connection(conn)
            return result if result else []

        except mysql.connector.Error as e:
            print(f"❌ Error reading orders: {e}")
            return []

    @staticmethod
    def update(order_id, produit_id, fournisseur_id, quantite, date_livraison, prix_total, statut):
        """
        Update order information
        Returns: True if successful, False otherwise
        """
        try:
            conn = get_connection('gestion_stock')
            cursor = conn.cursor()

            sql = """UPDATE commandes 
                     SET produit_id = %s, fournisseur_id = %s, quantite = %s, 
                         date_livraison = %s, prix_total = %s, statut = %s 
                     WHERE id = %s"""
            cursor.execute(sql, (produit_id, fournisseur_id, quantite, date_livraison, prix_total, statut, order_id))

            cursor.close()
            close_connection(conn)
            return cursor.rowcount > 0

        except mysql.connector.Error as e:
            print(f"❌ Error updating order: {e}")
            return False

    @staticmethod
    def delete(order_id):
        """
        Delete order by ID
        Returns: True if successful, False otherwise
        """
        try:
            conn = get_connection('gestion_stock')
            cursor = conn.cursor()

            sql = "DELETE FROM commandes WHERE id = %s"
            cursor.execute(sql, (order_id,))

            cursor.close()
            close_connection(conn)
            return cursor.rowcount > 0

        except mysql.connector.Error as e:
            print(f"❌ Error deleting order: {e}")
            return False

    @staticmethod
    def search(search_term):
        """
        Search orders by product or supplier name
        Returns: list of dicts matching the search term
        """
        try:
            conn = get_connection('gestion_stock')
            cursor = conn.cursor(dictionary=True)

            search_param = f"%{search_term}%"
            sql = """SELECT c.*, p.nom as produit_nom, f.nom as fournisseur_nom 
                     FROM commandes c
                     LEFT JOIN produits p ON c.produit_id = p.id
                     LEFT JOIN fournisseurs f ON c.fournisseur_id = f.id
                     WHERE p.nom LIKE %s OR f.nom LIKE %s
                     ORDER BY c.date_commande DESC"""
            cursor.execute(sql, (search_param, search_param))

            result = cursor.fetchall()
            cursor.close()
            close_connection(conn)
            return result if result else []

        except mysql.connector.Error as e:
            print(f"❌ Error searching orders: {e}")
            return []

    @staticmethod
    def get_by_supplier(supplier_id):
        """
        Get all orders for a specific supplier
        Returns: list of dicts
        """
        try:
            conn = get_connection('gestion_stock')
            cursor = conn.cursor(dictionary=True)

            sql = """SELECT c.*, p.nom as produit_nom, f.nom as fournisseur_nom 
                     FROM commandes c
                     LEFT JOIN produits p ON c.produit_id = p.id
                     LEFT JOIN fournisseurs f ON c.fournisseur_id = f.id
                     WHERE c.fournisseur_id = %s
                     ORDER BY c.date_commande DESC"""
            cursor.execute(sql, (supplier_id,))

            result = cursor.fetchall()
            cursor.close()
            close_connection(conn)
            return result if result else []

        except mysql.connector.Error as e:
            print(f"❌ Error getting orders by supplier: {e}")
            return []

    @staticmethod
    def get_by_product(product_id):
        """
        Get all orders for a specific product
        Returns: list of dicts
        """
        try:
            conn = get_connection('gestion_stock')
            cursor = conn.cursor(dictionary=True)

            sql = """SELECT c.*, p.nom as produit_nom, f.nom as fournisseur_nom 
                     FROM commandes c
                     LEFT JOIN produits p ON c.produit_id = p.id
                     LEFT JOIN fournisseurs f ON c.fournisseur_id = f.id
                     WHERE c.produit_id = %s
                     ORDER BY c.date_commande DESC"""
            cursor.execute(sql, (product_id,))

            result = cursor.fetchall()
            cursor.close()
            close_connection(conn)
            return result if result else []

        except mysql.connector.Error as e:
            print(f"❌ Error getting orders by product: {e}")
            return []

    @staticmethod
    def update_status(order_id, new_status):
        """
        Update only the order status
        Returns: True if successful, False otherwise
        """
        try:
            conn = get_connection('gestion_stock')
            cursor = conn.cursor()

            sql = "UPDATE commandes SET statut = %s WHERE id = %s"
            cursor.execute(sql, (new_status, order_id))

            cursor.close()
            close_connection(conn)
            return cursor.rowcount > 0

        except mysql.connector.Error as e:
            print(f"❌ Error updating order status: {e}")
            return False
