"""
Input Validators - Field validation utilities for form inputs
Returns tuple: (is_valid, error_message or None)
"""
import re
from datetime import datetime
from repositories.suppliers_repo import SuppliersRepository
from repositories.categories_repo import CategoriesRepository
from repositories.products_repo import ProductsRepository


class InputValidators:
    """Handle all input validation logic"""

    @staticmethod
    def validate_not_empty(field_name, value):
        """
        Validate that a field is not empty
        Returns: (bool, error_message or None)
        """
        if not value or str(value).strip() == "":
            return False, f"{field_name} cannot be empty"
        return True, None

    @staticmethod
    def validate_positive_number(field_name, value):
        """
        Validate that a value is a positive number
        Returns: (bool, error_message or None)
        """
        try:
            num = float(value)
            if num <= 0:
                return False, f"{field_name} must be a positive number"
            return True, None
        except (ValueError, TypeError):
            return False, f"{field_name} must be a valid number"

    @staticmethod
    def validate_integer(field_name, value):
        """
        Validate that a value is a positive integer
        Returns: (bool, error_message or None)
        """
        try:
            num = int(value)
            if num < 0:
                return False, f"{field_name} must be a non-negative integer"
            return True, None
        except (ValueError, TypeError):
            return False, f"{field_name} must be a valid integer"

    @staticmethod
    def validate_email(email):
        """
        Validate email format
        Returns: (bool, error_message or None)
        """
        if not email or email.strip() == "":
            return True, None  # Email is optional

        # Basic email regex pattern
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return False, "Invalid email format"
        return True, None

    @staticmethod
    def validate_phone(phone):
        """
        Validate phone number format (basic - digits, spaces, dashes, +)
        Returns: (bool, error_message or None)
        """
        if not phone or phone.strip() == "":
            return True, None  # Phone is optional

        # Allow digits, spaces, dashes, plus sign
        pattern = r'^[\d\s\-\+]+$'
        if not re.match(pattern, phone):
            return False, "Invalid phone format (use digits, spaces, dashes, or +)"
        return True, None

    @staticmethod
    def validate_date_format(date_str):
        """
        Validate date format (YYYY-MM-DD)
        Returns: (bool, error_message or None)
        """
        if not date_str or date_str.strip() == "":
            return True, None  # Date is optional

        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True, None
        except ValueError:
            return False, "Invalid date format (use YYYY-MM-DD)"

    @staticmethod
    def validate_price(price):
        """
        Validate price (positive decimal number)
        Returns: (bool, error_message or None)
        """
        try:
            amount = float(price)
            if amount < 0:
                return False, "Price cannot be negative"
            if amount > 999999.99:
                return False, "Price is too large"
            return True, None
        except (ValueError, TypeError):
            return False, "Price must be a valid number"

    @staticmethod
    def validate_stock_quantity(quantity):
        """
        Validate stock quantity (non-negative integer)
        Returns: (bool, error_message or None)
        """
        try:
            qty = int(quantity)
            if qty < 0:
                return False, "Stock quantity cannot be negative"
            return True, None
        except (ValueError, TypeError):
            return False, "Stock quantity must be a valid integer"

    @staticmethod
    def validate_unique_supplier_name(name, exclude_id=None):
        """
        Validate that supplier name is unique
        Returns: (bool, error_message or None)
        """
        is_valid, error = InputValidators.validate_not_empty("Supplier name", name)
        if not is_valid:
            return is_valid, error

        existing = SuppliersRepository.get_by_name(name)
        if existing and (exclude_id is None or existing['id'] != exclude_id):
            return False, f"Supplier name '{name}' already exists"
        return True, None

    @staticmethod
    def validate_unique_category_name(name, exclude_id=None):
        """
        Validate that category name is unique
        Returns: (bool, error_message or None)
        """
        is_valid, error = InputValidators.validate_not_empty("Category name", name)
        if not is_valid:
            return is_valid, error

        existing = CategoriesRepository.read_all()
        for cat in existing:
            if cat['nom'] == name and (exclude_id is None or cat['id'] != exclude_id):
                return False, f"Category name '{name}' already exists"
        return True, None

    @staticmethod
    def validate_unique_product_name(name, exclude_id=None):
        """
        Validate that product name is unique
        Returns: (bool, error_message or None)
        """
        is_valid, error = InputValidators.validate_not_empty("Product name", name)
        if not is_valid:
            return is_valid, error

        existing = ProductsRepository.read_all()
        for product in existing:
            if product['nom'] == name and (exclude_id is None or product['id'] != exclude_id):
                return False, f"Product name '{name}' already exists"
        return True, None

    @staticmethod
    def validate_min_length(field_name, value, min_length):
        """
        Validate minimum string length
        Returns: (bool, error_message or None)
        """
        if len(str(value).strip()) < min_length:
            return False, f"{field_name} must be at least {min_length} characters"
        return True, None

    @staticmethod
    def validate_max_length(field_name, value, max_length):
        """
        Validate maximum string length
        Returns: (bool, error_message or None)
        """
        if len(str(value).strip()) > max_length:
            return False, f"{field_name} cannot exceed {max_length} characters"
        return True, None

    @staticmethod
    def validate_text_length(field_name, value, min_length=1, max_length=255):
        """
        Validate text length range
        Returns: (bool, error_message or None)
        """
        is_valid, error = InputValidators.validate_not_empty(field_name, value)
        if not is_valid:
            return is_valid, error

        length = len(str(value).strip())
        if length < min_length:
            return False, f"{field_name} must be at least {min_length} characters"
        if length > max_length:
            return False, f"{field_name} cannot exceed {max_length} characters"
        return True, None

    @staticmethod
    def validate_supplier_form(nom, contact, email, telephone, adresse, exclude_id=None):
        """
        Validate entire supplier form
        Returns: (bool, error_message or None)
        """
        # Validate name
        is_valid, error = InputValidators.validate_text_length("Supplier name", nom, min_length=2, max_length=100)
        if not is_valid:
            return is_valid, error

        is_valid, error = InputValidators.validate_unique_supplier_name(nom, exclude_id)
        if not is_valid:
            return is_valid, error

        # Validate contact
        is_valid, error = InputValidators.validate_text_length("Contact", contact, min_length=2, max_length=100)
        if not is_valid:
            return is_valid, error

        # Validate email
        is_valid, error = InputValidators.validate_email(email)
        if not is_valid:
            return is_valid, error

        # Validate phone
        is_valid, error = InputValidators.validate_phone(telephone)
        if not is_valid:
            return is_valid, error

        # Validate address
        is_valid, error = InputValidators.validate_text_length("Address", adresse, max_length=500)
        if not is_valid:
            return is_valid, error

        return True, None

    @staticmethod
    def validate_category_form(nom, description, exclude_id=None):
        """
        Validate entire category form
        Returns: (bool, error_message or None)
        """
        # Validate name
        is_valid, error = InputValidators.validate_text_length("Category name", nom, min_length=2, max_length=100)
        if not is_valid:
            return is_valid, error

        is_valid, error = InputValidators.validate_unique_category_name(nom, exclude_id)
        if not is_valid:
            return is_valid, error

        # Validate description
        is_valid, error = InputValidators.validate_text_length("Description", description, max_length=500)
        if not is_valid:
            return is_valid, error

        return True, None

    @staticmethod
    def validate_product_form(nom, categorie_id, fournisseur_id, quantite_stock, prix_unitaire, prix_achat,
                              exclude_id=None):
        """
        Validate entire product form
        Returns: (bool, error_message or None)
        """
        # Validate name
        is_valid, error = InputValidators.validate_text_length("Product name", nom, min_length=2, max_length=100)
        if not is_valid:
            return is_valid, error

        is_valid, error = InputValidators.validate_unique_product_name(nom, exclude_id)
        if not is_valid:
            return is_valid, error

        # Validate category selection
        is_valid, error = InputValidators.validate_positive_number("Category ID", categorie_id)
        if not is_valid:
            return is_valid, error

        # Validate supplier selection
        is_valid, error = InputValidators.validate_positive_number("Supplier ID", fournisseur_id)
        if not is_valid:
            return is_valid, error

        # Validate stock quantity
        is_valid, error = InputValidators.validate_stock_quantity(quantite_stock)
        if not is_valid:
            return is_valid, error

        # Validate unit price
        is_valid, error = InputValidators.validate_price(prix_unitaire)
        if not is_valid:
            return False, "Unit price: " + error

        # Validate purchase price
        is_valid, error = InputValidators.validate_price(prix_achat)
        if not is_valid:
            return False, "Purchase price: " + error

        return True, None

    @staticmethod
    def validate_order_form(produit_id, fournisseur_id, quantite, date_livraison, prix_total):
        """
        Validate entire order form
        Returns: (bool, error_message or None)
        """
        # Validate product selection
        is_valid, error = InputValidators.validate_positive_number("Product ID", produit_id)
        if not is_valid:
            return is_valid, error

        # Validate supplier selection
        is_valid, error = InputValidators.validate_positive_number("Supplier ID", fournisseur_id)
        if not is_valid:
            return is_valid, error

        # Validate quantity
        is_valid, error = InputValidators.validate_stock_quantity(quantite)
        if not is_valid:
            return False, "Quantity: " + error

        # Validate delivery date
        is_valid, error = InputValidators.validate_date_format(date_livraison)
        if not is_valid:
            return is_valid, error

        # Validate total price
        is_valid, error = InputValidators.validate_price(prix_total)
        if not is_valid:
            return False, "Total price: " + error

        return True, None
