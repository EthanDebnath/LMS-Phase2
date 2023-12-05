

SELECT B.Title, MAX(julianday(BL.Returned_date)-julianday(BL.Date_Out)) as MaximumDaysBorrowed
FROM BOOK as B
JOIN BOOK_LOANS BL ON BL.Book_ID = B.Book_Id
WHERE BL.Returned_date <> "NULL" 
GROUP BY Title
ORDER BY MaximumDaysBorrowed DESC;