
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL
        CHECK(length(trim(title)) BETWEEN 3 AND 80),
    subject TEXT NOT NULL,
    semester INTEGER NOT NULL
        CHECK(semester BETWEEN 1 AND 4),
    book_condition TEXT NOT NULL
        CHECK(book_condition IN ('New', 'Good', 'Fair')),
    mrp REAL NOT NULL CHECK(mrp > 0),
    selling_price REAL NOT NULL
        CHECK(selling_price > 0 AND selling_price <= mrp),
    seller_name TEXT NOT NULL,
    seller_mobile TEXT NOT NULL
        CHECK(
            length(seller_mobile) = 10
            AND seller_mobile NOT GLOB '*[^0-9]*'
        ),
    status TEXT NOT NULL DEFAULT 'Available'
        CHECK(status IN ('Available', 'Sold')),
    listed_on TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT OR IGNORE INTO books
(book_id, title, subject, semester, book_condition,
 mrp, selling_price, seller_name, seller_mobile, status)
VALUES
(1, 'Python Programming', 'Python', 1, 'Good',
 600, 400, 'Amit', '9876543210', 'Available'),

(2, 'Database Systems', 'DBMS', 2, 'New',
 800, 600, 'Priya', '9876543211', 'Available'),

(3, 'Web Development', 'Web Technology', 3, 'Fair',
 500, 250, 'Rahul', '9876543212', 'Sold'),

(4, 'Operating Systems', 'OS', 3, 'Good',
 700, 450, 'Sneha', '9876543213', 'Available'),

(5, 'Computer Networks', 'Networking', 4, 'Good',
 650, 400, 'Karan', '9876543214', 'Sold');
