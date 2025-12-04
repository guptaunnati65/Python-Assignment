#!/usr/bin/env python3
"""
library_manager_cli.py

Standalone Library Inventory Manager:
- Book class with issue/return/is_available
- LibraryInventory with JSON persistence (catalog.json by default)
- Menu-driven command-line interface
- Exception handling and logging

Run:
    python library_manager_cli.py
Optionally specify a custom catalog path:
    python library_manager_cli.py --catalog my_catalog.json
"""

from __future__ import annotations

import argparse
import json
import logging
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional

# ----------------------------
# Logging configuration
# ----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("library_manager")


# ----------------------------
# Book model
# ----------------------------
@dataclass
class Book:
    """Represents a book in the library."""

    title: str
    author: str
    isbn: str
    status: str = "available"  # 'available' or 'issued'

    def __str__(self) -> str:
        return f"{self.title} — {self.author} (ISBN: {self.isbn}) [{self.status}]"

    def to_dict(self) -> dict:
        """Dictionary representation for JSON serialization."""
        return asdict(self)

    def issue(self) -> bool:
        """Mark the book as issued. Return True if status changed."""
        if self.status == "available":
            self.status = "issued"
            return True
        return False

    def return_book(self) -> bool:
        """Mark the book as available. Return True if status changed."""
        if self.status == "issued":
            self.status = "available"
            return True
        return False

    def is_available(self) -> bool:
        return self.status == "available"


# ----------------------------
# Inventory manager
# ----------------------------
class LibraryInventory:
    """Manages a collection of Book objects with JSON persistence."""

    def __init__(self, catalog_path: Optional[Path] = None):
        self.catalog_path: Path = Path(catalog_path or Path.cwd() / "catalog.json")
        self.books: List[Book] = []
        logger.info("Using catalog file: %s", self.catalog_path)
        self.load()

    # Persistence
    def load(self) -> None:
        """Load books from JSON file. Handles missing or corrupted files."""
        try:
            if not self.catalog_path.exists():
                logger.info("Catalog file not found. Starting with empty inventory.")
                self.books = []
                return

            with self.catalog_path.open("r", encoding="utf-8") as fh:
                data = json.load(fh)

            if not isinstance(data, list):
                raise ValueError("Catalog JSON must be a list of book dictionaries.")

            loaded_books: List[Book] = []
            for idx, item in enumerate(data):
                if not isinstance(item, dict):
                    logger.warning("Skipping non-dict entry at index %d in catalog.", idx)
                    continue
                # Ensure required keys exist
                for key in ("title", "author", "isbn", "status"):
                    if key not in item:
                        item.setdefault(key, "")
                loaded_books.append(Book(**item))
            self.books = loaded_books
            logger.info("Loaded %d books.", len(self.books))
        except json.JSONDecodeError as exc:
            logger.error("Failed to parse catalog JSON: %s", exc)
            # Try to back up corrupt file
            try:
                corrupt_backup = self.catalog_path.with_suffix(".corrupt.json")
                self.catalog_path.rename(corrupt_backup)
                logger.error("Backed up corrupted catalog to: %s", corrupt_backup)
            except Exception as e:
                logger.error("Failed to back up corrupted catalog: %s", e)
            self.books = []
        except Exception as exc:
            logger.error("Unexpected error loading catalog: %s", exc)
            self.books = []

    def save(self) -> None:
        """Save current books to JSON file. Uses pretty-print formatting."""
        try:
            self.catalog_path.parent.mkdir(parents=True, exist_ok=True)
            with self.catalog_path.open("w", encoding="utf-8") as fh:
                json.dump([b.to_dict() for b in self.books], fh, indent=4, ensure_ascii=False)
            logger.info("Saved %d books to catalog.", len(self.books))
        except Exception as exc:
            logger.error("Failed to save catalog: %s", exc)

    # Operations
    def add_book(self, book: Book) -> None:
        """Add book to inventory; raises ValueError if ISBN already exists."""
        if self.search_by_isbn(book.isbn):
            raise ValueError(f"A book with ISBN {book.isbn} already exists.")
        self.books.append(book)
        logger.info("Added book: %s", book)
        self.save()

    def search_by_title(self, substring: str) -> List[Book]:
        key = substring.strip().lower()
        return [b for b in self.books if key in b.title.lower()]

    def search_by_isbn(self, isbn: str) -> Optional[Book]:
        isbn_key = isbn.strip()
        for b in self.books:
            if b.isbn == isbn_key:
                return b
        return None

    def display_all(self) -> List[str]:
        return [str(b) for b in self.books]

    def issue_book(self, isbn: str) -> bool:
        book = self.search_by_isbn(isbn)
        if not book:
            logger.info("Issue attempted for non-existent ISBN: %s", isbn)
            return False
        changed = book.issue()
        if changed:
            self.save()
            logger.info("Book issued: %s", book)
        else:
            logger.info("Issue failed (already issued): %s", book)
        return changed

    def return_book(self, isbn: str) -> bool:
        book = self.search_by_isbn(isbn)
        if not book:
            logger.info("Return attempted for non-existent ISBN: %s", isbn)
            return False
        changed = book.return_book()
        if changed:
            self.save()
            logger.info("Book returned: %s", book)
        else:
            logger.info("Return failed (already available): %s", book)
        return changed


