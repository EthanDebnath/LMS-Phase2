SELECT LB.Branch_Name, SUM(BL.Returned_Date = "NULL") as StillBorrowed, SUM(BL.Returned_Date<>"NULL") as BookReturned, 
SUM(BL.Returned_date>BL.Due_Date) as ReturnedLate
FROM LIBRARY_BRANCH as LB
JOIN BOOK_LOANS BL ON BL.Branch_Id = LB.Branch_Id
GROUP BY LB.Branch_Name;
