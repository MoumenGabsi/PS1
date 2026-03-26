"""
Suppliers Tab - CRUD interface for suppliers (CustomTkinter version)
"""
import customtkinter as ctk
from tkinter import messagebox
from repositories.suppliers_repo import SuppliersRepository
from validators.input_validators import InputValidators
from gui.dialogs import AddUpdateDialog, DeleteConfirmDialog, ErrorDialog, SuccessDialog


class SuppliersTab(ctk.CTkFrame):
    """Tab for managing suppliers"""
    
    def __init__(self, parent):
        super().__init__(parent, fg_color="#0f0f0f")
        self.pack(fill="both", expand=True)
        self.repo = SuppliersRepository()
        self.validator = InputValidators()
        self.selected_row = None
        self.table_rows = []
        
        self._create_widgets()
        self._load_data()
    
    def _create_widgets(self):
        """Create tab widgets"""
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Search frame
        search_frame = ctk.CTkFrame(self, fg_color="#1a1a1a", corner_radius=8)
        search_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        search_frame.grid_columnconfigure(1, weight=1)
        
        search_label = ctk.CTkLabel(
            search_frame, text="🔍 Search:", font=("Arial", 12, "bold"), text_color="#3a7ebf"
        )
        search_label.grid(row=0, column=0, padx=12, pady=12)
        
        self.search_entry = ctk.CTkEntry(
            search_frame, 
            placeholder_text="Search suppliers...",
            width=300,
            fg_color="#2a2a2a",
            border_color="#3a7ebf",
            text_color="#ffffff"
        )
        self.search_entry.grid(row=0, column=1, padx=8, pady=12, sticky="w")
        self.search_entry.bind('<KeyRelease>', lambda e: self._on_search_change())
        
        clear_btn = ctk.CTkButton(
            search_frame,
            text="Clear",
            command=self._clear_search,
            fg_color="#3a7ebf",
            hover_color="#2a5a9f",
            width=80,
            height=36
        )
        clear_btn.grid(row=0, column=2, padx=8, pady=12)
        
        # Data frame
        data_frame = ctk.CTkFrame(self, fg_color="#1a1a1a", corner_radius=8)
        data_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        data_frame.grid_rowconfigure(0, weight=0)
        data_frame.grid_rowconfigure(1, weight=1)
        data_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        data_title = ctk.CTkLabel(
            data_frame,
            text="📋 Suppliers List",
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
        
        # Store for table rows
        self.table_rows = []
        
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
    
    def _load_data(self):
        """Load suppliers from database"""
        # Clear table
        for row in self.table_rows:
            row.destroy()
        self.table_rows.clear()
        
        # Create header row
        header_row = ctk.CTkFrame(self.table_frame, fg_color="#1a1a1a", height=40)
        header_row.pack(fill="x", padx=0, pady=0)
        header_row.pack_propagate(False)
        
        headers = ['ID', 'Name', 'Contact', 'Email', 'Phone', 'Address']
        widths = [30, 120, 100, 150, 100, 200]
        
        for i, (header, width) in enumerate(zip(headers, widths)):
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
        suppliers = self.repo.read_all()
        for supplier in suppliers:
            self._add_table_row(
                supplier['id'],
                supplier['nom'],
                supplier['contact'],
                supplier['email'] or '',
                supplier['telephone'] or '',
                supplier['adresse'] or ''
            )
    
    def _add_table_row(self, supplier_id, name, contact, email, phone, address):
        """Add a row to the suppliers table"""
        row_frame = ctk.CTkFrame(self.table_frame, fg_color="#2a2a2a", corner_radius=4, height=40)
        row_frame.pack(fill="x", padx=0, pady=2)
        row_frame.pack_propagate(False)
        
        # Store supplier ID for operations
        row_frame.supplier_id = supplier_id
        
        values = [str(supplier_id), name, contact, email, phone, address]
        widths = [30, 120, 100, 150, 100, 200]
        
        for i, (value, width) in enumerate(zip(values, widths)):
            col = ctk.CTkFrame(row_frame, width=width, fg_color="#2a2a2a")
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
        # Deselect all
        for row in self.table_rows[1:]:  # Skip header
            row.configure(fg_color="#2a2a2a")
        # Select current
        row_frame.configure(fg_color="#3a7ebf")
        self.selected_row = row_frame
    
    def _on_search_change(self):
        """Filter table based on search term"""
        search_term = self.search_entry.get().strip()
        
        # Clear table
        for row in self.table_rows:
            row.destroy()
        self.table_rows.clear()
        
        # Create header row
        header_row = ctk.CTkFrame(self.table_frame, fg_color="#1a1a1a", height=40)
        header_row.pack(fill="x", padx=0, pady=0)
        header_row.pack_propagate(False)
        
        headers = ['ID', 'Name', 'Contact', 'Email', 'Phone', 'Address']
        widths = [30, 120, 100, 150, 100, 200]
        
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
        
        if not search_term:
            self._load_data()
            return
        
        # Search
        results = self.repo.search(search_term)
        for supplier in results:
            self._add_table_row(
                supplier['id'],
                supplier['nom'],
                supplier['contact'],
                supplier['email'] or '',
                supplier['telephone'] or '',
                supplier['adresse'] or ''
            )
    
    def _clear_search(self):
        """Clear search field"""
        self.search_entry.delete(0, "end")
        self._load_data()
    
    def _on_add(self):
        """Add new supplier"""
        fields = [
            ("Name", "text", True),
            ("Contact", "text", True),
            ("Email", "email", False),
            ("Phone", "text", False),
            ("Address", "text", False)
        ]
        
        dialog = AddUpdateDialog(self, "Add Supplier", fields)
        result = dialog.get_result()
        
        if result:
            is_valid, error = self.validator.validate_supplier_form(
                result['Name'],
                result['Contact'],
                result['Email'],
                result['Phone'],
                result['Address']
            )
            
            if not is_valid:
                ErrorDialog.show(self, "Validation Error", error)
                return
            
            supplier_id = self.repo.create(
                result['Name'],
                result['Contact'],
                result['Email'],
                result['Phone'],
                result['Address']
            )
            
            if supplier_id:
                SuccessDialog.show(self, "Success", "Supplier added successfully")
                self._load_data()
            else:
                ErrorDialog.show(self, "Error", "Failed to add supplier")
    
    def _on_edit(self):
        """Edit selected supplier"""
        if not hasattr(self, 'selected_row') or self.selected_row is None:
            messagebox.showwarning("Warning", "Please select a supplier to edit")
            return
        
        supplier_id = self.selected_row.supplier_id
        
        supplier = self.repo.read(supplier_id)
        if not supplier:
            ErrorDialog.show(self, "Error", "Supplier not found")
            return
        
        fields = [
            ("Name", "text", True),
            ("Contact", "text", True),
            ("Email", "email", False),
            ("Phone", "text", False),
            ("Address", "text", False)
        ]
        
        initial = {
            "Name": supplier['nom'],
            "Contact": supplier['contact'],
            "Email": supplier['email'] or '',
            "Phone": supplier['telephone'] or '',
            "Address": supplier['adresse'] or ''
        }
        
        dialog = AddUpdateDialog(self, "Edit Supplier", fields, initial)
        result = dialog.get_result()
        
        if result:
            is_valid, error = self.validator.validate_supplier_form(
                result['Name'],
                result['Contact'],
                result['Email'],
                result['Phone'],
                result['Address'],
                exclude_id=supplier_id
            )
            
            if not is_valid:
                ErrorDialog.show(self, "Validation Error", error)
                return
            
            success = self.repo.update(
                supplier_id,
                result['Name'],
                result['Contact'],
                result['Email'],
                result['Phone'],
                result['Address']
            )
            
            if success:
                SuccessDialog.show(self, "Success", "Supplier updated successfully")
                self._load_data()
            else:
                ErrorDialog.show(self, "Error", "Failed to update supplier")
    
    def _on_delete(self):
        """Delete selected supplier"""
        if not hasattr(self, 'selected_row') or self.selected_row is None:
            messagebox.showwarning("Warning", "Please select a supplier to delete")
            return
        
        supplier_id = self.selected_row.supplier_id
        
        # Get supplier name from table (search for it in the row)
        supplier = self.repo.read(supplier_id)
        if not supplier:
            ErrorDialog.show(self, "Error", "Supplier not found")
            return
        
        supplier_name = supplier['nom']
        
        if DeleteConfirmDialog.show(self, "Delete Supplier", f"Supplier: {supplier_name}"):
            success = self.repo.delete(supplier_id)
            
            if success:
                SuccessDialog.show(self, "Success", "Supplier deleted successfully")
                self._load_data()
            else:
                ErrorDialog.show(self, "Error", "Failed to delete supplier")
