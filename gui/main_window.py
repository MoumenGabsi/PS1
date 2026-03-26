"""
Main Application Window - CustomTkinter Version
"""
import customtkinter as ctk
from gui.suppliers_tab import SuppliersTab
from gui.categories_tab import CategoriesTab
from gui.products_tab import ProductsTab
from gui.orders_tab import OrdersTab


# Set appearance mode and theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MainWindow(ctk.CTk):
    """Main application window with tabbed interface"""
    
    def __init__(self):
        super().__init__()
        self.title("Gestion de Stock - Store & Inventory Management System")
        self.geometry("1200x800")
        self.minsize(1000, 600)
        
        # Configure grid
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Create header
        self._create_header()
        
        # Create main content area
        self._create_tabs()
        
        # Center window on screen
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def _create_header(self):
        """Create header with title"""
        header = ctk.CTkFrame(self, fg_color="#1a1a1a", height=80)
        header.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header.grid_propagate(False)
        
        title_label = ctk.CTkLabel(
            header,
            text="Gestion de Stock",
            font=("Arial", 28, "bold"),
            text_color="#3a7ebf"
        )
        title_label.pack(side="left", padx=20, pady=15)
        
        subtitle_label = ctk.CTkLabel(
            header,
            text="Store & Inventory Management System",
            font=("Arial", 12),
            text_color="#aaaaaa"
        )
        subtitle_label.pack(side="left", padx=20, pady=15)
    
    def _create_tabs(self):
        """Create tabbed interface"""
        # Tab container
        tab_container = ctk.CTkFrame(self, fg_color="#0f0f0f")
        tab_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        tab_container.grid_rowconfigure(0, weight=1)
        tab_container.grid_columnconfigure(0, weight=1)
        
        self.notebook = ctk.CTkTabview(
            tab_container,
            fg_color="#1a1a1a",
            segmented_button_fg_color="#2a2a2a",
            segmented_button_selected_color="#3a7ebf",
            text_color="#ffffff",
            text_color_disabled="#888888"
        )
        self.notebook.grid(row=0, column=0, sticky="nsew")
        
        # Create tabs
        self.notebook.add("Suppliers")
        self.suppliers_tab = SuppliersTab(self.notebook.tab("Suppliers"))
        
        self.notebook.add("Categories")
        self.categories_tab = CategoriesTab(self.notebook.tab("Categories"))
        
        self.notebook.add("Products")
        self.products_tab = ProductsTab(self.notebook.tab("Products"))
        
        self.notebook.add("Orders")
        self.orders_tab = OrdersTab(self.notebook.tab("Orders"))


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
