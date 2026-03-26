"""
Products Tab - CRUD interface for products (CustomTkinter version)
"""
import customtkinter as ctk
from tkinter import messagebox
from repositories.products_repo import ProductsRepository
from repositories.categories_repo import CategoriesRepository
from repositories.suppliers_repo import SuppliersRepository
from validators.input_validators import InputValidators
from gui.dialogs import AddUpdateDialog, DeleteConfirmDialog, ErrorDialog, SuccessDialog


class ProductsTab(ctk.CTkFrame):
    """Tab for managing products"""
    
    def __init__(self, parent):
        super().__init__(parent, fg_color="#0f0f0f")
        self.pack(fill="both", expand=True)
        self.products_repo = ProductsRepository()
        self.categories_repo = CategoriesRepository()
        self.suppliers_repo = SuppliersRepository()
        self.validator = InputValidators()
        self.selected_row = None
        self.table_rows = []
        
        self._create_widgets()
        self._load_data()
    
    def _create_widgets(self):
        """Create tab widgets"""
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Search and filter frame
        search_frame = ctk.CTkFrame(self, fg_color="#1a1a1a", corner_radius=8)
        search_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        search_frame.grid_columnconfigure(3, weight=1)
        
        search_label = ctk.CTkLabel(
            search_frame, text="🔍 Search:", font=("Arial", 12, "bold"), text_color="#3a7ebf"
        )
        search_label.grid(row=0, column=0, padx=12, pady=12)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search products...",
            width=200,
            fg_color="#2a2a2a",
            border_color="#3a7ebf",
            text_color="#ffffff"
        )
        self.search_entry.grid(row=0, column=1, padx=8, pady=12)
        self.search_entry.bind('<KeyRelease>', lambda e: self._on_search_change())
        
        filter_label = ctk.CTkLabel(
            search_frame, text="📂 Category:", font=("Arial", 12, "bold"), text_color="#3a7ebf"
        )
        filter_label.grid(row=0, column=2, padx=12, pady=12)
        
        self.category_filter = ctk.CTkComboBox(
            search_frame,
            state="readonly",
            width=150,
            fg_color="#2a2a2a",
            border_color="#3a7ebf",
            text_color="#ffffff",
            command=self._apply_filters
        )
        self.category_filter.grid(row=0, column=3, padx=8, pady=12, sticky="w")
        
        clear_btn = ctk.CTkButton(
            search_frame,
            text="Clear",
            command=self._clear_filters,
            fg_color="#3a7ebf",
            hover_color="#2a5a9f",
            width=80,
            height=36
        )
        clear_btn.grid(row=0, column=4, padx=8, pady=12)
        
        # Data frame
        data_frame = ctk.CTkFrame(self, fg_color="#1a1a1a", corner_radius=8)
        data_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        data_frame.grid_rowconfigure(0, weight=0)
        data_frame.grid_rowconfigure(1, weight=1)
        data_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        data_title = ctk.CTkLabel(
            data_frame,
            text="📦 Products List",
            font=("Arial", 14, "bold"),
            text_color="#3a7ebf"
        )
        data_title.grid(row=0, column=0, sticky="w", padx=12, pady=8)
        
        # Table frame with scrollbar
        table_container = ctk.CTkFrame(data_frame, fg_color="#2a2a2a", corner_radius=6)
        table_container.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)
        
        # Create scrollable frame for table
        self.table_frame = ctk.CTkScrollableFrame(
            table_container,
            fg_color="#2a2a2a",
            label_text="",
            label_fg_color="#1a1a1a"
        )
        self.table_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.table_frame.grid_columnconfigure(0, weight=1)
        
        # Buttons frame
        button_frame = ctk.CTkFrame(self, fg_color="#1a1a1a", corner_radius=8)
        button_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        
        add_btn = ctk.CTkButton(
            button_frame,
            text="➕ Add",
            command=self._on_add,
            fg_color="#3a7ebf",
            hover_color="#2a5a9f",
            width=90,
            height=36,
            font=("Arial", 11, "bold")
        )
        add_btn.pack(side="left", padx=8, pady=8)
        
        edit_btn = ctk.CTkButton(
            button_frame,
            text="✏️ Edit",
            command=self._on_edit,
            fg_color="#3a7ebf",
            hover_color="#2a5a9f",
            width=90,
            height=36,
            font=("Arial", 11, "bold")
        )
        edit_btn.pack(side="left", padx=8, pady=8)
        
        delete_btn = ctk.CTkButton(
            button_frame,
            text="🗑️ Delete",
            command=self._on_delete,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            width=90,
            height=36,
            font=("Arial", 11, "bold")
        )
        delete_btn.pack(side="left", padx=8, pady=8)
        
        refresh_btn = ctk.CTkButton(
            button_frame,
            text="🔄 Refresh",
            command=self._load_data,
            fg_color="#27ae60",
            hover_color="#229954",
            width=90,
            height=36,
            font=("Arial", 11, "bold")
        )
        refresh_btn.pack(side="left", padx=8, pady=8)
    
    def _load_category_filter(self):
        """Load categories into filter dropdown"""
        categories = self.categories_repo.read_all()
        category_names = ['--All--'] + [cat['nom'] for cat in categories]
        self.category_filter.configure(values=category_names)
        self.category_filter.set('--All--')
    
    def _load_data(self):
        """Load products from database"""
        # Clear table
        for row in self.table_rows:
            row.destroy()
        self.table_rows.clear()
        
        # Create header row
        header_row = ctk.CTkFrame(self.table_frame, fg_color="#1a1a1a", height=40)
        header_row.pack(fill="x", padx=0, pady=0)
        header_row.pack_propagate(False)
        
        headers = ['ID', 'Name', 'Category', 'Supplier', 'Stock', 'Unit Price', 'Purchase Price']
        widths = [30, 120, 100, 100, 60, 80, 80]
        
        for header, width in zip(headers, widths):
            col = ctk.CTkFrame(header_row, width=width, fg_color="#1a1a1a")
            col.pack(side="left", fill="y", padx=4, pady=8)
            lbl = ctk.CTkLabel(
                col,
                text=header,
                font=("Arial", 11, "bold"),
                text_color="#3a7ebf",
                width=width
            )
            lbl.pack(fill="both", expand=True)
        
        self.table_rows.append(header_row)
        
        # Load category filter
        self._load_category_filter()
        
        # Load data
        products = self.products_repo.read_all()
        for product in products:
            self._add_table_row(
                product['id'],
                product['nom'],
                product['categorie_nom'],
                product['fournisseur_nom'],
                product['quantite_stock'],
                f"{product['prix_unitaire']:.2f}",
                f"{product['prix_achat']:.2f}"
            )
    
    def _add_table_row(self, product_id, name, category, supplier, stock, unit_price, purchase_price):
        """Add a row to the products table"""
        # Highlight low stock
        stock_int = int(stock)
        bg_color = "#c0392b" if stock_int < 10 else "#2a2a2a"
        row_frame = ctk.CTkFrame(self.table_frame, fg_color=bg_color, corner_radius=4, height=40)
        row_frame.pack(fill="x", padx=0, pady=2)
        row_frame.pack_propagate(False)
        
        # Store product ID for operations
        row_frame.product_id = product_id
        row_frame.stock_value = stock_int
        
        values = [str(product_id), name, category, supplier, str(stock), unit_price, purchase_price]
        widths = [30, 120, 100, 100, 60, 80, 80]
        
        for value, width in zip(values, widths):
            col = ctk.CTkFrame(row_frame, width=width, fg_color=bg_color)
            col.pack(side="left", fill="y", padx=4, pady=8)
            lbl = ctk.CTkLabel(
                col,
                text=value,
                font=("Arial", 10),
                text_color="#ffffff",
                width=width,
                wraplength=width - 8
            )
            lbl.pack(fill="both", expand=True)
        
        # Bind click to select row
        row_frame.bind("<Button-1>", lambda e: self._select_row(row_frame))
        for child in row_frame.winfo_children():
            child.bind("<Button-1>", lambda e: self._select_row(row_frame))
            for subchild in child.winfo_children():
                subchild.bind("<Button-1>", lambda e: self._select_row(row_frame))
        
        self.table_rows.append(row_frame)
    
    def _select_row(self, row_frame):
        """Select a table row"""
        for row in self.table_rows[1:]:
            if row == row_frame:
                continue
            default_color = "#c0392b" if row.stock_value < 10 else "#2a2a2a"
            row.configure(fg_color=default_color)
        row_frame.configure(fg_color="#3a7ebf")
        self.selected_row = row_frame
    
    def _on_search_change(self):
        """Filter table based on search term"""
        self._apply_filters()
    
    def _apply_filters(self, value=None):
        """Apply search and category filters"""
        search_term = self.search_entry.get().strip()
        category_filter = self.category_filter.get()
        
        # Clear table
        for row in self.table_rows[1:]:
            row.destroy()
        self.table_rows = [self.table_rows[0]]
        
        # Load all products
        products = self.products_repo.read_all()
        
        # Apply filters
        for product in products:
            # Search filter
            if search_term and search_term.lower() not in product['nom'].lower():
                continue
            
            # Category filter
            if category_filter != '--All--' and product['categorie_nom'] != category_filter:
                continue
            
            self._add_table_row(
                product['id'],
                product['nom'],
                product['categorie_nom'],
                product['fournisseur_nom'],
                product['quantite_stock'],
                f"{product['prix_unitaire']:.2f}",
                f"{product['prix_achat']:.2f}"
            )
    
    def _clear_filters(self):
        """Clear all filters"""
        self.search_entry.delete(0, "end")
        self.category_filter.set('--All--')
        self._load_data()
    
    def _on_add(self):
        """Add new product"""
        categories = self.categories_repo.read_all()
        suppliers = self.suppliers_repo.read_all()
        
        if not categories:
            ErrorDialog.show(self, "Error", "Please add at least one category first")
            return
        
        if not suppliers:
            ErrorDialog.show(self, "Error", "Please add at least one supplier first")
            return
        
        fields = [
            ("Name", "text", True),
            ("Category", "dropdown", True),
            ("Supplier", "dropdown", True),
            ("Stock Quantity", "number", True),
            ("Unit Price", "number", True),
            ("Purchase Price", "number", True)
        ]
        
        dialog = AddUpdateDialog(self, "Add Product", fields)
        
        # Populate dropdowns
        category_names = [cat['nom'] for cat in categories]
        supplier_names = [sup['nom'] for sup in suppliers]
        
        dialog.dropdowns['Category'].configure(values=category_names)
        dialog.dropdowns['Supplier'].configure(values=supplier_names)
        
        result = dialog.get_result()
        
        if result:
            # Find category and supplier IDs
            category = next((c for c in categories if c['nom'] == result['Category']), None)
            supplier = next((s for s in suppliers if s['nom'] == result['Supplier']), None)
            
            if not category or not supplier:
                ErrorDialog.show(self, "Error", "Invalid category or supplier")
                return
            
            is_valid, error = self.validator.validate_product_form(
                result['Name'],
                category['id'],
                supplier['id'],
                result['Stock Quantity'],
                result['Unit Price'],
                result['Purchase Price']
            )
            
            if not is_valid:
                ErrorDialog.show(self, "Validation Error", error)
                return
            
            product_id = self.products_repo.create(
                result['Name'],
                category['id'],
                supplier['id'],
                int(result['Stock Quantity']),
                float(result['Unit Price']),
                float(result['Purchase Price'])
            )
            
            if product_id:
                SuccessDialog.show(self, "Success", "Product added successfully")
                self._load_data()
            else:
                ErrorDialog.show(self, "Error", "Failed to add product")
    
    def _on_edit(self):
        """Edit selected product"""
        if not hasattr(self, 'selected_row') or self.selected_row is None:
            messagebox.showwarning("Warning", "Please select a product to edit")
            return
        
        product_id = self.selected_row.product_id
        
        product = self.products_repo.read(product_id)
        if not product:
            ErrorDialog.show(self, "Error", "Product not found")
            return
        
        categories = self.categories_repo.read_all()
        suppliers = self.suppliers_repo.read_all()
        
        fields = [
            ("Name", "text", True),
            ("Category", "dropdown", True),
            ("Supplier", "dropdown", True),
            ("Stock Quantity", "number", True),
            ("Unit Price", "number", True),
            ("Purchase Price", "number", True)
        ]
        
        initial = {
            "Name": product['nom'],
            "Category": product['categorie_nom'],
            "Supplier": product['fournisseur_nom'],
            "Stock Quantity": str(product['quantite_stock']),
            "Unit Price": str(product['prix_unitaire']),
            "Purchase Price": str(product['prix_achat'])
        }
        
        dialog = AddUpdateDialog(self, "Edit Product", fields, initial)
        
        # Populate dropdowns
        category_names = [cat['nom'] for cat in categories]
        supplier_names = [sup['nom'] for sup in suppliers]
        
        dialog.dropdowns['Category'].configure(values=category_names)
        dialog.dropdowns['Supplier'].configure(values=supplier_names)
        
        result = dialog.get_result()
        
        if result:
            # Find category and supplier IDs
            category = next((c for c in categories if c['nom'] == result['Category']), None)
            supplier = next((s for s in suppliers if s['nom'] == result['Supplier']), None)
            
            if not category or not supplier:
                ErrorDialog.show(self, "Error", "Invalid category or supplier")
                return
            
            is_valid, error = self.validator.validate_product_form(
                result['Name'],
                category['id'],
                supplier['id'],
                result['Stock Quantity'],
                result['Unit Price'],
                result['Purchase Price'],
                exclude_id=product_id
            )
            
            if not is_valid:
                ErrorDialog.show(self, "Validation Error", error)
                return
            
            success = self.products_repo.update(
                product_id,
                result['Name'],
                category['id'],
                supplier['id'],
                int(result['Stock Quantity']),
                float(result['Unit Price']),
                float(result['Purchase Price'])
            )
            
            if success:
                SuccessDialog.show(self, "Success", "Product updated successfully")
                self._load_data()
            else:
                ErrorDialog.show(self, "Error", "Failed to update product")
    
    def _on_delete(self):
        """Delete selected product"""
        if not hasattr(self, 'selected_row') or self.selected_row is None:
            messagebox.showwarning("Warning", "Please select a product to delete")
            return
        
        product_id = self.selected_row.product_id
        
        # Get product name from database
        product = self.products_repo.read(product_id)
        if not product:
            ErrorDialog.show(self, "Error", "Product not found")
            return
        
        product_name = product['nom']
        
        if DeleteConfirmDialog.show(self, "Delete Product", f"Product: {product_name}"):
            success = self.products_repo.delete(product_id)
            
            if success:
                SuccessDialog.show(self, "Success", "Product deleted successfully")
                self._load_data()
            else:
                ErrorDialog.show(self, "Error", "Failed to delete product")
