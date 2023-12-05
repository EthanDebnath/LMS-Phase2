
INSERT INTO BOOK(Title, Publisher_Name) VALUES("Harry Potter and the Sorcerer\'s Stone","Oxford Publisheing");
INSERT INTO BOOK_AUTHORS(Book_Id, Author_Name) VALUES ((SELECT Book_Id FROM BOOK WHERE Title = "Harry Potter and the Sorcerer\'s Stone"),
	"J.K. Rowling");