# PROJECT PLAN: Système de Gestion de Stock/Magasin

## Inventory & Store Management System (Tkinter + MySQL)

---

## 📋 PROJECT SPECIFICATION

- **Project Type**: Stock/Store Management (Gestion d'un stock/magasin)
- **Complexity**: Medium/Average
- **Main Entities**: Products, Categories, Suppliers, Orders
- **Language**: Python 3.10+
- **GUI Framework**: Tkinter or CustomTkinter (MANDATORY)
- **Database**: MySQL 8.x (REQUIRED - NO SQLite!)
- **Connector**: mysql-connector-python (MANDATORY)
- **Total Duration**: ~1 week
- **Grading**: 20 points total

---

## 🎯 GRADING BREAKDOWN (20 pts)

| Criterion                                | Points     |
| ---------------------------------------- | ---------- |
| Full CRUD operations (functional)        | 6 pts      |
| MySQL connection + parameterized queries | 4 pts      |
| Professional GUI (Tkinter/CustomTkinter) | 6 pts      |
| Error handling + input validation        | 2 pts      |
| Advanced features (search, sort, export) | 2 pts      |
| **TOTAL**                                | **20 pts** |

---

## 📊 DATABASE SCHEMA (MySQL)

### 4-Table Structure with Foreign Key Relationships

#### Table 1: `fournisseurs` (Suppliers)

```sql
CREATE TABLE fournisseurs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) UNIQUE NOT NULL,
    contact VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    telephone VARCHAR(20),
    adresse TEXT,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### Table 2: `categories` (Categories)

```sql
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### Table 3: `produits` (Products)

```sql
CREATE TABLE produits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    categorie_id INT NOT NULL,
    fournisseur_id INT NOT NULL,
    quantite_stock INT NOT NULL DEFAULT 0,
    prix_unitaire DECIMAL(10,2),
    prix_achat DECIMAL(10,2),
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (categorie_id) REFERENCES categories(id) ON DELETE CASCADE,
    FOREIGN KEY (fournisseur_id) REFERENCES fournisseurs(id) ON DELETE CASCADE
);
```

#### Table 4: `commandes` (Orders)

```sql
CREATE TABLE commandes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    produit_id INT NOT NULL,
    fournisseur_id INT NOT NULL,
    quantite INT NOT NULL,
    date_commande DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_livraison DATE,
    prix_total DECIMAL(10,2),
    statut ENUM('En attente', 'Livrée', 'Annulée') DEFAULT 'En attente',
    FOREIGN KEY (produit_id) REFERENCES produits(id) ON DELETE CASCADE,
    FOREIGN KEY (fournisseur_id) REFERENCES fournisseurs(id) ON DELETE CASCADE
);
```

---

## 🏗️ PROJECT STRUCTURE

```
SemesterialProject/
├── main.py                          # Entry point - main application window
├── config.py                        # Database config (externalized credentials)
├── requirements.txt                 # Python dependencies
├── README.md                        # Installation & usage instructions
│
├── database/
│   ├── __init__.py
│   ├── connection.py               # MySQL connection management + error handling
│   ├── suppliers_repo.py           # Suppliers CRUD operations
│   ├── categories_repo.py          # Categories CRUD operations
│   ├── products_repo.py            # Products CRUD operations
│   └── orders_repo.py              # Orders CRUD operations
│
├── gui/
│   ├── __init__.py
│   ├── main_window.py              # Main window with tabs/menu navigation
│   ├── suppliers_window.py         # Suppliers CRUD tab
│   ├── categories_window.py        # Categories CRUD tab
│   ├── products_window.py          # Products CRUD tab
│   ├── orders_window.py            # Orders CRUD tab
│   ├── dialogs.py                  # Reusable dialogs (Add/Edit/Delete/Error)
│   └── styles.py                   # Optional: CustomTkinter theme/styling
│
├── validators/
│   ├── __init__.py
│   └── input_validators.py         # Field validation utilities
│
├── utils/
│   ├── __init__.py
│   └── csv_export.py               # CSV export functionality
│
└── sql/
    ├── create_tables.sql           # CREATE TABLE statements + constraints
    └── test_data.sql               # Sample INSERT data (10-15 rows per table)
```

---

## ✅ IMPLEMENTATION PHASES

### **PHASE 1: PROJECT SETUP (Days 1-2)**

#### 1.1 Environment Setup

- [ ] Create virtual environment: `python -m venv venv`
- [ ] Activate venv: `venv\Scripts\activate` (Windows)
- [ ] Install dependencies:
  ```bash
  pip install mysql-connector-python customtkinter
  pip freeze > requirements.txt
  ```

#### 1.2 Create Project Folder Structure

- [ ] Create all folders: `database/`, `gui/`, `validators/`, `utils/`, `sql/`
- [ ] Create `__init__.py` in each package folder

#### 1.3 Database Connection Configuration

- [ ] Create `config.py` with externalized database credentials:
  ```python
  DB_CONFIG = {
      'host': 'localhost',
      'user': 'root',
      'password': 'your_password',
      'database': 'gestion_stock'
  }
  ```
- [ ] **⚠️ NEVER commit passwords in code - use environment variables or .env file**

#### 1.4 Create SQL Scripts

- [ ] Write `sql/create_tables.sql` with all 4 CREATE TABLE statements
- [ ] Write `sql/test_data.sql` with sample data (INSERT statements)
- [ ] Test SQL scripts on MySQL server to verify correctness

---

### **PHASE 2: DATABASE LAYER (Days 2-3)**

#### 2.1 Connection Management (`database/connection.py`)

```python
# Key requirements:
- get_connection() → returns mysql.connector.connect()
- Use try/except for all operations
- Always close cursor and connection
- Log errors clearly for debugging
```

#### 2.2 Suppliers Repository (`database/suppliers_repo.py`)

```python
class SuppliersRepository:
    def create(nom, contact, email, telephone, adresse) → int (supplier_id)
    def read(supplier_id) → dict
    def read_all() → list of dicts
    def update(supplier_id, nom, contact, email, telephone, adresse) → bool
    def delete(supplier_id) → bool
    def search(search_term) → list  # Search by name or contact
    def get_by_name(nom) → dict
```

#### 2.3 Categories Repository (`database/categories_repo.py`)

```python
class CategoriesRepository:
    def create(nom, description) → int (category_id)
    def read(category_id) → dict
    def read_all() → list of dicts
    def update(category_id, nom, description) → bool
    def delete(category_id) → bool  # Handle cascade warnings
    def search(search_term) → list
```

#### 2.4 Products Repository (`database/products_repo.py`)

```python
class ProductsRepository:
    def create(nom, categorie_id, fournisseur_id, quantite_stock, prix_unitaire, prix_achat) → int
    def read(product_id) → dict
    def read_all() → list of dicts
    def update(product_id, ...) → bool
    def delete(product_id) → bool
    def search(search_term) → list
    def get_by_category(category_id) → list
    def get_low_stock(threshold) → list  # Advanced feature
```

#### 2.5 Orders Repository (`database/orders_repo.py`)

```python
class OrdersRepository:
    def create(produit_id, fournisseur_id, quantite, date_livraison, prix_total, statut) → int
    def read(order_id) → dict
    def read_all() → list of dicts
    def update(order_id, ...) → bool
    def delete(order_id) → bool
    def search(search_term) → list
    def get_by_supplier(supplier_id) → list
    def get_by_product(product_id) → list
    def update_status(order_id, new_status) → bool
```

**⚠️ CRITICAL SQL Requirements:**

- ✅ USE PARAMETERIZED QUERIES ONLY: `cursor.execute("... WHERE id = %s", (id,))`
- ❌ NEVER USE: f-strings or string concatenation in SQL
- ✅ Always close cursor and connection
- ✅ Handle exceptions: `try/except` for all database operations

Example of CORRECT parameterized query:

```python
cursor.execute(
    "SELECT * FROM produits WHERE categorie_id = %s AND prix_unitaire > %s",
    (category_id, min_price)
)
```

---

### **PHASE 3: INPUT VALIDATION (Days 3)**

#### 3.1 Create `validators/input_validators.py`

```python
class InputValidators:
    # Field validation utilities
    - validate_not_empty(field_name, value) → (bool, error_message)
    - validate_positive_number(field_name, value) → (bool, error_message)
    - validate_email(email) → (bool, error_message)
    - validate_unique_name(table_name, name_field, value) → (bool, error_message)
    - validate_date_format(date_str) → (bool, error_message)
    - validate_price(price) → (bool, error_message)

    # Returns tuple: (is_valid, error_message or None)
```

---

### **PHASE 4: GUI LAYER (Days 4-6)**

#### 4.1 Main Window (`gui/main_window.py`)

```python
class MainWindow(tk.Tk):
    - Create main application window
    - Set minimum size (900x600) and make resizable
    - Create navigation structure:
      Option A: MenuBar at top with dropdown menus
      Option B: Sidebar with buttons (left side)

    - MenuBar structure:
      • File → Exit
      • Gestion → Fournisseurs, Catégories, Produits, Commandes
      • Rapports → Statistiques, Exporter en CSV
      • Aide → À propos

    - Use ttk.Notebook for tabbed interface
    - Each main entity (Suppliers, Categories, Products, Orders) gets a tab
```

#### 4.2 Reusable Dialog Components (`gui/dialogs.py`)

```python
# Standardized dialogs for all CRUD operations:

class AddUpdateDialog(tk.Toplevel):
    - Generic form dialog for CREATE and UPDATE operations
    - Auto-populate fields for UPDATE mode
    - Validation on Submit button
    - Return data or None if cancelled

class DeleteConfirmDialog:
    - Confirmation dialog before DELETE
    - Show record details being deleted
    - Return True/False

class ErrorDialog:
    - Display error messages clearly
    - Show exception details for debugging

class SuccessDialog:
    - Confirm successful operations
```

#### 4.3 Suppliers Tab (`gui/suppliers_window.py`)

```
┌─────────────────────────────────┐
│      GESTION DES FOURNISSEURS   │
├─────────────────────────────────┤
│  Search: [______________] [🔍]  │  ← Search/filter feature
├─────────────────────────────────┤
│ ID │ Nom │ Contact │ Email │... │
├─────────────────────────────────┤
│  1 │ ABC │ John    │ abc@...    │
│  2 │ XYZ │ Jane    │ xyz@...    │
│ ... (scrollable Treeview)  ↕↔   │
├─────────────────────────────────┤
│ [Ajouter] [Modifier] [Supprimer] │
│ [Actualiser]                     │
└─────────────────────────────────┘

Components:
- Search Entry + Search Button (filter by name/contact)
- Treeview with columns: ID, Nom, Contact, Email, Téléphone, Adresse
- Vertical + Horizontal scrollbars
- Buttons: Add, Edit, Delete, Refresh
- Double-click row to edit (or select + Edit button)
```

#### 4.4 Categories Tab (`gui/categories_window.py`)

```
Similar structure to Suppliers:
- Treeview: ID, Nom, Description
- CRUD buttons
- Search functionality
```

#### 4.5 Products Tab (`gui/products_window.py`)

**Most complex tab - shows relationships:**

```
┌──────────────────────────────────────────────┐
│           GESTION DES PRODUITS               │
├──────────────────────────────────────────────┤
│  Search: [______________] [🔍]               │
│  Filter by Category: [Dropdown ▼]            │  ← Advanced filtering
├──────────────────────────────────────────────┤
│ID│Nom│Catégorie│Fournisseur│Qt │Prix Unit │...
├──────────────────────────────────────────────┤
│ 1│Laptop│Electronics│DELL│50│800.00│
│ 2│Mouse│Electronics│DELL│200│15.50│
│ ... (scrollable, sortable)           ↕↔    │
├──────────────────────────────────────────────┤
│ [Ajouter] [Modifier] [Supprimer]            │
│ [Actualiser]                                │
└──────────────────────────────────────────────┘

Components:
- Treeview: ID, Nom, Catégorie (FK), Fournisseur (FK), Quantité, Prix Unitaire, Prix Achat
- Column sorting: Click header to sort ← Advanced feature
- Filter dropdown by Category
- Search by product name
- Add/Edit form shows dropdown for Category and Supplier selection
```

#### 4.6 Orders Tab (`gui/orders_window.py`)

```
Treeview: ID, Produit, Fournisseur, Quantité, Date Commande, Date Livraison, Prix Total, Statut
- Statut dropdown (En attente, Livrée, Annulée) with update functionality
- Filter by Status
- Search by product or supplier name
```

#### GUI Requirements Checklist:

- ✅ Window resizable with minimum dimensions
- ✅ ttk.Treeview for all data display (NOT plain text)
- ✅ Vertical AND horizontal scrollbars on tables
- ✅ messagebox for confirmations (delete) and errors
- ✅ Input validation labels (show error messages inline)
- ✅ Professional layout with proper spacing
- ✅ Keyboard shortcuts (optional but nice)
- ✅ If CustomTkinter: consistent theme throughout

---

### **PHASE 5: ADVANCED FEATURES (Days 6-7)**

Implement **minimum 2 of these 4 features** (you need all for full points):

#### Feature 1: Search & Filter ⭐ (EASY - HIGH VALUE)

```python
# Suppliers tab:
- Search entry field
- On-the-fly filtering as user types
- Highlight matching rows
- Works by Nom or Contact

# Products tab:
- Search by name
- Filter dropdown by Category
- Combine both filters

# Orders tab:
- Search by product or supplier name
- Filter by status (dropdown)
```

#### Feature 2: Column Sorting ⭐ (EASY - HIGH VALUE)

```python
# Click Treeview column header to sort
# First click: ascending
# Second click: descending
# Visual indicator (arrow or highlight)

# Implementation:
- Bind <Button-1> to Treeview heading
- On click: get_children() → sort → delete all items → re-insert sorted
```

#### Feature 3: Statistics (MEDIUM)

```python
# Add "Rapports" menu with statistics:
- Total suppliers
- Total categories
- Total products
- Total stock value (sum of quantity × unit_price)
- Average product price
- Total order value
- Orders by status
```

#### Feature 4: CSV Export (EASY)

```python
# Add "Export to CSV" button on each tab
# Export current Treeview data to CSV file
# Using csv module or pandas (if installed)
# File saved to Desktop or user selects location
```

---

### **PHASE 6: DATABASE SETUP (Day 7)**

#### 6.1 MySQL Setup

- [ ] Create MySQL database: `CREATE DATABASE gestion_stock;`
- [ ] Import create_tables.sql: `mysql -u root -p gestion_stock < sql/create_tables.sql`
- [ ] Import test_data.sql: `mysql -u root -p gestion_stock < sql/test_data.sql`
- [ ] Verify tables created: `SHOW TABLES;`

#### 6.2 Verify Database

```sql
-- Check all tables exist
SHOW TABLES;

-- Check table structures
DESCRIBE fournisseurs;
DESCRIBE categories;
DESCRIBE produits;
DESCRIBE commandes;

-- Check foreign keys
SELECT * FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE;
```

---

### **PHASE 7: TESTING & QA (Days 7-8)**

#### 7.1 CRUD Testing

For each entity (Suppliers, Categories, Products, Orders):

- [ ] **CREATE**: Add new record via form → Verify in database → Verify appears in Treeview
- [ ] **READ**: Display all records → Double-click to view details
- [ ] **UPDATE**: Edit record → Save → Verify changes in database → Treeview refreshes
- [ ] **DELETE**: Delete record → Confirm dialog → Verify removed from database

#### 7.2 Foreign Key & Cascade Testing

- [ ] Add product with category and supplier
- [ ] Delete supplier → orders should cascade delete
- [ ] Delete category → products should cascade delete
- [ ] Verify referential integrity enforced

#### 7.3 Advanced Features Testing

- [ ] **Search/Filter**: Type term → Results filter correctly
- [ ] **Column Sort**: Click header → Data sorts → Click again reverses
- [ ] **Statistics**: Totals calculate correctly
- [ ] **CSV Export**: File created with all data intact

#### 7.4 Edge Cases & Error Testing

- [ ] Empty field submission → Error message displayed
- [ ] Duplicate name submission → Error message
- [ ] Negative number → Error message
- [ ] Invalid email format → Error message (if applicable)
- [ ] Database offline → Connection error displayed clearly
- [ ] Circular reference attempts → Prevented/warned
- [ ] Special characters in fields → Handled correctly (SQL injection test)

#### 7.5 Performance Testing

- [ ] Load with 1000+ records → Treeview responsive
- [ ] Search/filter fast enough
- [ ] Sort operation completes quickly

---

### **PHASE 8: DOCUMENTATION & PACKAGING (Day 8)**

#### 8.1 Create README.md

````markdown
# Système de Gestion de Stock / Store Management System

## Requirements

- Python 3.10+
- MySQL 8.x
- Windows/Linux/Mac

## Installation

### 1. Clone/Download Project

```bash
cd path/to/SemesterialProject
```
````

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Database

Edit `config.py` with your MySQL credentials:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'gestion_stock'
}
```

### 5. Create MySQL Database

```bash
# Open MySQL and run:
CREATE DATABASE gestion_stock;
USE gestion_stock;
SOURCE sql/create_tables.sql;
SOURCE sql/test_data.sql;
```

### 6. Run Application

```bash
python main.py
```

## Features

- ✅ Full CRUD operations for Suppliers, Categories, Products, Orders
- ✅ Real-time search and filtering
- ✅ Column sorting in data tables
- ✅ Input validation and error handling
- ✅ MySQL database with foreign key constraints
- ✅ Professional Tkinter GUI
- ✅ CSV export functionality

## Project Structure

See DETAILED_PROJECT_PLAN.md for complete structure

## Database Schema

- `fournisseurs` (Suppliers)
- `categories` (Categories)
- `produits` (Products)
- `commandes` (Orders)

See sql/create_tables.sql for full schema

## Usage

1. Launch application
2. Use menu or tabs to navigate entities
3. Add/Edit/Delete records using forms
4. Search and filter data
5. Export to CSV as needed

## Notes

- All SQL queries are parameterized (safe from injection)
- Passwords NOT stored in code
- Database credentials in config.py
- Tested on MySQL 8.0+

```

