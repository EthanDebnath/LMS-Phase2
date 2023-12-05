UPDATE BOOK_LOANS
SET Late = CASE
    WHEN Returned_Date > Due_Date THEN 1
    ELSE 0
END;