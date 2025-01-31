"""
Bookstore package for managing books.

This package demonstrates Python best practices including:
- Clean architecture
- Dependency injection
- Type hints
- Proper documentation
- Error handling
- Testing
"""

from .models.book import Book
from .repositories.book_repository import BookRepository, StorageBackend
from .exceptions.book_exceptions import (
    BookstoreError,
    BookNotFoundError,
    DuplicateBookError,
    InvalidISBNError,
    InvalidPublicationYearError,
)

__version__ = "0.1.0"

__all__ = [
    "Book",
    "BookRepository",
    "StorageBackend",
    "BookstoreError",
    "BookNotFoundError",
    "DuplicateBookError",
    "InvalidISBNError",
    "InvalidPublicationYearError",
]
