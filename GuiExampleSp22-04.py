import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox

# Initialize the main window
root = tk.Tk()
root.title('Ethan and Turza LMS')
root.geometry("400x1000")

# Database connection function
def db_connect():
    return sqlite3.connect('EthanDb.db')


def list_borrowers_with_late_fee(search_term=''):
    conn = db_connect()
    cur = conn.cursor()

    sql_query = """
    SELECT 
        br.Card_No AS BorrowerID, 
        br.Name AS BorrowerName, 
        COALESCE('$' || CAST(ROUND(SUM(CASE 
            WHEN bl.Returned_date > bl.Due_Date THEN 
                (JULIANDAY(bl.Returned_date) - JULIANDAY(bl.Due_Date)) * lb.LateFee 
            ELSE 0 
        END), 2) AS TEXT), '$0.00') AS LateFeeBalance
    FROM 
        BORROWER br
    LEFT JOIN 
        BOOK_LOANS bl ON br.Card_No = bl.Card_No
    LEFT JOIN 
        LIBRARY_BRANCH lb ON bl.Branch_Id = lb.Branch_Id
    GROUP BY 
        br.Card_No
    HAVING 
        (? IS NULL OR ? = '') OR 
        (br.Card_No = ?) OR 
        (br.Name LIKE '%' || ? || '%')
    ORDER BY 
        LateFeeBalance DESC;
    """

    try:
        cur.execute(sql_query, (search_term, search_term, search_term, search_term))
        records = cur.fetchall()
        display_records_in_popup(records)
    except sqlite3.Error as e:
        messagebox.showerror("Error", str(e))
    finally:
        conn.close()

def display_records_in_popup(records):
    popup = tk.Toplevel(root)
    popup.title("Query Results")
    popup.geometry("600x400")

    text_widget = tk.Text(popup)
    text_widget.pack(expand=True, fill='both')

    scrollbar = tk.Scrollbar(popup, command=text_widget.yview)
    scrollbar.pack(side='right', fill='y')
    text_widget.config(yscrollcommand=scrollbar.set)

    for record in records:
        text_widget.insert(tk.END, f"Borrower ID: {record[0]}, Name: {record[1]}, Late Fee Balance: {record[2]}\n")

# Search field
search_label = tk.Label(root, text="Enter Borrower ID or Name:")
search_label.pack()

search_entry = tk.Entry(root)
search_entry.pack()

# Search button
search_button = tk.Button(root, text="Search", command=lambda: list_borrowers_with_late_fee(search_entry.get()))
search_button.pack()

#-----------------6b


def list_book_information(borrower_id='', book_id='', book_title=''):
    conn = db_connect()
    cur = conn.cursor()

    sql_query = """
    SELECT 
        b.Book_Id, 
        b.Title, 
        COALESCE('$' || CAST(ROUND((JULIANDAY(bl.Returned_date) - JULIANDAY(bl.Due_Date)) * lb.LateFee, 2) AS TEXT), 'Non-Applicable') AS LateFeeAmount
    FROM 
        BOOK b
    JOIN 
        BOOK_LOANS bl ON b.Book_Id = bl.Book_Id
    JOIN 
        BORROWER br ON bl.Card_No = br.Card_No
    JOIN 
        LIBRARY_BRANCH lb ON bl.Branch_Id = lb.Branch_Id
    WHERE 
        (br.Card_No = ? OR ? = '') AND
        (b.Book_Id = ? OR ? = '') AND
        (b.Title LIKE '%' || ? || '%' OR ? = '')
    ORDER BY 
        LateFeeAmount DESC;
    """

    try:
        cur.execute(sql_query, (borrower_id, borrower_id, book_id, book_id, book_title, book_title))
        records = cur.fetchall()
        display_records_in_popup(records)
    except sqlite3.Error as e:
        messagebox.showerror("Error", str(e))
    finally:
        conn.close()

def display_records_in_popup(records):
    popup = tk.Toplevel(root)
    popup.title("Book Information")
    popup.geometry("600x400")

    text_widget = tk.Text(popup)
    text_widget.pack(expand=True, fill='both')

    scrollbar = tk.Scrollbar(popup, command=text_widget.yview)
    scrollbar.pack(side='right', fill='y')
    text_widget.config(yscrollcommand=scrollbar.set)

    for record in records:
        text_widget.insert(tk.END, f"Book ID: {record[0]}, Title: {record[1]}, Late Fee: {record[2]}\n")

#-----------------6b

