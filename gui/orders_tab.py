"""
Orders Tab - CRUD interface for orders (CustomTkinter version)
"""
import customtkinter as ctk
from tkinter import messagebox
from repositories.orders_repo import OrdersRepository
from repositories.products_repo import ProductsRepository
from repositories.suppliers_repo import SuppliersRepository
from validators.input_validators import InputValidators
from gui.dialogs import AddUpdateDialog, DeleteConfirmDialog, ErrorDialog, SuccessDialog


class OrdersTab(ctk.CTkFrame):
    """Tab for managing orders"""
    
    def __init__(self, parent):
        super().__init__(parent, fg_color="#0f0f0f")
        self.pack(fill="both", expand=True)
        self.orders_repo = OrdersRepository()
        self.products_repo = ProductsRepository()
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
            placeholder_text="Search orders...",
            width=200,
            fg_color="#2a2a2a",
            border_color="#3a7ebf",
            text_color="#ffffff"
        )
        self.search_entry.grid(row=0, column=1, padx=8, pady=12)
        self.search_entry.bind('<KeyRelease>', lambda e: self._on_search_change())
        
        filter_label = ctk.CTkLabel(
            search_frame, text="📊 Status:", font=("Arial", 12, "bold"), text_color="#3a7ebf"
        )
        filter_label.grid(row=0, column=2, padx=12, pady=12)
        
        self.status_filter = ctk.CTkComboBox(
            search_frame,
            state="readonly",
            width=120,
            values=['--All--', 'En attente', 'Livrée', 'Annulée'],
            fg_color="#2a2a2a",
            border_color="#3a7ebf",
            text_color="#ffffff",
            command=self._apply_filters
        )
        self.status_filter.grid(row=0, column=3, padx=8, pady=12, sticky="w")
        self.status_filter.set('--All--')
        
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
            text="📝 Orders List",
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
    
    def _format_date(self, date_obj):
        """Format date to readable string"""
        if date_obj is None:
            return ''
        return str(date_obj)[:10]
    
    def _load_data(self):
        """Load orders from database"""
        # Clear table
        for row in self.table_rows:
            row.destroy()
        self.table_rows.clear()
        
        # Create header row
        header_row = ctk.CTkFrame(self.table_frame, fg_color="#1a1a1a", height=40)
        header_row.pack(fill="x", padx=0, pady=0)
        header_row.pack_propagate(False)
        
        headers = ['ID', 'Product', 'Supplier', 'Qty', 'Order Date', 'Delivery Date', 'Total Price', 'Status']
        widths = [30, 100, 100, 50, 100, 100, 80, 80]
        
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
        
        # Load data
        orders = self.orders_repo.read_all()
        for order in orders:
            self._add_table_row(
                order['id'],
                order['produit_nom'],
                order['fournisseur_nom'],
                order['quantite'],
                self._format_date(order['date_commande']),
                self._format_date(order['date_livraison']),
                f"{order['prix_total']:.2f}",
                order['statut']
            )
    
    def _add_table_row(self, order_id, product, supplier, quantity, order_date, delivery_date, total_price, status):
        """Add a row to the orders table"""
        # Color code by status
        status_colors = {
            'En attente': '#f39c12',
            'Livrée': '#27ae60',
            'Annulée': '#e74c3c'
        }
        bg_color = status_colors.get(status, '#2a2a2a')
        
        row_frame = ctk.CTkFrame(self.table_frame, fg_color=bg_color, corner_radius=4, height=40)
        row_frame.pack(fill="x", padx=0, pady=2)
        row_frame.pack_propagate(False)
        
        # Store order ID for operations
        row_frame.order_id = order_id
        row_frame.status = status
        
        values = [str(order_id), product, supplier, str(quantity), order_date, delivery_date, total_price, status]
        widths = [30, 100, 100, 50, 100, 100, 80, 80]
        
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
            status_colors = {
                'En attente': '#f39c12',
                'Livrée': '#27ae60',
                'Annulée': '#e74c3c'
            }
            default_color = status_colors.get(row.status, '#2a2a2a')
            row.configure(fg_color=default_color)
        row_frame.configure(fg_color="#3a7ebf")
        self.selected_row = row_frame
    
    def _on_search_change(self):
        """Filter table based on search term"""
        self._apply_filters()
    
    def _apply_filters(self, value=None):
        """Apply search and status filters"""
        search_term = self.search_entry.get().strip()
        status_filter = self.status_filter.get()
        
        # Clear table
        for row in self.table_rows[1:]:
            row.destroy()
        self.table_rows = [self.table_rows[0]]
        
        # Load all orders
        orders = self.orders_repo.read_all()
        
        # Apply filters
        for order in orders:
            # Search filter
            if search_term:
                search_lower = search_term.lower()
                if (search_lower not in order['produit_nom'].lower() and
                    search_lower not in order['fournisseur_nom'].lower()):
                    continue
            
            # Status filter
            if status_filter != '--All--' and order['statut'] != status_filter:
                continue
            
            self._add_table_row(
                order['id'],
                order['produit_nom'],
                order['fournisseur_nom'],
                order['quantite'],
                self._format_date(order['date_commande']),
                self._format_date(order['date_livraison']),
                f"{order['prix_total']:.2f}",
                order['statut']
            )
    
    def _clear_filters(self):
        """Clear all filters"""
        self.search_entry.delete(0, "end")
        self.status_filter.set('--All--')
        self._load_data()
    
    def _on_add(self):
        """Add new order"""
        products = self.products_repo.read_all()
        suppliers = self.suppliers_repo.read_all()
        
        if not products:
            ErrorDialog.show(self, "Error", "Please add at least one product first")
            return
        
        if not suppliers:
            ErrorDialog.show(self, "Error", "Please add at least one supplier first")
            return
        
        fields = [
            ("Product", "dropdown", True),
            ("Supplier", "dropdown", True),
            ("Quantity", "number", True),
            ("Delivery Date", "date", False),
            ("Total Price", "number", True)
        ]
        
        dialog = AddUpdateDialog(self, "Add Order", fields)
        
        # Populate dropdowns
        product_names = [p['nom'] for p in products]
        supplier_names = [s['nom'] for s in suppliers]
        
        dialog.dropdowns['Product']['values'] = product_names
        dialog.dropdowns['Supplier']['values'] = supplier_names
        
        result = dialog.get_result()
        
        if result:
            # Find product and supplier IDs
            product = next((p for p in products if p['nom'] == result['Product']), None)
            supplier = next((s for s in suppliers if s['nom'] == result['Supplier']), None)
            
            if not product or not supplier:
                ErrorDialog.show(self, "Error", "Invalid product or supplier")
                return
            
            is_valid, error = self.validator.validate_order_form(
                product['id'],
                supplier['id'],
                result['Quantity'],
                result['Delivery Date'],
                result['Total Price']
            )
            
            if not is_valid:
                ErrorDialog.show(self, "Validation Error", error)
                return
            
            order_id = self.orders_repo.create(
                product['id'],
                supplier['id'],
                int(result['Quantity']),
                result['Delivery Date'] if result['Delivery Date'] else None,
                float(result['Total Price'])
            )
            
            if order_id:
                SuccessDialog.show(self, "Success", "Order added successfully")
                self._load_data()
            else:
                ErrorDialog.show(self, "Error", "Failed to add order")
    
    def _on_edit(self):
        """Edit selected order"""
        if not hasattr(self, 'selected_row') or self.selected_row is None:
            messagebox.showwarning("Warning", "Please select an order to edit")
            return
        
        order_id = self.selected_row.order_id
        
        order = self.orders_repo.read(order_id)
        if not order:
            ErrorDialog.show(self, "Error", "Order not found")
            return
        
        products = self.products_repo.read_all()
        suppliers = self.suppliers_repo.read_all()
        
        fields = [
            ("Product", "dropdown", True),
            ("Supplier", "dropdown", True),
            ("Quantity", "number", True),
            ("Delivery Date", "date", False),
            ("Total Price", "number", True),
            ("Status", "dropdown", True)
        ]
        
        initial = {
            "Product": order['produit_nom'],
            "Supplier": order['fournisseur_nom'],
            "Quantity": str(order['quantite']),
            "Delivery Date": self._format_date(order['date_livraison']),
            "Total Price": str(order['prix_total']),
            "Status": order['statut']
        }
        
        dialog = AddUpdateDialog(self, "Edit Order", fields, initial)
        
        # Populate dropdowns
        product_names = [p['nom'] for p in products]
        supplier_names = [s['nom'] for s in suppliers]
        
        dialog.dropdowns['Product']['values'] = product_names
        dialog.dropdowns['Supplier']['values'] = supplier_names
        dialog.dropdowns['Status']['values'] = ['En attente', 'Livrée', 'Annulée']
        
        result = dialog.get_result()
        
        if result:
            # Find product and supplier IDs
            product = next((p for p in products if p['nom'] == result['Product']), None)
            supplier = next((s for s in suppliers if s['nom'] == result['Supplier']), None)
            
            if not product or not supplier:
                ErrorDialog.show(self, "Error", "Invalid product or supplier")
                return
            
            is_valid, error = self.validator.validate_order_form(
                product['id'],
                supplier['id'],
                result['Quantity'],
                result['Delivery Date'],
                result['Total Price']
            )
            
            if not is_valid:
                ErrorDialog.show(self, "Validation Error", error)
                return
            
            success = self.orders_repo.update(
                order_id,
                product['id'],
                supplier['id'],
                int(result['Quantity']),
                result['Delivery Date'] if result['Delivery Date'] else None,
                float(result['Total Price']),
                result['Status']
            )
            
            if success:
                SuccessDialog.show(self, "Success", "Order updated successfully")
                self._load_data()
            else:
                ErrorDialog.show(self, "Error", "Failed to update order")
    
    def _on_delete(self):
        """Delete selected order"""
        if not hasattr(self, 'selected_row') or self.selected_row is None:
            messagebox.showwarning("Warning", "Please select an order to delete")
            return
        
        order_id = self.selected_row.order_id
        
        # Get order details from database
        order = self.orders_repo.read(order_id)
        if not order:
            ErrorDialog.show(self, "Error", "Order not found")
            return
        
        order_product = order['produit_nom']
        
        if DeleteConfirmDialog.show(self, "Delete Order", f"Order for: {order_product}"):
            success = self.orders_repo.delete(order_id)
            
            if success:
                SuccessDialog.show(self, "Success", "Order deleted successfully")
                self._load_data()
            else:
                ErrorDialog.show(self, "Error", "Failed to delete order")
