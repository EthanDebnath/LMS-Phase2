
SELECT B.Title, LB.Branch_Name,(STRFTIME('%Y%m%d', BL.Returned_date)-STRFTIME('%Y%m%d',BL.Date_Out )) as DaysBorrowed
FROM BOOK as B
JOIN BOOK_LOANS BL ON BL.Book_ID = B.Book_Id
JOIN LIBRARY_BRANCH LB on LB.Branch_Id = BL.Branch_Id
WHERE STRFTIME('%Y%m%d',BL.Date_Out) BETWEEN STRFTIME('%Y%m%d', date('2022-03-05')) 
AND STRFTIME('%Y%m%d', date('2022-03-23'));