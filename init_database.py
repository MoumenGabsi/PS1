"""
Simple database initialization script
Run: python init_database.py
"""
from database.create_tables import create_database, create_tables
from database.insert_tables import insert_data


def main():
    print("\n" + "="*60)
    print("🔧 Initializing Database...")
    print("="*60 + "\n")

    create_database()
    create_tables()
    insert_data()

    print("\n" + "="*60)
    print("✅ Database ready!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
