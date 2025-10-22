"""
scripts/init_env.py
-------------------
Automates local environment setup by creating required folders and .env file.
Useful for volunteers during Stage 1 setup.
"""

from pathlib import Path

REQUIRED_DIRS = ["data/raw", "data/cleaned", "logs"]

def create_env_file():
    env_path = Path(".env")
    if not env_path.exists():
        env_path.write_text("SCRAPER_MODE=local\nLOG_PATH=logs/\nDEBUG=True\nDATA_PATH=data/\n")
        print("Created .env file")
    else:
        print(".env already exists")

def create_directories():
    for folder in REQUIRED_DIRS:
        path = Path(folder)
        path.mkdir(parents=True, exist_ok=True)
        print(f"Ensured directory: {folder}")

if __name__ == "__main__":
    create_directories()
    create_env_file()
    print("Environment initialized successfully.")
