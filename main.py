from database_manager import DatabaseManager
from redundancy_checker import RedundancyChecker

def process_data(data_list):
    db = DatabaseManager()
    checker = RedundancyChecker()

    print(f"{'Data Content':<40} | {'Status':<15} | {'Message'}")
    print("-" * 80)

    for data in data_list:
        data_hash = checker.generate_hash(data)
        
        # Step 1: Identification
        if checker.is_redundant(db, data_hash):
            status = "REDUNDANT"
            message = "Duplicate detected. Skipped."
        else:
            # Step 2: Validation & Insertion
            status = "VERIFIED"
            success = db.add_entry(str(data), data_hash)
            if success:
                message = "Added to database."
            else:
                status = "ERROR"
                message = "Failed to add."

        print(f"{str(data)[:37] + '...':<40} | {status:<15} | {message}")

if __name__ == "__main__":
    # Sample Test Data
    sample_data = [
        "User: Alice, ID: 101",
        "User: Bob, ID: 102",
        "User: Alice, ID: 101", # Duplicate
        "User: Charlie, ID: 103",
        {"name": "David", "id": 104},
        {"name": "David", "id": 104} # Duplicate Dict
    ]

    print("Processing Sample Data...")
    process_data(sample_data)
    
    print("\nFinal Database State:")
    db = DatabaseManager()
    entries = db.get_all_entries()
    print(f"Total Entries: {len(entries)}")
    for row in entries:
        print(f"ID: {row[0]}, Content: {row[1]}")
