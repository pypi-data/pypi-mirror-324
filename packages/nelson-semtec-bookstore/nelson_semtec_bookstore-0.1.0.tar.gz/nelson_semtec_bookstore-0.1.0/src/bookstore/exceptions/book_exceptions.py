"""Custom exceptions for the bookstore package."""


class BookstoreError(Exception):
    """Base exception class for all bookstore-related errors."""


class BookNotFoundError(BookstoreError):
    """Raised when a book cannot be found in the repository."""

    def __init__(self, isbn: str) -> None:
        """
        Initialize the exception.

        Args:
            isbn: The ISBN that was not found
        """
        super().__init__(f"Book with ISBN {isbn} not found")


class DuplicateBookError(BookstoreError):
    """Raised when attempting to add a book that already exists."""

    def __init__(self, isbn: str) -> None:
        """
        Initialize the exception.

        Args:
            isbn: The duplicate ISBN
        """
        super().__init__(f"Book with ISBN {isbn} already exists")


class InvalidISBNError(BookstoreError):
    """Raised when an invalid ISBN is provided."""

    def __init__(self, isbn: str, reason: str) -> None:
        """
        Initialize the exception.

        Args:
            isbn: The invalid ISBN
            reason: The reason why the ISBN is invalid
        """
        super().__init__(f"Invalid ISBN {isbn}: {reason}")


class InvalidPublicationYearError(BookstoreError):
    """Raised when an invalid publication year is provided."""

    def __init__(self, year: int, reason: str) -> None:
        """
        Initialize the exception.

        Args:
            year: The invalid publication year
            reason: The reason why the year is invalid
        """
        super().__init__(f"Invalid publication year {year}: {reason}")
