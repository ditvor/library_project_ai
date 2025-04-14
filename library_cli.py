import cmd
from datetime import datetime
from library_system import Book, Patron, Library


class LibraryCLI(cmd.Cmd):
    intro = "Welcome to the Library Management System. Type 'help' to see available commands."
    prompt = "Library> "

    def __init__(self):
        super().__init__()
        self.library = Library("My Library")

    def do_add_book(self, arg):
        """Add a book to the library. Format: add_book title|author|isbn|publication_year"""
        try:
            title, author, isbn, year = arg.split('|')
            book = Book(title, author, isbn, int(year))
            self.library.add_book(book)
            print(f"Added book: {title} by {author}")
        except ValueError:
            print("Error: Use format 'add_book title|author|isbn|publication_year'")

    def do_add_patron(self, arg):
        """Add a patron to the library. Format: add_patron name|id"""
        try:
            name, patron_id = arg.split('|')
            patron = Patron(name, patron_id)
            self.library.register_patron(patron)
            print(f"Added patron: {name} with ID {patron_id}")
        except ValueError:
            print("Error: Use format 'add_patron name|id'")

    def do_checkout(self, arg):
        """Checkout a book to a patron. Format: checkout isbn|patron_id"""
        try:
            isbn, patron_id = arg.split('|')
            if self.library.checkout_book(isbn, patron_id):
                print(f"Book {isbn} checked out to patron {patron_id}")
            else:
                print("Checkout failed. Check book availability and patron ID.")
        except ValueError:
            print("Error: Use format 'checkout isbn|patron_id'")

    def do_return(self, arg):
        """Return a book to the library. Format: return isbn"""
        if self.library.return_book(arg):
            print(f"Book {arg} returned successfully")
        else:
            print("Return failed. Check if the book exists and is checked out.")

    def do_list_books(self, arg):
        """List all books in the library."""
        if not self.library.books:
            print("No books in the library.")
            return

        print("\nLibrary Books:")
        print("=" * 80)
        print(f"{'Title':<30} {'Author':<20} {'ISBN':<15} {'Status':<15}")
        print("-" * 80)

        for book in self.library.books.values():
            status = "Available" if book.available else f"Borrowed by {book.current_borrower}"
            print(f"{book.title[:30]:<30} {book.author[:20]:<20} {book.isbn:<15} {status:<15}")

    def do_search(self, arg):
        """Search for books. Format: search query"""
        results = self.library.search_books(arg)
        if not results:
            print(f"No books found matching '{arg}'")
            return

        print(f"\nSearch results for '{arg}':")
        print("=" * 80)
        print(f"{'Title':<30} {'Author':<20} {'ISBN':<15} {'Status':<15}")
        print("-" * 80)

        for book in results:
            status = "Available" if book.available else f"Borrowed by {book.current_borrower}"
            print(f"{book.title[:30]:<30} {book.author[:20]:<20} {book.isbn:<15} {status:<15}")

    def do_overdue(self, arg):
        """List all overdue books."""
        overdue_books = self.library.get_overdue_books()

        if not overdue_books:
            print("No overdue books.")
            return

        print("\nOverdue Books:")
        print("=" * 80)
        print(f"{'Title':<30} {'Borrower':<15} {'Due Date':<20} {'Late Fee':<10}")
        print("-" * 80)

        for book in overdue_books:
            due_date_str = book.due_date.strftime("%Y-%m-%d %H:%M") if book.due_date else "N/A"
            late_fee = f"${book.calculate_late_fee():.2f}"
            print(f"{book.title[:30]:<30} {book.current_borrower:<15} {due_date_str:<20} {late_fee:<10}")

    def do_quit(self, arg):
        """Exit the program."""
        print("Thank you for using the Library Management System.")
        return True

    def do_exit(self, arg):
        """Exit the program."""
        return self.do_quit(arg)


if __name__ == "__main__":
    LibraryCLI().cmdloop()
