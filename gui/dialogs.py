"""
Reusable Dialog Components for CRUD operations - CustomTkinter Version
"""
import customtkinter as ctk
from tkinter import messagebox


class ErrorDialog:
    """Display error messages"""
    @staticmethod
    def show(parent, title, message):
        messagebox.showerror(title, message, parent=parent)


class SuccessDialog:
    """Confirm successful operations"""
    @staticmethod
    def show(parent, title, message):
        messagebox.showinfo(title, message, parent=parent)


class DeleteConfirmDialog:
    """Confirmation dialog before DELETE"""
    @staticmethod
    def show(parent, title, record_info):
        message = f"Are you sure you want to delete this record?\n\n{record_info}"
        result = messagebox.askyesno(title, message, parent=parent)
        return result


class AddUpdateDialog(ctk.CTkToplevel):
    """Generic form dialog for CREATE and UPDATE operations"""
    
    def __init__(self, parent, title, fields, initial_values=None):
        """
        parent: parent window
        title: dialog title
        fields: list of tuples (field_name, field_type, required)
        initial_values: dict with field names as keys (for UPDATE mode)
        """
        super().__init__(parent)
        self.title(title)
        self.geometry("450x400")
        self.resizable(False, False)
        self.result_data = None
        
        self.fields = fields
        self.entries = {}
        self.dropdowns = {}
        
        self._create_form(initial_values)
        
        # Center dialog on parent
        self.transient(parent)
        self.grab_set()
        self._center_on_parent(parent)
    
    def _center_on_parent(self, parent):
        """Center dialog on screen"""
        self.update_idletasks()
        
        # Get dialog dimensions
        dialog_width = self.winfo_width()
        dialog_height = self.winfo_height()
        
        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calculate center position on screen
        x = (screen_width - dialog_width) // 2
        y = (screen_height - dialog_height) // 2
        
        # Set geometry
        self.geometry(f"+{x}+{y}")
    
    def _create_form(self, initial_values):
        """Create form fields dynamically"""
        # Main container
        main_frame = ctk.CTkFrame(self, fg_color="#1a1a1a")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Create scrollable frame for fields
        canvas_frame = ctk.CTkScrollableFrame(main_frame, fg_color="#1a1a1a")
        canvas_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Create fields
        for field_name, field_type, required in self.fields:
            label_text = f"{field_name}" + (" *" if required else "")
            label = ctk.CTkLabel(canvas_frame, text=label_text, text_color="#ffffff", font=("Arial", 12, "bold"))
            label.pack(anchor="w", pady=(10, 3))
            
            if field_type == 'dropdown':
                combo = ctk.CTkComboBox(canvas_frame, state="readonly", fg_color="#2a2a2a", text_color="#ffffff", 
                                       button_color="#3a7ebf", dropdown_fg_color="#2a2a2a", dropdown_text_color="#ffffff")
                combo.pack(anchor="w", pady=(0, 8), fill="x")
                self.dropdowns[field_name] = combo
                self.entries[field_name] = combo
            else:
                entry = ctk.CTkEntry(canvas_frame, fg_color="#2a2a2a", text_color="#ffffff", 
                                    border_color="#3a7ebf", border_width=1)
                entry.pack(anchor="w", pady=(0, 8), fill="x")
                self.entries[field_name] = entry
            
            # Set initial value if provided
            if initial_values and field_name in initial_values:
                value = initial_values[field_name]
                if field_type == 'dropdown':
                    self.dropdowns[field_name].set(value)
                else:
                    entry.insert(0, str(value))
        
        # Buttons frame
        button_frame = ctk.CTkFrame(main_frame, fg_color="#1a1a1a")
        button_frame.pack(fill="x", pady=(10, 0))
        
        save_btn = ctk.CTkButton(button_frame, text="Save", command=self._on_save, 
                                fg_color="#3a7ebf", hover_color="#2a5a9f", text_color="#ffffff")
        save_btn.pack(side="left", padx=5, fill="x", expand=True)
        
        cancel_btn = ctk.CTkButton(button_frame, text="Cancel", command=self._on_cancel,
                                  fg_color="#555555", hover_color="#666666", text_color="#ffffff")
        cancel_btn.pack(side="left", padx=5, fill="x", expand=True)
    
    def _on_save(self):
        """Collect form data and close"""
        self.result_data = {}
        for field_name, entry in self.entries.items():
            self.result_data[field_name] = entry.get()
        self.destroy()
    
    def _on_cancel(self):
        """Cancel and close without saving"""
        self.result_data = None
        self.destroy()
    
    def get_result(self):
        """Wait for dialog to close and return result"""
        self.wait_window()
        return self.result_data
