"""
Categories Repository - CRUD operations for categories table
"""
import mysql.connector
from database.connection import get_connection, close_connection


class CategoriesRepository:
    """Handle all category-related database operations"""

    @staticmethod
    def create(nom, description):
        """
        Create a new category
        Returns: category_id if successful, None if failed
        """
        try:
            conn = get_connection('gestion_stock')
            cursor = conn.cursor()

            sql = "INSERT INTO categories (nom, description) VALUES (%s, %s)"
            cursor.execute(sql, (nom, description))

            category_id = cursor.lastrowid
            cursor.close()
            close_connection(conn)
            return category_id

        except mysql.connector.Error as e:
            print(f"❌ Error creating category: {e}")
            return None

    @staticmethod
    def read(category_id):
        """
        Get category by ID
        Returns: dict with category data or None
        """
        try:
            conn = get_connection('gestion_stock')
            cursor = conn.cursor(dictionary=True)

            sql = "SELECT * FROM categories WHERE id = %s"
            cursor.execute(sql, (category_id,))

            result = cursor.fetchone()
            cursor.close()
            close_connection(conn)
            return result

        except mysql.connector.Error as e:
            print(f"❌ Error reading category: {e}")
            return None

    @staticmethod
    def read_all():
        """
        Get all categories
        Returns: list of dicts
        """
        try:
            conn = get_connection('gestion_stock')
            cursor = conn.cursor(dictionary=True)

            sql = "SELECT * FROM categories ORDER BY id"
            cursor.execute(sql)

            result = cursor.fetchall()
            cursor.close()
            close_connection(conn)
            return result if result else []

        except mysql.connector.Error as e:
            print(f"❌ Error reading categories: {e}")
            return []

    @staticmethod
    def update(category_id, nom, description):
        """
        Update category information
        Returns: True if successful, False otherwise
        """
        try:
            conn = get_connection('gestion_stock')
            cursor = conn.cursor()

            sql = "UPDATE categories SET nom = %s, description = %s WHERE id = %s"
            cursor.execute(sql, (nom, description, category_id))

            cursor.close()
            close_connection(conn)
            return cursor.rowcount > 0

        except mysql.connector.Error as e:
            print(f"❌ Error updating category: {e}")
            return False

    @staticmethod
    def delete(category_id):
        """
        Delete category by ID
        CASCADE will delete all products with this category
        Returns: True if successful, False otherwise
        """
        try:
            conn = get_connection('gestion_stock')
            cursor = conn.cursor()

            sql = "DELETE FROM categories WHERE id = %s"
            cursor.execute(sql, (category_id,))

            cursor.close()
            close_connection(conn)
            return cursor.rowcount > 0

        except mysql.connector.Error as e:
            print(f"❌ Error deleting category: {e}")
            return False

    @staticmethod
    def search(search_term):
        """
        Search categories by name or description
        Returns: list of dicts matching the search term
        """
        try:
            conn = get_connection('gestion_stock')
            cursor = conn.cursor(dictionary=True)

            search_param = f"%{search_term}%"
            sql = "SELECT * FROM categories WHERE nom LIKE %s OR description LIKE %s ORDER BY id"
            cursor.execute(sql, (search_param, search_param))

            result = cursor.fetchall()
            cursor.close()
            close_connection(conn)
            return result if result else []

        except mysql.connector.Error as e:
            print(f"❌ Error searching categories: {e}")
            return []
