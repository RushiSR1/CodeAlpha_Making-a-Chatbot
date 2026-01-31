import hashlib
import json

class RedundancyChecker:
    @staticmethod
    def generate_hash(data: dict | str) -> str:
        """
        Generates a SHA-256 hash for the given data.
        """
        if isinstance(data, dict):
            # Sort keys to ensure consistent hashing for dictionaries
            serialized = json.dumps(data, sort_keys=True)
        else:
            serialized = str(data)
            
        return hashlib.sha256(serialized.encode('utf-8')).hexdigest()

    @staticmethod
    def is_redundant(db_manager, data_hash: str) -> bool:
        """
        Checks if the data hash already exists in the database.
        """
        return db_manager.entry_exists(data_hash)
