CREATE VIEW vBookLoanInfo AS
SELECT 
    bl.Card_No,
    br.Name AS BorrowerName,
    bl.Date_Out,
    bl.Due_Date,
    bl.Returned_date,
    (JULIANDAY(bl.Due_Date) - JULIANDAY(bl.Date_Out)) AS TotalDays,
    b.Title AS BookTitle,
    CASE 
        WHEN bl.Returned_date IS NULL OR bl.Returned_date <= bl.Due_Date THEN 0 
        ELSE JULIANDAY(bl.Returned_date) - JULIANDAY(bl.Due_Date) 
    END AS DaysReturnedLate,
    bl.Branch_Id
FROM 
    BOOK_LOANS bl
JOIN 
    BORROWER br ON bl.Card_No = br.Card_No
JOIN 
    BOOK b ON bl.Book_ID = b.Book_Id
JOIN 
    LIBRARY_BRANCH lb ON bl.Branch_Id = lb.Branch_Id;
