from src.db.database import create_phonetic_table
from scripts.seed_phonetics import seed_phonetics

if __name__ == "__main__":
    print("🛠️ Creating phonetic_rules table...")
    create_phonetic_table()
    print("🌱 Seeding phonetic data...")
    seed_phonetics()
    print("✨ Database is ready!")