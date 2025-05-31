import os
import subprocess # Recommended over os.system for better security and control
from datetime import datetime
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BACKUP_FOLDER = "backups/"
os.makedirs(BACKUP_FOLDER, exist_ok=True) # Ensure backup folder exists

def backup_database_service():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # Use .gz for a compressed archive file. mongodump can handle gzipping.
    backup_archive_file = os.path.join(BACKUP_FOLDER, f"backup_{timestamp}.gz")

    # Command using --archive for a single output file, and --gzip for compression.
    # Add --uri="mongodb://user:pass@host:port/dbname" if your MongoDB needs authentication
    # or is not running on localhost with default port.
    command = [
        "mongodump",
        f"--archive={backup_archive_file}",
        "--gzip"
        # Example: "--uri=mongodb://localhost:27017/mydatabase"
    ]
    
    logger.info(f"Executing backup command: {' '.join(command)}")
    try:
        # Using subprocess.run for better error handling and security
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        logger.info(f"Backup successful: {result.stdout}")
        return {"message": "Backup completed successfully", "backup_file": backup_archive_file}
    except subprocess.CalledProcessError as e:
        logger.error(f"Backup failed. Error: {e.stderr}")
        # Clean up partially created file if it exists
        if os.path.exists(backup_archive_file):
            try:
                os.remove(backup_archive_file)
                logger.info(f"Removed incomplete backup file: {backup_archive_file}")
            except OSError as oe:
                logger.error(f"Error removing incomplete backup file {backup_archive_file}: {oe}")
        return {"message": "Backup failed", "error": e.stderr, "backup_file": None}
    except FileNotFoundError:
        logger.error("mongodump command not found. Ensure MongoDB Database Tools are installed and in PATH.")
        return {"message": "Backup failed", "error": "mongodump command not found.", "backup_file": None}

def restore_database_service(backup_file_name: str):
    """
    Restores the database from a given backup archive file name.
    backup_file_name should be the name of the file within the BACKUP_FOLDER, e.g., "backup_2025-05-25_16-00-00.gz"
    """
    backup_archive_file = os.path.join(BACKUP_FOLDER, backup_file_name)

    if not os.path.exists(backup_archive_file) or not os.path.isfile(backup_archive_file):
        logger.error(f"Backup file not found: {backup_archive_file}")
        return {"message": "Restore failed", "error": "Backup file not found."}

    # Command using --archive for restoring from a single file, and --gzip if it was compressed.
    # --drop will drop collections before restoring.
    # Add --uri="mongodb://user:pass@host:port/dbname" if needed.
    command = [
        "mongorestore",
        "--drop",
        f"--archive={backup_archive_file}",
        "--gzip"
        # Example: "--uri=mongodb://localhost:27017/mydatabase"
    ]

    logger.info(f"Executing restore command: {' '.join(command)}")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        logger.info(f"Restore successful: {result.stdout}")
        return {"message": "Database restored successfully from backup", "restored_file": backup_archive_file}
    except subprocess.CalledProcessError as e:
        logger.error(f"Restore failed. Error: {e.stderr}")
        return {"message": "Restore failed", "error": e.stderr}
    except FileNotFoundError:
        logger.error("mongorestore command not found. Ensure MongoDB Database Tools are installed and in PATH.")
        return {"message": "Restore failed", "error": "mongorestore command not found."}

# Example of a function to list backups (optional, but useful)
def list_backups_service():
    try:
        files = [
            f for f in os.listdir(BACKUP_FOLDER) 
            if os.path.isfile(os.path.join(BACKUP_FOLDER, f)) and f.startswith("backup_") and f.endswith(".gz")
        ]
        return {"backups": sorted(files, reverse=True)}
    except Exception as e:
        logger.error(f"Error listing backups: {e}")
        return {"backups": [], "error": str(e)}