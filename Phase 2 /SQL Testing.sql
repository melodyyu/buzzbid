---------------------------------------------
--               SQL Testing               --
---------------------------------------------

--Drop enums
DROP TYPE IF EXISTS user_type_enum CASCADE;
DROP TYPE IF EXISTS condition_enum CASCADE;
DROP TYPE IF EXISTS auction_length_enum CASCADE;

--Drop existing tables
DROP TABLE IF EXISTS "user" CASCADE;
DROP TABLE IF EXISTS "adminuser" CASCADE;
DROP TABLE IF EXISTS "item" CASCADE;
DROP TABLE IF EXISTS "rating" CASCADE;
DROP TABLE IF EXISTS "bid" CASCADE;
DROP TABLE IF EXISTS "category" CASCADE;

--------------------------------------------------------------------
--        User Type, Item Condition, Auction Length enums         --
--------------------------------------------------------------------

CREATE TYPE user_type_enum AS ENUM ('Regular', 'Admin');
CREATE TYPE condition_enum AS ENUM ('New', 'Very Good', 'Good', 'Fair', 'Poor');
CREATE TYPE auction_length_enum AS ENUM ('1','3','5','7');

--------------------------------------------------------------------
--                       Create table schema                      --
--------------------------------------------------------------------
--Creating tables
CREATE TABLE "category" (
    category_name VARCHAR(50) NOT NULL,
    PRIMARY KEY (category_name)
);

CREATE TABLE "user" (
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    user_type user_type_enum NOT NULL,
    PRIMARY KEY (username)
);

