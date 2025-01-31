"""Test module for the Book model and BookRepository."""

from datetime import datetime

import pytest

from bookstore import (
    Book,
    BookRepository,
    DuplicateBookError,
    InvalidISBNError,
    InvalidPublicationYearError,
)


@pytest.fixture
def sample_book() -> Book:
    """
    Fixture providing a valid book instance for testing.

    Returns:
        Book: A sample book instance
    """
    return Book(
        isbn="978-0-7475-3269-9",
        title="Test Book",
        author="Test Author",
        publication_year=2020,
        description="A book for testing",
    )


@pytest.fixture
def repository() -> BookRepository:
    """
    Fixture providing a fresh repository instance for testing.

    Returns:
        BookRepository: A new repository instance
    """
    return BookRepository()


class TestBook:
    """Test suite for the Book model."""

    def test_valid_book_creation(self, sample_book: Book) -> None:
        """Test that a book can be created with valid data."""
        assert sample_book.isbn == "978-0-7475-3269-9"
        assert sample_book.title == "Test Book"
        assert sample_book.author == "Test Author"
        assert sample_book.publication_year == 2020
        assert sample_book.description == "A book for testing"
        assert isinstance(sample_book.added_at, datetime)

    def test_invalid_isbn(self) -> None:
        """Test that invalid ISBN raises appropriate error."""
        with pytest.raises(InvalidISBNError):
            Book(
                isbn="invalid-isbn",
                title="Test Book",
                author="Test Author",
                publication_year=2020,
            )

    def test_future_publication_year(self) -> None:
        """Test that future publication year raises appropriate error."""
        future_year = datetime.now().year + 1
        with pytest.raises(InvalidPublicationYearError):
            Book(
                isbn="978-0-7475-3269-9",
                title="Test Book",
                author="Test Author",
                publication_year=future_year,
            )


class TestBookRepository:
    """Test suite for the BookRepository class."""

    def test_add_and_retrieve_book(
        self, repository: BookRepository, sample_book: Book
    ) -> None:
        """Test adding a book and retrieving it by ISBN."""
        repository.add_book(sample_book)
        retrieved_book = repository.get_book_by_isbn(sample_book.isbn)

        assert retrieved_book is not None
        assert retrieved_book.isbn == sample_book.isbn
        assert retrieved_book.title == sample_book.title

    def test_duplicate_book(
        self, repository: BookRepository, sample_book: Book
    ) -> None:
        """Test that adding a duplicate book raises appropriate error."""
        repository.add_book(sample_book)

        with pytest.raises(DuplicateBookError):
            repository.add_book(sample_book)

    def test_delete_book(self, repository: BookRepository, sample_book: Book) -> None:
        """Test deleting a book from the repository."""
        repository.add_book(sample_book)
        repository.delete_book(sample_book.isbn)

        assert repository.get_book_by_isbn(sample_book.isbn) is None
