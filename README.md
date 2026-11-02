# Library Management System

A desktop-based Library Management System developed using Python and Tkinter. This application allows users to browse, search, borrow, and return books, while administrators can manage the library's book collection through a simple graphical user interface.

## Features

### User Features
- View all books in the library.
- Browse books that are currently available.
- Search for books by Book ID, title, author, or genre.
- Sort books by Book ID, title, author, publication year, or genre.
- Borrow available books and return borrowed books.

### Admin Features
- Access the Admin Menu through the admin login screen.
- The current admin login accepts any password, as password validation has not been implemented.
- Add new books to the library.
- Update existing book information.
- Delete books from the collection.
- View and manage all books.

### Data Management
- Stores book information in a CSV file.
- Automatically creates the CSV file with the required column headers if it does not exist.
- Maintains book availability status as either Available or Borrowed.
- Validates book IDs, publication years, and duplicate book IDs.

## Technologies Used

- Python
- Tkinter – graphical user interface
- CSV – data storage
- PyCharm – development environment

## Project Structure

```text
Library_management_demo/
├── Library Management.py
├── library.csv
└── README.md
```

## Requirements

- Python 3.10 or later
- Tkinter (usually included with Python)
- PyCharm or another Python IDE

No additional Python packages are required.

## How to Run

1. Clone or download this repository.
2. Open the project in PyCharm.
3. Ensure that `Library Management.py` and `library.csv` are in the same directory.
4. Run `Library Management.py`.

The application will open with a welcome screen where users can enter their first and last names before accessing the main menu.

## How to Use

1. Enter your first and last name on the welcome screen.
2. Choose User Menu to browse, search, borrow, or return books.
3. Choose Admin Menu to add, update, or delete books.
4. Use the search and sort options to find books easily.

## Data Storage

Book information is stored in `library.csv` using the following fields:

| Field | Description |
|---|---|
| BookID | Unique identifier for each book |
| Title | Book title |
| Author | Book author |
| Year | Publication year |
| Genre | Book category |
| Status | Availability status |

## Future Improvements

- Add secure administrator authentication.
- Introduce a database for more reliable data management.
- Add user accounts and borrowing history.
- Improve input validation and error handling.

## Author

Dhruba Chatterjee