CREATE TABLE "adminuser" (
    username VARCHAR(50) NOT NULL,
    position VARCHAR(50) NOT NULL,
    PRIMARY KEY (username),
    FOREIGN KEY (username) REFERENCES "user" (username) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE "item" (
    username VARCHAR(50) NOT NULL,
    item_id SERIAL,
    name VARCHAR(250) NOT NULL,
    condition condition_enum NOT NULL,
    category_name VARCHAR(50) NOT NULL,
    description VARCHAR(5000) NOT NULL,
    starting_bid DECIMAL(10,2) NOT NULL,
    min_sale_price DECIMAL(10,2) NOT NULL,
    get_it_now_price DECIMAL(10,2) NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE NOT NULL,
    is_returnable BOOLEAN NOT NULL,
    cancellation_reason VARCHAR(250),
    PRIMARY KEY (item_id),
    FOREIGN KEY (username) REFERENCES "user" (username) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (category_name) REFERENCES "category" (category_name) ON DELETE CASCADE ON UPDATE CASCADE,
    CHECK (get_it_now_price > starting_bid AND get_it_now_price > min_sale_price AND starting_bid <= min_sale_price),
    CHECK (starting_bid > 0),
    CHECK (min_sale_price > 0),
    CHECK (get_it_now_price > 0 OR get_it_now_price IS NULL)
);

CREATE TABLE "rating" (
    item_id INT NOT NULL,
    comments VARCHAR(5000),
    number_of_stars INT NOT NULL CHECK (number_of_stars IN (1, 2, 3, 4, 5)),
    date_and_time TIMESTAMP WITH TIME ZONE NOT NULL,
    PRIMARY KEY (item_id),
    FOREIGN KEY (item_id) REFERENCES "item" (item_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE "bid" (
    username VARCHAR(50) NOT NULL,
    item_id INT NOT NULL,
    bid_time TIMESTAMP WITH TIME ZONE NOT NULL,
    bid_amount decimal(10, 2) NOT NULL,
    PRIMARY KEY (username, item_id, bid_time),
    FOREIGN KEY (username) REFERENCES "user" (username) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (item_id) REFERENCES "item" (item_id) ON DELETE CASCADE ON UPDATE CASCADE
);


--Populate categories
INSERT INTO "category" (category_name) VALUES ('Arts');
INSERT INTO "category" (category_name) VALUES ('Books');
INSERT INTO "category" (category_name) VALUES ('Electronics');
INSERT INTO "category" (category_name) VALUES ('Cookies');


--Populating tables 

--User table
INSERT INTO "user" (username, password, first_name, last_name, user_type) VALUES ('JSmith', '12345', 'John', 'Smith', 'Regular');
INSERT INTO "user" (username, password, first_name, last_name, user_type) VALUES ('LMark', '12345', 'Leo', 'Mark', 'Regular');
INSERT INTO "user" (username, password, first_name, last_name, user_type) VALUES ('CHoarse', '12345', 'Charlie', 'Hoarse', 'Regular');
INSERT INTO "user" (username, password, first_name, last_name, user_type) VALUES ('EHouse', '12345', 'Eddie', 'House', 'Regular');
INSERT INTO "user" (username, password, first_name, last_name, user_type) VALUES ('NJerger', '12345', 'Natalie', 'Jerger', 'Regular');
INSERT INTO "user" (username, password, first_name, last_name, user_type) VALUES ('BLiang', '12345', 'Ben', 'Liang', 'Regular');
INSERT INTO "user" (username, password, first_name, last_name, user_type) VALUES ('PlayStationSeller', 'PS12345', 'Stock', 'Flipper', 'Regular');
INSERT INTO "user" (username, password, first_name, last_name, user_type) VALUES ('GBurdell', '54321', 'George', 'Burdell', 'Admin');

--Admin table
INSERT INTO "adminuser" (username, position) VALUES ('GBurdell', 'GT Admin');
--INSERT INTO "adminuser" (username, position) VALUES ('AdminTest', 'TestAdmin'); --This should throw an error if uncommented, foreign key violation

INSERT INTO "item" (username, name, condition, category_name, description, starting_bid, min_sale_price, get_it_now_price, end_time, is_returnable, cancellation_reason) 
--VALUES ('PlayStationSeller', 'PS5', 'test', 'Electronics', 'New playstation 5', 100, 100, 500, (CURRENT_TIMESTAMP AT TIME ZONE 'EDT') + INTERVAL '3 day', FALSE, NULL); --This should throw an error if uncommented, condition enum violation
--VALUES ('PlayStationSeller', 'PS5', 'New', 'test', 'New playstation 5', 100, 100, 500, (CURRENT_TIMESTAMP AT TIME ZONE 'EDT') + INTERVAL '3 day', FALSE, NULL); --This should throw an error if uncommented, category enum violation
--VALUES ('PlayStationSeller', 'PS5', 'New', 'Electronics', 'New playstation 5', 100, 100, 1, (CURRENT_TIMESTAMP AT TIME ZONE 'EDT') + INTERVAL '3 day', FALSE, NULL); --This should fail the constraint check where get_it_now_price > starting_bid
--VALUES ('PlayStationSeller', 'PS5', 'New', 'Electronics', 'New playstation 5', 0, 100, 1, (CURRENT_TIMESTAMP AT TIME ZONE 'EDT') + INTERVAL '3 day', FALSE, NULL); --This should fail the constraint check, starting_bid > 0
--VALUES ('PlayStationSeller', 'PS5', 'New', 'Electronics', 'New playstation 5', 100, 0, 1, (CURRENT_TIMESTAMP AT TIME ZONE 'EDT') + INTERVAL '3 day', FALSE, NULL); --This should fail the constraint check, min_sale_price > 0
--VALUES ('PlayStationSeller', 'PS5', 'New', 'Electronics', 'New playstation 5', 0, 100, 0, (CURRENT_TIMESTAMP AT TIME ZONE 'EDT') + INTERVAL '3 day', FALSE, NULL); --This should fail the constraint check, get_it_now_price > 0 or get_it_now_price == NULL
VALUES ('PlayStationSeller', 'PS5', 'New', 'Electronics', 'New playstation 5', 100, 100, 500, (CURRENT_TIMESTAMP AT TIME ZONE 'EDT') + INTERVAL '3 day', FALSE, NULL);
INSERT INTO "item" (username, name, condition, category_name, description, starting_bid, min_sale_price, get_it_now_price, end_time, is_returnable, cancellation_reason) 
VALUES ('PlayStationSeller', 'PS4', 'New', 'Electronics', 'New playstation 4', 100, 100, 400, (CURRENT_TIMESTAMP AT TIME ZONE 'EDT') + INTERVAL '3 day', FALSE, NULL);
INSERT INTO "item" (username, name, condition, category_name, description, starting_bid, min_sale_price, get_it_now_price, end_time, is_returnable, cancellation_reason) 
VALUES ('PlayStationSeller', 'PS3', 'New', 'Electronics', 'New playstation 3', 100, 100, 300, (CURRENT_TIMESTAMP AT TIME ZONE 'EDT') + INTERVAL '3 day', FALSE, NULL);
INSERT INTO "item" (username, name, condition, category_name, description, starting_bid, min_sale_price, get_it_now_price, end_time, is_returnable, cancellation_reason) 
VALUES ('PlayStationSeller', 'PS2', 'New', 'Electronics', 'New playstation 2', 100, 100, 200, (CURRENT_TIMESTAMP AT TIME ZONE 'EDT') + INTERVAL '3 day', FALSE, NULL);
INSERT INTO "item" (username, name, condition, category_name, description, starting_bid, min_sale_price, get_it_now_price, end_time, is_returnable, cancellation_reason) 
VALUES ('PlayStationSeller', 'PS1', 'New', 'Electronics', 'New playstation 1', 10, 10, 100, (CURRENT_TIMESTAMP AT TIME ZONE 'EDT') + INTERVAL '3 day', FALSE, NULL);

--added more values for search item testing; itemID 9-16
INSERT INTO "item" (username, name, condition, category_name, description, starting_bid, min_sale_price, get_it_now_price, end_time, is_returnable, cancellation_reason) 
VALUES ('cookieguy', 'ChocolateChip', 'Very Good', 'Cookies', 'best cookie, most standard, terrible for dogs', 10, 10, 100, (CURRENT_TIMESTAMP AT TIME ZONE 'EDT') + INTERVAL '3 day', FALSE, NULL);
INSERT INTO "item" (username, name, condition, category_name, description, starting_bid, min_sale_price, get_it_now_price, end_time, is_returnable, cancellation_reason) 
VALUES ('cookieguy', 'RedVelvet', 'Good', 'Cookies', 'fake chocolate chip', 10, 10, 100, (CURRENT_TIMESTAMP AT TIME ZONE 'EDT') + INTERVAL '3 day', FALSE, NULL);
INSERT INTO "item" (username, name, condition, category_name, description, starting_bid, min_sale_price, get_it_now_price, end_time, is_returnable, cancellation_reason) 
VALUES ('cookieguy', 'Matcha', 'Fair', 'Cookies', 'not as grassy as people think', 10, 10, 100, (CURRENT_TIMESTAMP AT TIME ZONE 'EDT') + INTERVAL '3 day', FALSE, NULL);
INSERT INTO "item" (username, name, condition, category_name, description, starting_bid, min_sale_price, get_it_now_price, end_time, is_returnable, cancellation_reason) 
VALUES ('cookieguy', 'Fudge', 'Poor', 'Cookies', 'might od on sugar but worth', 10, 10, 100, (CURRENT_TIMESTAMP AT TIME ZONE 'EDT') + INTERVAL '3 day', FALSE, NULL); 
INSERT INTO "item" (username, name, condition, category_name, description, starting_bid, min_sale_price, get_it_now_price, end_time, is_returnable, cancellation_reason) 
VALUES ('cookieguy', 'Snickerdoodle', 'Fair', 'Cookies', 'mid-cookie but fun to roll in sugar', 10, 10, 110, (CURRENT_TIMESTAMP AT TIME ZONE 'EDT') + INTERVAL '7 day', FALSE, NULL);
UPDATE item SET end_time='2024-03-13 10:20:09.508188-07' WHERE name='Macaron';
INSERT INTO "item" (username, name, condition, category_name, description, starting_bid, min_sale_price, get_it_now_price, end_time, is_returnable, cancellation_reason) 
VALUES ('cookieguy', 'biscotti', 'Very Good', 'Cookies', 'i emerged during the dark ages', 1, 20, 40, (CURRENT_TIMESTAMP AT TIME ZONE 'EDT') + INTERVAL '1 day', FALSE, NULL);

UPDATE item SET end_time='2024-03-13 10:20:09.508188-07' WHERE name='biscotti';


INSERT INTO "rating" (item_id, comments, number_of_stars, date_and_time) VALUES (1, 'Excellent product, fast shipping', 5, CURRENT_TIMESTAMP AT TIME ZONE 'EDT');
INSERT INTO "bid" (username, item_id, bid_time, bid_amount) VALUES ('JSmith', 1, CURRENT_TIMESTAMP AT TIME ZONE 'EDT', 101.00);
INSERT INTO "bid" (username, item_id, bid_time, bid_amount) VALUES ('LMark', 1, CURRENT_TIMESTAMP AT TIME ZONE 'EDT', 102.00);
INSERT INTO "bid" (username, item_id, bid_time, bid_amount) VALUES ('CHoarse', 1, CURRENT_TIMESTAMP AT TIME ZONE 'EDT', 103.00);
INSERT INTO "bid" (username, item_id, bid_time, bid_amount) VALUES ('EHouse', 1, CURRENT_TIMESTAMP AT TIME ZONE 'EDT', 104.00);
INSERT INTO "bid" (username, item_id, bid_time, bid_amount) VALUES ('NJerger', 1, CURRENT_TIMESTAMP AT TIME ZONE 'EDT', 105.00);
INSERT INTO "bid" (username, item_id, bid_time, bid_amount) VALUES ('GBurdell', 1, CURRENT_TIMESTAMP AT TIME ZONE 'EDT', 0);

SELECT
  CASE
	WHEN bid_amount = 0 THEN 'Cancelled'
	ELSE bid_amount::text
  END AS "Bid Amount",
  bid_time AS "Time of Bid",
  username AS "Username"
FROM bid
WHERE item_id = 1
ORDER BY bid_time DESC;


--added more values for search-item testing
INSERT INTO "bid" (username, item_id, bid_time, bid_amount) VALUES ('JSmith', 9, CURRENT_TIMESTAMP AT TIME ZONE 'EDT', 110.00);
INSERT INTO "bid" (username, item_id, bid_time, bid_amount) VALUES ('LMark', 9, CURRENT_TIMESTAMP AT TIME ZONE 'EDT', 120.00);
INSERT INTO "bid" (username, item_id, bid_time, bid_amount) VALUES ('JSmith', 9, CURRENT_TIMESTAMP AT TIME ZONE 'EDT', 130.00);
INSERT INTO "bid" (username, item_id, bid_time, bid_amount) VALUES ('LMark', 9, CURRENT_TIMESTAMP AT TIME ZONE 'EDT', 140.00);
INSERT INTO "bid" (username, item_id, bid_time, bid_amount) VALUES ('JSmith', 9, CURRENT_TIMESTAMP AT TIME ZONE 'EDT', 150.00);
INSERT INTO "bid" (username, item_id, bid_time, bid_amount) VALUES ('LMark', 9, CURRENT_TIMESTAMP AT TIME ZONE 'EDT', 160.00);
INSERT INTO "bid" (username, item_id, bid_time, bid_amount) VALUES ('BLiang', 9, CURRENT_TIMESTAMP AT TIME ZONE 'EDT', 170.00);

INSERT INTO "bid" (username, item_id, bid_time, bid_amount) VALUES ('LMark', 10, CURRENT_TIMESTAMP AT TIME ZONE 'EDT', 110.00);

INSERT INTO "bid" (username, item_id, bid_time, bid_amount) VALUES ('PlayStationSeller', 16, CURRENT_TIMESTAMP AT TIME ZONE 'EDT', 2.00);
INSERT INTO "bid" (username, item_id, bid_time, bid_amount) VALUES ('LMark', 16, CURRENT_TIMESTAMP AT TIME ZONE 'EDT', 4.00);
INSERT INTO "bid" (username, item_id, bid_time, bid_amount) VALUES ('PlayStationSeller', 16, CURRENT_TIMESTAMP AT TIME ZONE 'EDT', 5.00);
INSERT INTO "bid" (username, item_id, bid_time, bid_amount) VALUES ('LMark', 16, CURRENT_TIMESTAMP AT TIME ZONE 'EDT', 9.00);

INSERT INTO "bid" (username, item_id, bid_time, bid_amount) VALUES ('PlayStationSeller', 16, CURRENT_TIMESTAMP AT TIME ZONE 'EDT', 45.00);
UPDATE "bid" SET bid_time=(CURRENT_TIMESTAMP AT TIME ZONE 'EDT') - INTERVAL '1 day' WHERE username='LMark' AND bid_amount=45.00;







--Sample table print statements
--select * from "user";
--select * from "adminuser";
--select * from "item";
--select * from "rating";
--select * from "bid";

--Printing enum contents
--SELECT enumlabel AS "User Types" FROM pg_enum JOIN pg_type ON pg_enum.enumtypid = pg_type.oid WHERE pg_type.typname = 'user_typeenum';
--SELECT enumlabel AS "Conditions" FROM pg_enum JOIN pg_type ON pg_enum.enumtypid = pg_type.oid WHERE pg_type.typname = 'conditionenum';
--SELECT enumlabel AS "Auction Length" FROM pg_enum JOIN pg_type ON pg_enum.enumtypid = pg_type.oid WHERE pg_type.typname = 'auctionlengthenum';

--1.1 Log In, $username = GBurdell
--SELECT password FROM "user" WHERE username = 'GBurdell';

--1.2 Register, $username = testuser, $password = testpassword, $first_name = test, $last_name = user
/*
INSERT INTO "user" (username, password, first_name, last_name, user_type) 
SELECT 'testuser', 'testpassword', 'test', 'user', 'Regular'
WHERE NOT EXISTS (SELECT username FROM "user" WHERE username = 'testuser');

INSERT INTO "user" (username, password, first_name, last_name, user_type) 
SELECT 'testuser', 'testpassword', 'test', 'user', 'Regular'
WHERE NOT EXISTS (SELECT username FROM "user" WHERE username = 'testuser'); --This query is a duplicate of the above. It should not go through

INSERT INTO "user" (username, password, first_name, last_name, user_type) 
SELECT 'testuser2', 'testpassword', 'test', 'user', 'Regular'
WHERE NOT EXISTS (SELECT username FROM "user" WHERE username = 'testuser2'); --This query should show up in the final result

select * from "user";
*/

--1.3 View Main Menu $username = GBurdell
--SELECT user_type, first_name, last_name FROM "user" WHERE username = 'GBurdell'; 

--1.4 List Item
--Select all categories sorted in alphabetical order
--SELECT * FROM "category" ORDER BY category_name ASC;

--Select all conditions sorted in enumerical order
/*
SELECT enumlabel AS item_condition
FROM pg_enum
JOIN pg_type ON pg_enum.enumtypid = pg_type.oid
WHERE pg_type.typname = 'conditionenum'
ORDER BY pg_enum.enumsortorder;
*/

--Select all auction length enums sorted in enumerical order
/*
SELECT enumlabel AS auction_length
FROM pg_enum
JOIN pg_type ON pg_enum.enumtypid = pg_type.oid
WHERE pg_type.typname = 'auctionlengthenum'
ORDER BY pg_enum.enumsortorder;
*/

--1.9 Delete Rating
/*
SELECT user_type
FROM “user”
WHERE username = GBurdell;


DELETE FROM "rating"
WHERE username = GBurdell AND item_id = 1;

SELECT * FROM "rating";
*/

--1.14 View Category Report
/*
SELECT 
    i.category_name AS "Category",
    COUNT(i.item_id) AS "Total Items",
    MIN(i.get_it_now_price) FILTER (WHERE i.get_it_now_price > 0) AS "Min Price",
    MAX(i.get_it_now_price) AS "Max Price",
    ROUND(AVG(i.get_it_now_price) FILTER (WHERE i.get_it_now_price > 0), 2) AS "Average Price"
FROM "item" i
WHERE i.cancellation_reason IS NULL
GROUP BY i.category_name
ORDER BY i.category_name ASC;
*/

--1.19 View Item Listing (Done)
/*
SELECT 
    item_id, 
    name AS "Item Name",
    description AS "Description", 
    category_name AS "Category",
    condition AS "Condition",
    is_returnable AS "Returns Accepted",
    get_it_now_price AS "Get It Now Price",
    end_time AS "Auction Ended"
FROM "item" 
WHERE item_id = 1;


SELECT
  CASE
	WHEN bid_amount = 0 THEN 'Cancelled'
	ELSE bid_amount::text
  END AS "Bid Amount",
  bid_time AS "Time of Bid",
  username AS "Username"
FROM bid
WHERE item_id = 1
ORDER BY bid_time DESC;
*/



--1.5 Search Item (tested) 
/* Notes:
    if there are no bids (max(b.bid_amount)) returns null, then use i.starting_bid instead);
    tested parts at a time, then holistically with diff values (using all current values rn returns nothing)
SELECT
    i.item_id,
    i.name,
    COALESCE(MAX(b.bid_amount)::text, '--') AS current_bid,
    (
      SELECT b.username 
      FROM "bid" b 
      WHERE b.item_id = i.item_id 
      ORDER BY b.bid_amount DESC 
      LIMIT 1
    ) AS high_bidder,
    COALESCE(i.get_it_now_price::text, '--') AS get_it_now_price,
    i.end_time AS auction_ends
FROM 
    "item" i
LEFT OUTER JOIN 
    "bid" b ON i.item_id = b.item_id
GROUP BY 
    i.item_id
HAVING
    (i.name LIKE '%' || 'playstation' || '%' OR 'playstation' IS NULL) OR 
    (i.description LIKE '%' || 'playstation' || '%' OR 'playstation' IS NULL) AND
    (COALESCE(MAX(b.bid_amount), i.starting_bid) >= 105.00 OR 105.00 IS NULL) AND
    (COALESCE(MAX(b.bid_amount), i.starting_bid) <= 150.00 OR 150.00 IS NULL) AND
    (i.category_name = 'Cookies' OR 'Cookies' IS NULL) AND
    (i.condition <= 'Good' OR 'Good' IS NULL) AND 
    i.end_time > NOW() AND 
    i.cancellation_reason IS NULL
ORDER BY 
    i.end_time ASC;
*/

--1.10 View Auction Results (tested)
/*
SELECT 
    i.item_id AS "ID",
    i.name AS "Item Name",
    CASE
        WHEN (mb.max_bid >= i.min_sale_price) AND i.cancellation_reason IS NULL 
        THEN COALESCE(mb.max_bid::text, '--')
        WHEN (mb.max_bid < i.min_sale_price) AND i.cancellation_reason IS NULL THEN '--'
        WHEN mb.max_bid IS NULL AND i.cancellation_reason IS NULL THEN '--'
        WHEN i.cancellation_reason IS NOT NULL THEN '--' --auction got canceled 
        ELSE '--' 
    END AS "Sale Price",
    CASE 
        WHEN mb.max_bid >= i.min_sale_price THEN (
            SELECT b.username 
            FROM "bid" b 
            WHERE b.item_id = i.item_id AND b.bid_amount = mb.max_bid
            ORDER BY b.bid_time DESC
            LIMIT 1
        )
        WHEN (mb.max_bid < i.min_sale_price) AND i.cancellation_reason IS NULL THEN '--'
        WHEN mb.max_bid IS NULL AND i.cancellation_reason IS NULL THEN '--'
        WHEN i.cancellation_reason IS NOT NULL THEN 'Canceled'
        ELSE '--'
    END AS "Winner",
    i.end_time AS "Auction Ended"
FROM "item" i
LEFT JOIN (
    SELECT 
        item_id,
        MAX(bid_amount) AS max_bid
    FROM "bid"
    GROUP BY item_id
) AS mb ON i.item_id = mb.item_id
WHERE i.end_time <= NOW();
*/

--1.15 View User Reports (tested)
/*
WITH UserListings AS (
    SELECT
        username,
        COUNT(*) AS total_listings,
        COUNT(DISTINCT item_id) AS unique_listings
    FROM "item" i
    GROUP BY username
), UserSold AS (
    SELECT
        i.username,
        COUNT(*) AS total_sold
    FROM "item" i
    JOIN "bid" b ON b.item_id = i.item_id 
    WHERE b.bid_amount >= i.min_sale_price AND 
    i.end_time <= NOW() AND 
    i.cancellation_reason IS NULL 
    GROUP BY i.username
), UserWins AS (
    SELECT
        b.username,
        COUNT(*) AS wins
    FROM "bid" b
    JOIN "item" i ON b.item_id = i.item_id 
    WHERE 
    b.bid_amount >= i.min_sale_price AND
    b.bid_time = (
      SELECT MAX(bid_time)
      FROM "bid"
      WHERE item_id = b.item_id
    ) AND
    i.cancellation_reason IS NULL
    GROUP BY b.username
), UserComments AS (
    SELECT
        username,
        COUNT(DISTINCT date_and_time) AS total_comments
    FROM "rating"
    JOIN "item" ON item.item_id = rating.item_id
    GROUP BY username
), MostFrequentCondition AS (
    SELECT
        cc.username,
        COALESCE(cc.condition::text, 'N/A') AS most_frequent_condition
    FROM (
        SELECT DISTINCT ON (username) username, condition
        FROM (
            SELECT 
                username,
                condition,
                COUNT(*) AS condition_count
            FROM "item"
            GROUP BY username, condition
            ORDER BY username, condition_count DESC
        ) AS condition_counts
    ) AS cc
)
SELECT
    u.username AS "Username",
    COALESCE(ul.total_listings, 0) AS "Listed",
    COALESCE(us.total_sold, 0) AS "Sold",
    COALESCE(uw.wins, 0) AS "Won",
    COALESCE(uc.total_comments, 0) AS "Rated",
    COALESCE(mfc.most_frequent_condition::text, 'N/A') AS "Most Frequent Condition"
FROM "user" u
LEFT JOIN UserListings ul ON u.username = ul.username
LEFT JOIN UserSold us on u.username = us.username
LEFT JOIN UserWins uw ON u.username = uw.username
LEFT JOIN UserComments uc ON u.username = uc.username
LEFT JOIN MostFrequentCondition mfc ON u.username = mfc.username
ORDER BY total_listings DESC;
/*
