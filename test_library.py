import pytest
from datetime import datetime, timedelta
from library_system import Book, Patron, Library


@pytest.fixture
def sample_library():
    """Create a sample library with some books and patrons."""
    lib = Library("Test Library")

    # Add some books
    books = [
        Book("Python Crash Course", "Eric Matthes", "978-1593279288", 2019),
        Book("Clean Code", "Robert Martin", "978-0132350884", 2008),
        Book("The Pragmatic Programmer", "Andrew Hunt", "978-0201616224", 1999)
    ]

    for book in books:
        lib.add_book(book)

    # Add some patrons
    patrons = [
        Patron("Alice Smith", "P001"),
        Patron("Bob Johnson", "P002")
    ]

    for patron in patrons:
        lib.register_patron(patron)

    return lib


def test_add_book(sample_library):
    """Test adding a book to the library."""
    new_book = Book("Effective Python", "Brett Slatkin", "978-0134853987", 2019)
    sample_library.add_book(new_book)

    assert new_book.isbn in sample_library.books
    assert sample_library.books[new_book.isbn].title == "Effective Python"


def test_register_patron(sample_library):
    """Test registering a new patron."""
    new_patron = Patron("Charlie Brown", "P003")
    sample_library.register_patron(new_patron)

    assert new_patron.patron_id in sample_library.patrons
    assert sample_library.patrons[new_patron.patron_id].name == "Charlie Brown"


def test_checkout_book(sample_library):
    """Test checking out a book."""
    isbn = "978-1593279288"  # Python Crash Course
    patron_id = "P001"  # Alice

    result = sample_library.checkout_book(isbn, patron_id)

    assert result is True
    assert sample_library.books[isbn].available is False
    assert sample_library.books[isbn].current_borrower == patron_id
    assert isbn in sample_library.patrons[patron_id].books_borrowed


def test_return_book(sample_library):
    """Test returning a book."""
    # First checkout a book
    isbn = "978-0132350884"  # Clean Code
    patron_id = "P002"  # Bob

    sample_library.checkout_book(isbn, patron_id)

    # Now return the book
    result = sample_library.return_book(isbn)

    assert result is True
    assert sample_library.books[isbn].available is True
    assert sample_library.books[isbn].current_borrower is None
    assert isbn not in sample_library.patrons[patron_id].books_borrowed


def test_get_overdue_books(sample_library):
    """Test identifying overdue books."""
    # Checkout a book with a custom due date in the past
    isbn = "978-0201616224"  # The Pragmatic Programmer
    patron_id = "P001"  # Alice

    # Checkout the book
    sample_library.checkout_book(isbn, patron_id)

    # Manually set the due date to be in the past
    sample_library.books[isbn].due_date = datetime.now() - timedelta(days=1)

    overdue_books = sample_library.get_overdue_books()

    assert len(overdue_books) == 1
    assert overdue_books[0].isbn == isbn


def test_calculate_late_fee():
    """Test calculating late fees for an overdue book."""
    book = Book("Test Book", "Test Author", "123456789", 2020)
    book.available = False
    book.due_date = datetime.now() - timedelta(days=5)

    fee = book.calculate_late_fee(0.25)

    assert fee == 5 * 0.25  # 5 days late at $0.25 per day


def test_search_books(sample_library):
    """Test searching for books."""
    # Search by title
    results = sample_library.search_books("python")
    assert len(results) == 1
    assert results[0].title == "Python Crash Course"

    # Search by author
    results = sample_library.search_books("martin")
    assert len(results) == 1
    assert results[0].author == "Robert Martin"
