# Library Management System

A simple command-line library management system that allows librarians to manage books and patrons.

## Features

- Add and manage books in the library collection
- Register and manage library patrons
- Check out books to patrons
- Return books to the library
- Search for books by title, author, or ISBN
- Track overdue books and calculate late fees

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Docker (optional, for containerized deployment)

### Installation

#### Local Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/library_project_ai.git
   cd library_project_ai
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python library_cli.py
   ```

#### Docker Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/library_project_ai.git
   cd library_project_ai
   ```

2. (Optional) Test the Docker setup:
   ```
   ./test_docker.sh
   ```
   This script will build a test image and verify that the application can run in Docker.

3. Build and run using Docker Compose:
   ```
   docker-compose up -d
   ```

4. Attach to the running container to use the CLI:
   ```
   docker attach library-management-system
   ```

   Note: To detach from the container without stopping it, press `Ctrl+P` followed by `Ctrl+Q`.

5. Alternatively, run the container directly:
   ```
   docker build -t library-system .
   docker run -it --name library-management-system library-system
   ```

## Usage

Once the application is running, you can use the following commands:

- `add_book title|author|isbn|publication_year` - Add a new book
- `add_patron name|id` - Register a new patron
- `checkout isbn|patron_id` - Check out a book to a patron
- `return isbn` - Return a book to the library
- `list_books` - List all books in the library
- `search query` - Search for books by title, author, or ISBN
- `overdue` - List all overdue books
- `help` - Show available commands
- `quit` or `exit` - Exit the program

## Running Tests

To run the tests:

```
pytest test_library.py
```

With Docker:

```
docker-compose run library pytest test_library.py
```

## Data Persistence

When running with Docker, a volume is mounted at `./data:/app/data` for data persistence. Currently, the application uses in-memory storage, but this volume is prepared for future implementation of file-based or database storage.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
