CREATE TRIGGER IF NOT EXISTS UpdateBookCopiesAfterLoan
AFTER INSERT ON BOOK_LOANS
BEGIN
    UPDATE BOOK_COPIES
    SET No_of_copies = No_of_copies - 1
    WHERE Book_Id = NEW.Book_ID AND Branch_Id = NEW.Branch_Id;
END;