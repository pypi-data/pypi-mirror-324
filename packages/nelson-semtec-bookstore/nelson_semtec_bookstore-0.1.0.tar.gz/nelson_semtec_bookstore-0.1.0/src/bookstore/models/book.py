"""Book model module for representing book entities in the system."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ..exceptions.book_exceptions import InvalidISBNError, InvalidPublicationYearError


@dataclass
class Book:
    """
    Represents a book in the bookstore system.

    This class demonstrates proper type hints, documentation, and validation.
    It uses the dataclass decorator to automatically generate special methods
    like __init__, __repr__, and __eq__.

    Attributes:
        isbn (str): The International Standard Book Number (ISBN-13)
        title (str): The book's title
        author (str): The book's author
        publication_year (int): Year when the book was published
        description (Optional[str]): A brief description of the book
        added_at (datetime): Timestamp when the book was added to the system

    Example:
        >>> book = Book(
        ...     isbn="978-0-7475-3269-9",
        ...     title="Harry Potter and the Philosopher's Stone",
        ...     author="J.K. Rowling",
        ...     publication_year=1997,
        ...     description="The first book in the Harry Potter series"
        ... )
    """

    isbn: str
    title: str
    author: str
    publication_year: int
    description: Optional[str] = None
    added_at: datetime = datetime.now()

    def __post_init__(self) -> None:
        """
        Validates the book's attributes after initialization.

        Raises:
            ValueError: If ISBN format is invalid or publication year is in the future
        """
        if self.isbn == "" or self.isbn is None:
            raise ValueError("ISBN cannot be empty")

        if self.title == "" or self.title is None:
            raise ValueError("Title cannot be empty")

        self._validate_isbn()
        self._validate_publication_year()

    def _validate_isbn(self) -> None:
        """
        Validates the ISBN format.

        Raises:
            InvalidISBNError: If ISBN format is invalid
        """
        # Remove hyphens and spaces for validation
        clean_isbn = self.isbn.replace("-", "").replace(" ", "")
        if not (len(clean_isbn) == 13 and clean_isbn.isdigit()):
            raise InvalidISBNError(
                self.isbn, "ISBN must be 13 digits (excluding hyphens and spaces)"
            )

    def _validate_publication_year(self) -> None:
        """
        Validates that the publication year is not in the future.

        Raises:
            InvalidPublicationYearError: If publication year is in the future
        """
        current_year = datetime.now().year
        if self.publication_year > current_year:
            raise InvalidPublicationYearError(
                self.publication_year, "Publication year cannot be in the future"
            )

    def get_age(self) -> int:
        """
        Calculates the age of the book in years.

        Returns:
            int: The number of years since the book was published

        Example:
            >>> book = Book(isbn="978-0-7475-3269-9", title="Example",
            ...            author="Author", publication_year=2000)
            >>> current_year = datetime.now().year
            >>> book.get_age() == current_year - 2000
            True
        """
        return datetime.now().year - self.publication_year