# ----------------------------
# CLI helpers
# ----------------------------
def prompt(text: str) -> str:
    try:
        return input(text)
    except EOFError:
        print()
        return ""


def read_nonempty(prompt_text: str) -> str:
    while True:
        val = prompt(prompt_text).strip()
        if val:
            return val
        print("Input cannot be empty. Please try again.")


# ----------------------------
# Menu CLI
# ----------------------------
def run_cli(catalog_path: Optional[Path] = None) -> None:
    inv = LibraryInventory(catalog_path=catalog_path)

    MENU = """
Library Inventory Manager
1. Add Book
2. Issue Book
3. Return Book
4. View All Books
5. Search by Title
6. Search by ISBN
7. Exit
"""

    while True:
        print(MENU)
        choice = prompt("Enter choice (1-7): ").strip()
        if choice == "1":
            try:
                title = read_nonempty("Title: ")
                author = read_nonempty("Author: ")
                isbn = read_nonempty("ISBN: ")
                # Normalize status to available by default
                book = Book(title=title, author=author, isbn=isbn, status="available")
                inv.add_book(book)
                print("Book added successfully.")
            except ValueError as ve:
                print("Error:", ve)
            except Exception as exc:
                logger.error("Unexpected error adding book: %s", exc)
                print("An unexpected error occurred. See logs for details.")
        elif choice == "2":
            isbn = read_nonempty("ISBN to issue: ")
            success = inv.issue_book(isbn)
            if success:
                print("Book issued successfully.")
            else:
                print("Issue failed: ISBN not found or already issued.")
        elif choice == "3":
            isbn = read_nonempty("ISBN to return: ")
            success = inv.return_book(isbn)
            if success:
                print("Book returned successfully.")
            else:
                print("Return failed: ISBN not found or already available.")
        elif choice == "4":
            all_books = inv.display_all()
            if not all_books:
                print("No books in catalog.")
            else:
                print("\nCatalog:")
                for line in all_books:
                    print(" -", line)
        elif choice == "5":
            q = read_nonempty("Title search (substring): ")
            results = inv.search_by_title(q)
            if results:
                print(f"Found {len(results)} matching book(s):")
                for b in results:
                    print(" -", b)
            else:
                print("No matching titles found.")
        elif choice == "6":
            isbn = read_nonempty("ISBN search: ")
            book = inv.search_by_isbn(isbn)
            if book:
                print("Found:", book)
            else:
                print("ISBN not found.")
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Enter a number between 1 and 7.")


# ----------------------------
# Entry point + arg parsing
# ----------------------------
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Library Inventory Manager (CLI)")
    parser.add_argument(
        "--catalog",
        "-c",
        default=None,
        help="Path to catalog JSON file (default: ./catalog.json)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    catalog_path = Path(args.catalog) if args.catalog else None
    try:
        run_cli(catalog_path=catalog_path)
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")
    except Exception as exc:
        logger.exception("Unhandled exception in main: %s", exc)


if __name__ == "__main__":
    main()
