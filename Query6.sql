

SELECT B.Name
FROM Borrower as B
JOIN BOOK_LOANS BL ON BL.Card_No = B.Card_No
WHERE BL.Returned_date = "NULL";