import streamlit as st
import sqlite3
import pandas as pd

# Add a style block to the head section of the page
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Call the function to load the CSS file
local_css("style.css")
# Connect to the SQLite database
conn = sqlite3.connect('libraryManagementSystem.db')
c = conn.cursor()

# Create a books table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS books
             (book_id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT, author TEXT, isbn TEXT, status TEXT)''')
conn.commit()

import streamlit as st

def issue_book_form():
    st.header("Issue Book")
    # book_title = st.text_input("Book Title:")
    # borrower_name = st.text_input("Borrower Name:")
    
    book_options = [row[0] for row in c.execute("SELECT title FROM books WHERE status = 'Available'")]
    book_title = st.selectbox("Book Title:", book_options)

    borrower_options = [row[0] for row in c.execute("SELECT name FROM borrowers")]
    borrower_name = st.selectbox("Borrower Name:", borrower_options)

    
    issue_date = st.date_input("Issue Date:")
    due_date = st.date_input("Due Date:")
    submit_button = st.button("Issue Book")

    if submit_button:
        issue_book(book_title, borrower_name, issue_date, due_date)
        st.success(f"{book_title} has been issued to {borrower_name} until {due_date}.")

def issue_book(book_title, borrower_name, issue_date, due_date):
    c.execute("SELECT * FROM books where title = ?",(book_title,))
    book = c.fetchall()
    c.execute("UPDATE books SET status = 'issued' WHERE title = ?", (book_title,))
    c.execute('''CREATE TABLE IF NOT EXISTS BookIssueTable (id INTEGER PRIMARY KEY AUTOINCREMENT, book_id INTEGER, borrower_name TEXT, issue_date TEXT, due_date TEXT)''')
    c.execute("INSERT INTO BookIssueTable (id, book_id, borrower_name, issue_date, due_date) VALUES (NULL,?, ?, ?, ?)",
                   (book[0][0], borrower_name, issue_date, due_date))
    conn.commit()
    conn.close()
    

def borrower_registration():
    st.header("Borrower Registration")
    name = st.text_input("Name:")
    email = st.text_input("Email:")
    address = st.text_input("Address:")
    submit_button = st.button("Submit")

    if submit_button:
        register_borrower(name, email, address)
        st.success("Borrower registered successfully.")

def register_borrower(name, email, address):
    c.execute('''CREATE TABLE IF NOT EXISTS borrowers
                 (id INTEGER PRIMARY KEY, name TEXT, email TEXT, address TEXT)''')
    c.execute("INSERT INTO borrowers (id, name, email, address)VALUES (NULL, ?, ?, ?)", (name, email, address))
    conn.commit()
    conn.close()

def view_borrowers():
    # borrowers_df = pd.read_sql_query("SELECT * FROM borrowers", conn)
    # conn.close()
    # st.table(borrowers_df)
    c.execute('SELECT * FROM borrowers')
    borrowers = c.fetchall()
    if not borrowers:
        st.write("No borrower found.")
    else:
        bborrowers_table = [[borrower[0], borrower[1], borrower[2],borrower[3]] for borrower in borrowers]
        # headers = ["Name", "Email", "Address"]
        borrowers_df = pd.DataFrame(bborrowers_table)
        # , columns=headers)
        st.write(borrowers_df.to_html(escape=False), unsafe_allow_html=True)

# Define a class to represent a book
class Book:
    def __init__(self, title, author, isbn, status):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status=status

# Define a function to add a book to the database
def add_book(title, author, isbn, status):
    book = Book(title, author, isbn, status)
    c.execute("INSERT INTO books VALUES (NULL, ?, ?, ?, ?)", (book.title, book.author, book.isbn, book.status))
    conn.commit()



# Create a function to search for books
def search_books(query):
    c.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?", ('%'+query+'%', '%'+query+'%', '%'+query+'%'))
    books = c.fetchall()
    conn.close()
    return books

def delete_book(title):
    c.execute('DELETE FROM books WHERE title=?', (title,))
    conn.commit()
    st.success('Book deleted')

# Define a function to display the books in a table
def view_books():
    c.execute('SELECT * FROM books')
    books = c.fetchall()
    if not books:
        st.write("No books found.")
    else:
        book_table = [[book[0], book[1], book[2], book[3], book[4]] for book in books]
        headers = ["ID", "Title", "Author","ISBN","Status"]
        book_df = pd.DataFrame(book_table, columns=headers)
        st.write(book_df.to_html(escape=False), unsafe_allow_html=True)



# Define a function to retrieve all books from the database
def get_all_books():
    c.execute("SELECT * FROM books")
    books = c.fetchall()
    return books

# Define a function to search for books by title or author
def search_books(search_term):
    c.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", ('%' + search_term + '%', '%' + search_term + '%'))
    matching_books = c.fetchall()
    return matching_books

def view_borrowers_with_book():
    c.execute('''SELECT BookIssueTable.id, books.title, BookIssueTable.borrower_name, BookIssueTable.issue_date, BookIssueTable.due_date 
              FROM BookIssueTable INNER JOIN books ON BookIssueTable.book_id = books.id''')
    data = c.fetchall()
    if data:
        st.write("List of All Borrowers:")
        df = pd.DataFrame(data, columns=["ID", "Book Title", "Borrower Name", "Issue Date", "Due Date"])
        st.table(df)
    else:
        st.warning("No borrowers found.")
# Define the Streamlit app
def main():
    st.title("Library Management System")

    menu = ["Add Book", "View Books", "Search Books",'Delete Book','Borrower Registration','View Borrowers','Issue Book']
    choice = st.sidebar.selectbox("Select an option", menu)

    if choice == "Add Book":
        st.subheader("Add a Book")
        title = st.text_input("Enter the book title")
        author = st.text_input("Enter the author")
        isbn = st.text_input("Enter the ISBN")
        status="Available"
        if st.button("Add"):
            add_book(title, author, isbn, status)
            st.success("Book added.")
    elif choice == "View Books":
        st.subheader("Book List")
        books = get_all_books()
        if not books:
            st.write("No books found.")
        else:
            book_table = [[book[0], book[1], book[2], book[3], book[4]] for book in books]
            headers = ["ID", "Title", "Author","ISBN","Status"]
            book_df = pd.DataFrame(book_table, columns=headers)
            st.write(book_df.to_html(escape=False), unsafe_allow_html=True)

            # book_table = [[book[0], book[1], book[2]] for book in books]
            # headers = ["Title", "Author", "ISBN"]
            # st.table(pd.DataFrame(book_table, columns=headers).style.set_properties(**{'text-align': 'center', 'font-size': '14px', 'border': '1px solid black'}))

    elif choice == "Search Books":
        st.subheader("Search Books")
        
        query = st.text_input("Enter a search query")
        serach_button=st.button("Search")
        if query:
            if serach_button:
                books = search_books(query)
                if not books:
                    st.write("No books found.")
                else:
                    book_table = [[book[0], book[1], book[2], book[3], book[4]] for book in books]
                    headers = ["ID", "Title", "Author","ISBN","Status"]
                    book_df = pd.DataFrame(book_table, columns=headers)
                    st.write(book_df.to_html(escape=False), unsafe_allow_html=True)

                    # book_table = [[book[0], book[1], book[2]] for book in books]
                    # headers = ["Title", "Author", "ISBN"]
                    # st.table(pd.DataFrame(book_table, columns=headers).style.set_properties(**{'text-align': 'center', 'font-size': '14px', 'border': '1px solid black'}))
    
    elif choice == 'Delete Book':
        st.header("Delete Book")
        title = st.text_input("Enter the title of the book to delete:")
        delete_button = st.button("Delete")
        st.subheader("Book List")
        view_books()

        if title:
            if delete_button:
                delete_book(title)
                st.success(f"{title} has been deleted from the library.")
            else:
                st.warning(f"{title} not found in the library.")        
    elif choice == "Borrower Registration":
        borrower_registration()
    elif choice == "View Borrowers":
        view_borrowers_with_book()
        # view_borrowers()
    elif choice == "Issue Book":
        issue_book_form()
    
if __name__ == "__main__":
    main()
