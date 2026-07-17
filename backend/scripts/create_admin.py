#!/usr/bin/env python3
"""Create the default admin user.

Usage: python scripts/create_admin.py
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.database import SyncSessionLocal
from app.core.security import get_password_hash
from app.models.user import User

DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "fortiq-demo-2024"


def main():
    """Create the default admin user if not exists."""
    print(f"Creating admin user: {DEFAULT_USERNAME}")

    session = SyncSessionLocal()
    try:
        # Check if user already exists
        existing = session.query(User).filter(User.username == DEFAULT_USERNAME).first()
        if existing:
            print(f"User '{DEFAULT_USERNAME}' already exists. Skipping.")
            return

        # Create user
        hashed_password = get_password_hash(DEFAULT_PASSWORD)
        user = User(username=DEFAULT_USERNAME, hashed_password=hashed_password)
        session.add(user)
        session.commit()

        print(f"Created user '{DEFAULT_USERNAME}' with password '{DEFAULT_PASSWORD}'")
        print("Remember to change this password in production!")

    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