def add_new_book():
    conn = db_connect()
    cur = conn.cursor()

    title = title_entry.get()
    publisher_name = publisher_entry.get()
    author_name = author_entry.get()

    try:
        # Insert the new book (assumes Publisher already exists)
        cur.execute("INSERT INTO BOOK (Title, Publisher_name) VALUES (?, ?)",
                    (title, publisher_name))
        book_id = cur.lastrowid

        # Insert author information
        cur.execute("INSERT INTO BOOK_AUTHORS (Book_id, Author_name) VALUES (?, ?)",
                    (book_id, author_name))
        
        # Insert author information
        cur.execute("INSERT INTO BOOK_AUTHORS (Book_id, Author_name) VALUES (?, ?)",
                    (book_id, author_name))

        # Add copies to each branch (assuming 5 branches with IDs 1 to 5)
        for branch_id in range(1, 4):
            cur.execute("INSERT INTO BOOK_COPIES (Book_Id, Branch_Id, No_of_copies) VALUES (?, ?, ?)",
                        (book_id, branch_id, 5))

        conn.commit()
        messagebox.showinfo("Success", "Book added successfully to all branches")
    except sqlite3.Error as e:
        messagebox.showerror("Error", str(e))
    finally:
        conn.close()

borrower_id_label = tk.Label(root, text="Borrower ID:")
borrower_id_label.pack()
borrower_id_entry = tk.Entry(root)
borrower_id_entry.pack()

book_id_label = tk.Label(root, text="Book ID:")
book_id_label.pack()
book_id_entry = tk.Entry(root)
book_id_entry.pack()

book_title_label = tk.Label(root, text="Book Title:")
book_title_label.pack()
book_title_entry = tk.Entry(root)
book_title_entry.pack()

search_button = tk.Button(root, text="Search", command=lambda: list_book_information(borrower_id_entry.get(), book_id_entry.get(), book_title_entry.get()))
search_button.pack()

# Function to list the number of copies loaned out per branch for a given book title
def list_copies_loaned_out():
    conn = db_connect()
    cur = conn.cursor()

    book_title = book_title_entry.get()

    try:
        cur.execute("""
            SELECT lb.Branch_Id, lb.Branch_Name, COUNT(*) AS CopiesLoanedOut
            FROM BOOK_LOANS bl
            JOIN BOOK b ON bl.Book_ID = b.Book_Id
            JOIN LIBRARY_BRANCH lb ON bl.Branch_Id = lb.Branch_Id
            WHERE b.Title = ?
            GROUP BY lb.Branch_Id
        """, (book_title,))

        records = cur.fetchall()
        print(records)  # Print records for debugging
        display_records(records)  # Ensure this function is called
    except sqlite3.Error as e:
        messagebox.showerror("Error", str(e))
    finally:
        conn.close()




# Function to check out a book
def checkout_book():
    conn = db_connect()
    cur = conn.cursor()
    
    # Get input values from GUI
    book_id = book_id_entry.get()
    branch_id = branch_id_entry.get()
    card_no = card_no_entry.get()
    date_out = date_out_entry.get()
    due_date = due_date_entry.get()

    try:
        cur.execute("INSERT INTO BOOK_LOANS (Book_ID, Branch_Id, Card_No, Date_Out, Due_Date) VALUES (?, ?, ?, ?, ?)",
                    (book_id, branch_id, card_no, date_out, due_date))
        conn.commit()
        messagebox.showinfo("Success", "Book checked out successfully")
    except sqlite3.Error as e:
        messagebox.showerror("Error", str(e))
    finally:
        conn.close()


# Function to list late Book Loans within a due date range
def list_late_book_loans():
    conn = db_connect()
    cur = conn.cursor()

    start_due_date = start_due_date_entry.get()
    end_due_date = end_due_date_entry.get()

    try:
        cur.execute("""
            SELECT bl.Book_ID, bl.Branch_Id, bl.Card_No, bl.Due_Date, bl.Returned_date, 
                   JULIANDAY(bl.Returned_date) - JULIANDAY(bl.Due_Date) AS DaysLate
            FROM BOOK_LOANS bl
            WHERE bl.Due_Date BETWEEN ? AND ? AND bl.Returned_date > bl.Due_Date
        """, (start_due_date, end_due_date))

        records = cur.fetchall()
        display_records(records)
    except sqlite3.Error as e:
        messagebox.showerror("Error", str(e))
    finally:
        conn.close()




# Function to add a new borrower
def add_borrower():
    conn = db_connect()
    cur = conn.cursor()
    
    # Get input values from GUI
    name = name_entry.get()
    address = address_entry.get()
    phone = phone_entry.get()

    try:
        cur.execute("INSERT INTO BORROWER (Name, Address, Phone) VALUES (?, ?, ?)",
                    (name, address, phone))
        conn.commit()
        new_card_no = cur.execute("SELECT last_insert_rowid()").fetchone()[0]
        messagebox.showinfo("Success", f"Borrower added successfully. Card Number: {new_card_no}")
    except sqlite3.Error as e:
        messagebox.showerror("Error", str(e))
    finally:
        conn.close()



