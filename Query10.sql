
SELECT BR.Name, BR.Address
FROM BORROWER as BR
JOIN BOOK_LOANS BL ON BL.Card_No = BR.Card_No
JOIN LIBRARY_BRANCH LB ON LB.Branch_Id = BL.Branch_Id
WHERE LB.Branch_Name = "West Branch";