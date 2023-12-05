
CREATE TABLE IF NOT EXISTS BOOK(
	Book_Id integer PRIMARY KEY,
    Title TEXT NOT NULL,
    Publisher_name TEXT NOT NULL,
    FOREIGN KEY(Publisher_name) REFERENCES PUBLISHER(Publisher_name)
);

CREATE TABLE IF NOT EXISTS PUBLISHER(
	Publisher_name TEXT PRIMARY KEY,
    Phone TEXT NOT NULL,
    Address TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS LIBRARY_BRANCH(
	Branch_Id integer PRIMARY KEY,
    Branch_Name TEXT NOT NULL,
    Branch_Address TEXT NOT NULL

);
CREATE TABLE IF NOT EXISTS BORROWER(
	Card_No integer PRIMARY KEY,
    Name TEXT NOT NULL,
    Address TEXT NOT NULL,
    Phone TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS BOOK_AUTHORS(
	Book_id INT NOT NULL,
    Author_name TEXT NOT NULL,
    
    FOREIGN KEY (Book_id) REFERENCES BOOK(Book_Id)
);

CREATE TABLE IF NOT EXISTS BOOK_LOANS(
	Book_ID INT NOT NULL,
    Branch_Id INT NOT NULL,
    Card_No INT NOT NULL,
    Date_Out TEXT NOT NULL,
    Due_Date TEXT NOT NULL,
    Returned_date TEXT,
    
    FOREIGN KEY(Book_Id) REFERENCES BOOK(Book_Id),
    FOREIGN KEY(Branch_Id) REFERENCES LIBRARY_BRANCH(Branch_Id),
    FOREIGN KEY(Card_No) REFERENCES BORROWER(Card_No)
);

CREATE TABLE IF NOT EXISTS BOOK_COPIES(
	Book_Id INT NOT NULL,
    Branch_Id INT NOT NULL,
    No_of_copies INT NOT NULL,

    FOREIGN KEY(Book_Id) REFERENCES BOOK(Book_Id),
    FOREIGN KEY(Branch_Id) REFERENCES LIBRARY_BRANCH(Branch_Id)
);
