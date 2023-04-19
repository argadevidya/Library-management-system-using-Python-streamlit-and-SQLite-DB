# Library-management-system-using-Python-streamlit-and-SQLite-DB
The Library Management System project is a web application that allows librarians to manage their library's resources.
This is a web-based Library Management System built with Streamlit and SQLite. It allows librarians to keep track of books, borrowers, and book borrowing activities.

# Features
  ## Add Book
Librarians can add new books to the library. They need to provide the book's title, author, publisher, and genre. The system will automatically assign an ID to the book.

  ## View Books
Librarians can view all the books in the library in a table format. The table will display the book's ID, title, author, publisher, genre, and status (available/issued).

## Delete Book
Librarians can delete a book from the library. They need to provide the book's title, and the system will delete the book from the database. If the book is currently issued, the librarian needs to mark it as returned before deleting it.

## Add Borrower
Librarians can add new borrowers to the library. They need to provide the borrower's name, address, email, and phone number. The system will automatically assign an ID to the borrower.
 
## View Borrowers
Librarians can view all the borrowers in the library in a table format. The table will display the borrower's ID, name, address, email, and phone number.

## Issue Book
Librarians can issue a book to a borrower. They need to provide the book's title, the borrower's name, the issue date, and the due date. The system will mark the book as issued and create an entry in the BookIssueTable with the book ID, borrower ID, issue date, and due date.

## Return Book
Librarians can mark a book as returned. They need to provide the book's title, and the system will mark the book as available and update the BookIssueTable with the return date.

## View Issued Books
Librarians can view all the books that are currently issued in a table format. The table will display the book's ID, title, author, borrower name, issue date, and due date.

# How to run the project
*    Clone the repository
*   Install the required dependencies using pip install -r requirements.txt
*    Run streamlit run app.py to launch the web app

# Technologies Used
Streamlit - for building the web app
SQLite - for storing the data

# Conclusion
This Library Management System provides a user-friendly interface for librarians to manage books, borrowers, and book borrowing activities. It can be easily customized to add new features and functionality.
