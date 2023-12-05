UPDATE BOOK_COPIES
SET No_Of_Copies = No_Of_Copies +1
WHERE Branch_ID IN(
		SELECT Branch_Id
        FROM LIBRARY_BRANCH
        WHERE Branch_Name = "East Branch"
	);