#### 8.2 Update requirements.txt
```

mysql-connector-python==8.0.33
customtkinter==4.6.2

````

#### 8.3 Final Code Review
- [ ] No hardcoded passwords
- [ ] All queries parameterized
- [ ] All exceptions handled properly
- [ ] Connections always closed
- [ ] No SQLite, no ORM
- [ ] Clean code with comments
- [ ] Professional GUI
- [ ] All CRUD operations working
- [ ] At least 2 advanced features implemented

#### 8.4 Package for Submission
```bash
# Create archive with proper name
Gabsi_AbdelMoumen_GestionStock.zip

Contents:
├── main.py
├── config.py
├── requirements.txt
├── README.md
├── DETAILED_PROJECT_PLAN.md (optional but helpful)
├── database/ (all .py files)
├── gui/ (all .py files)
├── validators/ (all .py files)
├── utils/ (all .py files)
└── sql/ (create_tables.sql, test_data.sql)
````

---

## 🗂️ FILE CHECKLIST

### Python Files (12+ files)

- [ ] main.py
- [ ] config.py
- [ ] database/**init**.py
- [ ] database/connection.py
- [ ] database/suppliers_repo.py
- [ ] database/categories_repo.py
- [ ] database/products_repo.py
- [ ] database/orders_repo.py
- [ ] gui/**init**.py
- [ ] gui/main_window.py
- [ ] gui/suppliers_window.py
- [ ] gui/categories_window.py
- [ ] gui/products_window.py
- [ ] gui/orders_window.py
- [ ] gui/dialogs.py
- [ ] validators/**init**.py
- [ ] validators/input_validators.py
- [ ] utils/**init**.py
- [ ] utils/csv_export.py

### SQL Files (2 files)

- [ ] sql/create_tables.sql
- [ ] sql/test_data.sql

### Documentation Files (3 files)

- [ ] README.md
- [ ] requirements.txt
- [ ] DETAILED_PROJECT_PLAN.md

---

## ⚠️ CRITICAL RULES

1. **Database Connection**: ALWAYS use parameterized queries with `%s` placeholder
   - ✅ `cursor.execute("SELECT * FROM fournisseurs WHERE id = %s", (supplier_id,))`
   - ❌ `cursor.execute(f"SELECT * FROM fournisseurs WHERE id = {supplier_id}")`

2. **Connection Management**: Always close connections

   ```python
   try:
       cursor = conn.cursor()
       cursor.execute(...)
       result = cursor.fetchall()
   except Exception as e:
       messagebox.showerror("Database Error", str(e))
   finally:
       cursor.close()
       conn.close()
   ```

3. **No ORM/SQLite**: Use ONLY mysql-connector-python for database

4. **Externalize Credentials**: NEVER hardcode passwords
   - Use config.py and add to .gitignore

5. **GUI Only**: NO CLI interface - use Tkinter/CustomTkinter

6. **Foreign Keys**: All relationships properly defined with ON DELETE CASCADE

7. **Validation**: Validate ALL inputs before database operation

8. **Error Handling**: Wrap ALL database operations in try/except

9. **Minimum Tables**: 4 tables (Suppliers, Categories, Products, Orders)

10. **Advanced Features**: Implement at LEAST 2 of 4 features

---

## 📈 EXPECTED TIMELINE

| Phase     | Description               | Duration       | Status      |
| --------- | ------------------------- | -------------- | ----------- |
| 1         | Setup & Configuration     | 1-2 days       | Not started |
| 2         | Database Layer            | 1-2 days       | Not started |
| 3         | Input Validators          | 0.5 days       | Not started |
| 4         | GUI Implementation        | 2-3 days       | Not started |
| 5         | Advanced Features         | 1 day          | Not started |
| 6         | Database Setup            | 0.5 days       | Not started |
| 7         | Testing & QA              | 1 day          | Not started |
| 8         | Documentation & Packaging | 0.5 days       | Not started |
| **TOTAL** |                           | **~8-10 days** |             |

---

## 🎯 SUCCESS CRITERIA

Your project is successful when:

1. ✅ All 4 CRUD operations work for each entity (24 points max)
2. ✅ MySQL connection with parameterized queries (no hardcoded values)
3. ✅ Professional GUI with Treeview tables and proper layout
4. ✅ Search/filter + column sorting working (2 advanced features)
5. ✅ Input validation preventing invalid data
6. ✅ Error messages display clearly
7. ✅ README with proper setup instructions
8. ✅ SQL scripts provided and working
9. ✅ Code is original and well-commented
10. ✅ Final package: `Gabsi_AbdelMoumen_GestionStock.zip`

---

**You're ready to begin Phase 1! Let me know when you want to start coding.**
