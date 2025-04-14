from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional, Dict


@dataclass
class Book:
    title: str
    author: str
    isbn: str
    publication_year: int
    available: bool = True
    current_borrower: Optional[str] = None
    due_date: Optional[datetime] = None

    def calculate_late_fee(self, fee_per_day: float = 0.25) -> float:
        """Calculate late fee for this book if it's overdue."""
        if self.available or not self.due_date:
            return 0.0

        if self.due_date > datetime.now():
            return 0.0

        days_late = (datetime.now() - self.due_date).days
        return days_late * fee_per_day


@dataclass
class Patron:
    name: str
    patron_id: str
    books_borrowed: List[str] = field(default_factory=list)


class Library:
    def __init__(self, name: str):
        self.name = name
        self.books: Dict[str, Book] = {}  # isbn -> Book
        self.patrons: Dict[str, Patron] = {}  # patron_id -> Patron

    def add_book(self, book: Book) -> None:
        """Add a book to the library collection."""
        self.books[book.isbn] = book

    def register_patron(self, patron: Patron) -> None:
        """Register a new patron with the library."""
        self.patrons[patron.patron_id] = patron

    def checkout_book(self, isbn: str, patron_id: str, loan_days: int = 14) -> bool:
        """Checkout a book to a patron."""
        # Check if book and patron exist
        if isbn not in self.books or patron_id not in self.patrons:
            return False

        book = self.books[isbn]
        patron = self.patrons[patron_id]

        # Check if book is available
        if not book.available:
            return False

        # Update book status
        book.available = False
        book.current_borrower = patron_id
        book.due_date = datetime.now() + timedelta(days=loan_days)

        # Update patron record
        patron.books_borrowed.append(isbn)

        return True

    def return_book(self, isbn: str) -> bool:
        """Return a book to the library."""
        if isbn not in self.books:
            return False

        book = self.books[isbn]

        # Check if book is actually checked out
        if book.available or book.current_borrower is None:
            return False

        # Get the patron who borrowed the book
        patron_id = book.current_borrower
        if patron_id in self.patrons:
            patron = self.patrons[patron_id]
            if isbn in patron.books_borrowed:
                patron.books_borrowed.remove(isbn)

        # Update book status
        book.available = True
        book.current_borrower = None
        book.due_date = None

        return True

    def get_overdue_books(self) -> List[Book]:
        """Get a list of all overdue books."""
        now = datetime.now()
        return [book for book in self.books.values()
                if not book.available and book.due_date and book.due_date < now]

    def search_books(self, query: str) -> List[Book]:
        """Search for books by title, author, or ISBN."""
        query = query.lower()
        results = []

        for book in self.books.values():
            if (query in book.title.lower() or
                    query in book.author.lower() or
                    query in book.isbn.lower()):
                results.append(book)

        return results