def display_records(records):
    for i in tree.get_children():
        tree.delete(i)
    for record in records:
        tree.insert("", tk.END, values=record)

# Create a Canvas
canvas = tk.Canvas(root)
canvas.pack(side='left', fill='both', expand=True)

# Create a Scrollbar and attach it to the Canvas
scrollbar = ttk.Scrollbar(root, command=canvas.yview)
scrollbar.pack(side='right', fill='y')

# Configure the Canvas
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

# Create a Frame inside the Canvas
frame = tk.Frame(canvas)
canvas.create_window((0,0), window=frame, anchor='nw')

# GUI Components inside the frame
add_book_heading = tk.Label(frame, text="Add a New Book", font=("Helvetica", 16, "bold"))
add_book_heading.pack(pady=10)


# Set up Treeview for displaying results
columns = ('BorrowerID', 'BorrowerName', 'LateFeeBalance')
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack(fill='both', expand=True)

# GUI Components for adding a new book
title_label = tk.Label(frame, text="Book Title:")
title_label.pack()
title_entry = tk.Entry(frame)
title_entry.pack()

publisher_label = tk.Label(frame, text="Publisher Name:")
publisher_label.pack()
publisher_entry = tk.Entry(frame)
publisher_entry.pack()

author_label = tk.Label(frame, text="Author Name:")
author_label.pack()
author_entry = tk.Entry(frame)
author_entry.pack()

add_book_btn = tk.Button(frame, text="Add New Book", command=add_new_book)
add_book_btn.pack(pady=15)


# GUI Components
book_title_label = tk.Label(frame, text="Enter Book Title:")
book_title_label.pack()
book_title_entry = tk.Entry(frame)
book_title_entry.pack()

list_copies_btn = tk.Button(frame, text="List Copies Loaned Out", command=list_copies_loaned_out)
list_copies_btn.pack()

# Setting up Treeview to display results
columns = ('Branch_Id', 'Branch_Name', 'CopiesLoanedOut')
tree = ttk.Treeview(frame, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack(fill='both', expand=True)


# GUI components for Book Checkout

add_book_heading = tk.Label(frame, text="Book Checkout", font=("Helvetica", 16, "bold"))
add_book_heading.pack(pady=10)

book_id_label = tk.Label(frame, text="Book ID:")
book_id_label.pack()
book_id_entry = tk.Entry(frame)
book_id_entry.pack()

branch_id_label = tk.Label(frame, text="Branch ID:")
branch_id_label.pack()
branch_id_entry = tk.Entry(frame)
branch_id_entry.pack()

card_no_label = tk.Label(frame, text="Card Number:")
card_no_label.pack()
card_no_entry = tk.Entry(frame)
card_no_entry.pack()

date_out_label = tk.Label(frame, text="Date Out (YYYY-MM-DD):")
date_out_label.pack()
date_out_entry = tk.Entry(frame)
date_out_entry.pack()

due_date_label = tk.Label(frame, text="Due Date (YYYY-MM-DD):")
due_date_label.pack()
due_date_entry = tk.Entry(frame)
due_date_entry.pack()

checkout_btn = tk.Button(frame, text="Checkout Book", command=checkout_book)
checkout_btn.pack(pady=15)





# GUI Components for Due Date Range Input
start_due_date_label = tk.Label(frame, text="Start Due Date (YYYY-MM-DD):")
start_due_date_label.pack()
start_due_date_entry = tk.Entry(frame)
start_due_date_entry.pack()

end_due_date_label = tk.Label(frame, text="End Due Date (YYYY-MM-DD):")
end_due_date_label.pack()
end_due_date_entry = tk.Entry(frame)
end_due_date_entry.pack()

list_late_loans_btn = tk.Button(frame, text="List Late Book Loans", command=list_late_book_loans)
list_late_loans_btn.pack()

# Setting up Treeview to display results
columns = ('Book_ID', 'Branch_Id', 'Card_No', 'Due_Date', 'Returned_Date', 'DaysLate')
tree = ttk.Treeview(frame, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack(fill='both', expand=True)



# GUI components for adding a borrower

add_book_heading = tk.Label(frame, text="New Borrower", font=("Helvetica", 16, "bold"))
add_book_heading.pack(pady=10)

name_label = tk.Label(frame, text="Name:")
name_label.pack()
name_entry = tk.Entry(frame)
name_entry.pack()

address_label = tk.Label(frame, text="Address:")
address_label.pack()
address_entry = tk.Entry(frame)
address_entry.pack()

phone_label = tk.Label(frame, text="Phone:")
phone_label.pack()
phone_entry = tk.Entry(frame)
phone_entry.pack()

add_borrower_btn = tk.Button(frame, text="Add Borrower", command=add_borrower)
add_borrower_btn.pack(pady=15)


# Main loop
root.mainloop()