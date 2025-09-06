
# Book Catalog

## Overview

Book Catalog is a desktop application for managing your personal book collection. It features a user-friendly GUI built with Tkinter and stores all data in a local SQLite database. You can add, edit, search, and rate books, as well as filter by read status.

## Features

- Add new books with title, author, location, read status, and rating
- Search books by keyword (title, author, location)
- Filter books by read status (All, Yes, No)
- Edit or delete existing books
- Sort books by any column in the results table
- Ratings from 1 to 10
- Persistent storage using SQLite

## Requirements

- Python 3.11 or newer
- Tkinter (included with standard Python)
- SQLite3 (included with standard Python)

## Setup

1. Clone or download this repository.
2. Ensure you have Python 3.11+ installed.
3. No additional dependencies are required.

## Usage

1. Open a terminal in the `Book_Catalog` directory.
1. Run the application:

     ```bash
     python Book_Catalog.py
     ```

1. The GUI will open. Use the menu to:
   - **Find Books**: Search and filter your catalog. Edit or delete books from the results table.
   - **Add Book**: Enter details for a new book and add it to your catalog.
   - **Exit**: Close the application.

### Adding a Book

1. Click "Add Book".
2. Fill in Title, Author, Location.
3. Optionally check "Read Before" and enter a rating (1-10).
4. Click "Add Book" to save.

### Finding and Editing Books

1. Click "Find Books".
2. Enter a keyword to search (matches title, author, or location).
3. Filter by read status if desired.
4. Click "Edit Selected" to modify or delete a book.

### Editing/Deleting a Book

1. In the edit screen, change any details and click "Save Changes".
2. To delete, click "Delete Book" and confirm.

## Database

- The database file is located at:
  `C:/Users/levig/OneDrive/Documents/Coding/book_database.db`
- All book data is stored in the `books` table.

## Troubleshooting

- If the app does not start, ensure Python 3.11+ is installed and run from the correct directory.
- If you get database errors, check that you have write permissions for the database file location.
- Ratings must be integers between 1 and 10; invalid ratings are ignored.
- Title, Author, and Location are required fields.

## Example

```text
Menu:
Book Catalog
1. Find Books
2. Add Book
3. Exit

Add Book:
Title: Dune
Author: Frank Herbert
Location: Shelf 2
Read Before: [x]
Rating: 9

Find Books:
Keyword: Dune
Filter by Read: Yes
Results:
| ID | Title | Author        | Location | ReadBefore | Rating |
|----|-------|--------------|----------|------------|--------|
| 1  | Dune  | Frank Herbert| Shelf 2  | Yes        | 9      |

Edit Book:
Change rating to 10, click Save Changes.
Delete book if desired.
```
