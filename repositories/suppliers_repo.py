"""
Suppliers Repository - CRUD operations for fournisseurs table
"""
import mysql.connector
from database.connection import get_connection, close_connection


class SuppliersRepository:
    """Handle all supplier-related database operations"""

    @staticmethod
    def create(nom, contact, email, telephone, adresse):
        """
        Create a new supplier
        Returns: supplier_id if successful, None if failed
        """
        try:
            conn = get_connection('gestion_stock')
            cursor = conn.cursor()

            sql = "INSERT INTO fournisseurs (nom, contact, email, telephone, adresse) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (nom, contact, email, telephone, adresse))

            supplier_id = cursor.lastrowid
            cursor.close()
            close_connection(conn)
            return supplier_id

        except mysql.connector.Error as e:
            print(f"❌ Error creating supplier: {e}")
            return None

    @staticmethod
    def read(supplier_id):
        """
        Get supplier by ID
        Returns: dict with supplier data or None
        """
        try:
            conn = get_connection('gestion_stock')
            cursor = conn.cursor(dictionary=True)

            sql = "SELECT * FROM fournisseurs WHERE id = %s"
            cursor.execute(sql, (supplier_id,))

            result = cursor.fetchone()
            cursor.close()
            close_connection(conn)
            return result

        except mysql.connector.Error as e:
            print(f"❌ Error reading supplier: {e}")
            return None

    @staticmethod
    def read_all():
        """
        Get all suppliers
        Returns: list of dicts
        """
        try:
            conn = get_connection('gestion_stock')
            cursor = conn.cursor(dictionary=True)

            sql = "SELECT * FROM fournisseurs ORDER BY nom"
            cursor.execute(sql)

            result = cursor.fetchall()
            cursor.close()
            close_connection(conn)
            return result if result else []

        except mysql.connector.Error as e:
            print(f"❌ Error reading suppliers: {e}")
            return []

    @staticmethod
    def update(supplier_id, nom, contact, email, telephone, adresse):
        """
        Update supplier information
        Returns: True if successful, False otherwise
        """
        try:
            conn = get_connection('gestion_stock')
            cursor = conn.cursor()

            sql = "UPDATE fournisseurs SET nom = %s, contact = %s, email = %s, telephone = %s, adresse = %s WHERE id = %s"
            cursor.execute(sql, (nom, contact, email, telephone, adresse, supplier_id))

            cursor.close()
            close_connection(conn)
            return cursor.rowcount > 0

        except mysql.connector.Error as e:
            print(f"❌ Error updating supplier: {e}")
            return False

    @staticmethod
    def delete(supplier_id):
        """
        Delete supplier by ID
        Returns: True if successful, False otherwise
        """
        try:
            conn = get_connection('gestion_stock')
            cursor = conn.cursor()

            sql = "DELETE FROM fournisseurs WHERE id = %s"
            cursor.execute(sql, (supplier_id,))

            cursor.close()
            close_connection(conn)
            return cursor.rowcount > 0

        except mysql.connector.Error as e:
            print(f"❌ Error deleting supplier: {e}")
            return False

    @staticmethod
    def search(search_term):
        """
        Search suppliers by name or contact
        Returns: list of dicts matching the search term
        """
        try:
            conn = get_connection('gestion_stock')
            cursor = conn.cursor(dictionary=True)

            search_param = f"%{search_term}%"
            sql = "SELECT * FROM fournisseurs WHERE nom LIKE %s OR contact LIKE %s OR email LIKE %s ORDER BY nom"
            cursor.execute(sql, (search_param, search_param, search_param))

            result = cursor.fetchall()
            cursor.close()
            close_connection(conn)
            return result if result else []

        except mysql.connector.Error as e:
            print(f"❌ Error searching suppliers: {e}")
            return []

    @staticmethod
    def get_by_name(nom):
        """
        Get supplier by name
        Returns: dict with supplier data or None
        """
        try:
            conn = get_connection('gestion_stock')
            cursor = conn.cursor(dictionary=True)

            sql = "SELECT * FROM fournisseurs WHERE nom = %s"
            cursor.execute(sql, (nom,))

            result = cursor.fetchone()
            cursor.close()
            close_connection(conn)
            return result

        except mysql.connector.Error as e:
            print(f"❌ Error getting supplier by name: {e}")
            return None
