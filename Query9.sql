

SELECT BR.Name,B.Title, BA.Author_Name, 
(julianday(BL.Returned_date)-julianday(BL.Date_Out)) as DaysBorrowed,
(CASE WHEN BL.Returned_date>Bl.Due_Date THEN "Returned Late" ELSE "Returned On Time" END) as ReturnStatus
FROM BORROWER as BR
JOIN BOOK_LOANS BL ON BL.Card_No = BR.Card_No
JOIN BOOK B ON B.Book_Id = BL.Book_ID
JOIN BOOK_AUTHORS BA ON BA.Book_Id = BL.Book_ID
WHERE BR.Name = "Ethan Martinez"
ORDER BY BL.date_out;
