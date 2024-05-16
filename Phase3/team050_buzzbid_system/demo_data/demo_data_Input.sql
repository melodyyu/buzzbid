-----------------------------------------------------------------------
--                        Drop Tables and Types                      --
-----------------------------------------------------------------------
DROP TYPE user_type_enum CASCADE;
DROP TYPE condition_enum CASCADE;
DROP TYPE auction_length_enum CASCADE;

DROP TABLE "user" CASCADE;
DROP TABLE "adminuser" CASCADE;
DROP TABLE "category" CASCADE;
DROP TABLE "item" CASCADE;
DROP TABLE "rating" CASCADE;
DROP TABLE "bid" CASCADE;

-----------------------------------------------------------------------
--   User Type, Item Condition, Auction Length enums (PostgreSQL)    --
-----------------------------------------------------------------------

CREATE TYPE user_type_enum AS ENUM ('Regular', 'Admin');
CREATE TYPE condition_enum AS ENUM ('New', 'Very Good', 'Good', 'Fair', 'Poor');
CREATE TYPE auction_length_enum AS ENUM ('1','3','5','7');

-----------------------------------------------------------------------
--                 Create table schema (PostgreSQL)                  --
-----------------------------------------------------------------------
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
    get_it_now_price DECIMAL(10,2),
    end_time TIMESTAMP WITH TIME ZONE NOT NULL,
    is_returnable BOOLEAN NOT NULL,
    cancellation_reason VARCHAR(250),
    PRIMARY KEY (item_id),
    FOREIGN KEY (username) REFERENCES "user" (username) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (category_name) REFERENCES "category" (category_name) ON DELETE CASCADE ON UPDATE CASCADE,
    CHECK (get_it_now_price IS NULL OR (get_it_now_price > starting_bid AND get_it_now_price > min_sale_price AND starting_bid <= min_sale_price)),
    CHECK (starting_bid > 0),
    CHECK (min_sale_price > 0),
    CHECK (get_it_now_price > 0 OR get_it_now_price IS NULL)
);

CREATE TABLE "rating" (
    item_id INT NOT NULL,
    comments VARCHAR(5000),
    number_of_stars INT NOT NULL CHECK (number_of_stars IN (0, 1, 2, 3, 4, 5)),
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

ALTER SEQUENCE item_item_id_seq RESTART WITH 1;

-- Insert into user table
INSERT INTO "user" (username, password, first_name, last_name, user_type) VALUES
('ablack', '1234', 'Alex', 'Black', 'Regular'),
('admin1', 'opensesame', 'Riley', 'Fuiss', 'Admin'),
('admin2', 'opensesayou', 'Tonnis', 'Kinser', 'Admin'),
('apink', '1234', 'Alice', 'Pink', 'Regular'),
('jbrian', '1234', 'James', 'O''Brian', 'Regular'),
('jgreen', '1234', 'John', 'Green', 'Regular'),
('jsmith', '1234', 'John', 'Smith', 'Regular'),
('mred', '12345', 'Michael', 'Red', 'Admin'),
('o''brian', '1234', 'Jack', 'Brian', 'Regular'),
('pbrown', '1234', 'Peter', 'Brown', 'Regular'),
('Pink', '1234', 'apink', 'Alice', 'Regular'),
('porange', '1234', 'Peter', 'Orange', 'Regular'),
('tblue', '1234', 'Tom', 'Blue', 'Regular'),
('trichards', '1234', 'Tom', 'Richards', 'Regular'),
('user1', 'pass1', 'Danite', 'Kelor', 'Regular'),
('user2', 'pass2', 'Dodra', 'Kiney', 'Regular'),
('user3', 'pass3', 'Peran', 'Bishop', 'Regular'),
('user4', 'pass4', 'Randy', 'Roran', 'Regular'),
('user5', 'pass5', 'Ashod', 'Iankel', 'Regular'),
('user6', 'pass6', 'Cany', 'Achant', 'Regular');

-- Insert into adminuser table
INSERT INTO "adminuser" (username, position) VALUES
('admin1', 'Technical Support'),
('admin2', 'Chief Techy'),
('mred', 'CEO');

INSERT INTO "category" (category_name) VALUES 
('Books'),
('Art'),
('Home & Garden'),
('Electronics'),
('Sporting Goods'),
('Other'),
('Toys');

-- Insert into item table
INSERT INTO "item" (
    username,
    name,
    description,
    starting_bid,
    condition,
    get_it_now_price,
    min_sale_price,
    is_returnable,
    end_time,
    category_name,
    cancellation_reason
) VALUES
    ('pbrown', 'good book', 'good book', 20, 'New', 80, 50, TRUE, '2024-02-02 22:48:00+00', 'Books', NULL),
    ('pbrown', 'good book', 'the best book', 10, 'Good', 70, 18.63, FALSE, '2024-02-07 22:44:00+00', 'Books', NULL),
    ('mred', 'painting', 'good picture', 100, 'Very Good', 300, 200, TRUE, '2024-02-03 12:36:00+00', 'Art', NULL),
    ('mred', 'plant', 'great plant', 500, 'Very Good', 1000, 538.16, FALSE, '2024-02-06 15:21:00+00', 'Home & Garden', NULL),
    ('mred', 'computer1', 'old computer', 300, 'Fair', 750, 500, TRUE, '2024-02-04 16:32:00+00', 'Electronics', 'Item is no longer available.'),
    ('jgreen', 'skates', 'for skating', 250, 'New', 450, 350, FALSE, '2024-04-21 23:59:00+00', 'Sporting Goods', NULL),
    ('pbrown', 'plant', 'another plant', 40, 'Good', 70, 60, TRUE, '2024-02-10 20:53:00+00', 'Other', NULL),
    ('tblue', 'lego toy', 'very interesting toy this is not very informative description', 30, 'Very Good', 75, 50, FALSE, '2024-04-21 23:59:00+00', 'Toys', NULL),
    ('jgreen', 'sculpture', 'expensive', 1000, 'Very Good', 3000, 1058.53, FALSE, '2024-04-21 23:59:00+00', 'Art', NULL),
    ('tblue', 'good book', 'one more good book', 50, 'New', NULL, 58.93, TRUE, '2024-02-11 10:59:00+00', 'Books', NULL),
    ('tblue', 'good book', 'book posted after some time', 25, 'Fair', 75, 55, FALSE, '2024-04-21 23:59:00+00', 'Books', NULL),
    ('mred', 'item with really long name how would it show', 'this is an item with really long name to test if it would be acceptable in all screens', 100, 'New', NULL, 122.68, TRUE, '2024-02-19 13:44:00+00', 'Other', NULL),
    ('tblue', 'Garmin GPS', 'Brand new last model GPS', 200, 'New', NULL, 350, TRUE, '2024-04-21 23:59:00+00', 'Electronics', NULL),
    ('jgreen', 'later GPS', 'GPS listed later', 300, 'New', 600, 400, FALSE, '2024-04-21 23:59:00+00', 'Electronics', NULL),
    ('jgreen', 'still later GPS', 'still later GPS', 400, 'New', NULL, 600, TRUE, '2024-04-21 23:59:00+00', 'Electronics', NULL),
    ('jgreen', 'still still later GPS', 'still still later GPS', 500, 'New', NULL, 501.95, TRUE, '2024-02-22 09:11:00+00', 'Electronics', NULL),
    ('ablack', 'good book', 'new book listed', 20, 'New', 100, 50, TRUE, '2024-02-18 12:43:00+00', 'Books', NULL),
    ('ablack', 'plant', 'great gazebo', 1000, 'Good', 3000, 2000, FALSE, '2024-04-21 23:59:00+00', 'Home & Garden', NULL),
    ('tblue', 'painting', 'pretty good painting', 300, 'New', 700, 500, FALSE, '2024-02-18 13:33:00+00', 'Art', NULL),
    ('tblue', 'Art Albom', 'Albom of classic art illustrations', 250, 'New', 750, 250.81, FALSE, '2024-02-27 16:38:00+00', 'Art', NULL),
    ('jgreen', 'Art Albom', 'listed by jgreen', 100, 'New', NULL, 200, FALSE, '2024-02-26 07:27:00+00', 'Art', 'Item is no longer available.'),
    ('tblue', 'ite with very long name just to see how it works', 'item with long name', 10, 'New', 50, 30, TRUE, '2024-02-23 17:11:00+00', 'Other', 'User requested. Wrong minimum price.'),
    ('pbrown', 'now i want to make the item name as long as i can and even longer than anyone of the items I made before', 'long name again', 20, 'New', 75, 50, FALSE, '2024-04-21 23:59:00+00', 'Other', NULL),
    ('pbrown', 'once again item with very long item name and how it will be seen in the tables which i will be creating', 'again long item name', 10, 'New', 30, 20, FALSE, '2024-04-21 23:59:00+00', 'Other', NULL),
    ('jgreen', 'item to buy', 'just to have it bought', 15, 'New', 35, 25, TRUE, '2024-02-23 15:34:00+00', 'Other', NULL),
    ('mred', 'furby', 'old toy', 50, 'Good', 70, 60, FALSE, '2024-02-23 15:46:00+00', 'Toys', NULL),
    ('pbrown', 'Nexus', 'tablet', 100, 'New', 200, 150, TRUE, '2024-02-23 15:51:00+00', 'Electronics', NULL),
    ('pbrown', 'once again just to buy', 'just to buy', 5, 'New', 15, 10, FALSE, '2024-02-23 15:59:00+00', 'Other', NULL),
    ('pbrown', 'third one to buy', 'third to buy', 5, 'Poor', 18, 10, FALSE, '2024-02-23 16:04:00+00', 'Other', NULL),
    ('pbrown', 'fourth to sell immediately', 'to sell', 10, 'Poor', 20, 15, FALSE, '2024-02-23 16:06:00+00', 'Other', NULL),
    ('pbrown', 'fifth for sale immediate', 'for sale immediate fifth', 4, 'New', 15, 10, FALSE, '2024-02-23 16:16:00+00', 'Other', NULL),
    ('pbrown', 'sixth to sell immediate', 'sixth to sell immediate', 3, 'New', 7, 5, TRUE, '2024-02-23 16:22:00+00', 'Other', NULL),
    ('pbrown', 'eighth to check for sale immediate', 'eighth to sell', 2, 'Poor', 6, 4, TRUE, '2024-02-23 16:27:00+00', 'Other', NULL),
    ('tblue', 'ninth to sell', 'ninth to sell', 1, 'New', 5, 3, TRUE, '2024-02-23 16:32:00+00', 'Art', NULL),
    ('trichards', 'detective novel', 'Interesting spy novel', 20, 'New', 40, 30, FALSE, '2024-03-03 19:41:00+00', 'Books', NULL),
    ('ablack', 'sculpture', 'ancient sculpture', 100, 'Very Good', NULL, 350, FALSE, '2024-03-06 19:36:00+00', 'Art', NULL),
    ('jgreen', 'my item', 'very simple item', 1, 'Poor', 10, 5, TRUE, '2024-03-04 21:43:00+00', 'Other', NULL),
    ('jsmith', 'good book', 'Spanish-English', 30, 'New', 50, 40, FALSE, '2024-04-21 23:59:00+00', 'Books', NULL),
    ('jsmith', 'sculpture', 'not so old sculpture', 200, 'Very Good', 600, 400, FALSE, '2024-03-07 13:49:00+00', 'Art', NULL),
    ('ablack', 'something', 'strange thing', 10, 'Good', 30, 15, FALSE, '2024-03-07 13:35:00+00', 'Other', NULL),
   	('ablack', 'something', 'even more strange thing', 15, 'Fair', 35, 15.23, TRUE, '2024-03-10 13:36:00+00', 'Other', NULL),
    ('porange', 'good book', 'interesting book', 20, 'Very Good', 50, 35, TRUE, '2024-03-07 19:11:00+00', 'Books', NULL),
    ('tblue', 'sculpture', 'good sculpture', 300, 'Good', 750, 500, FALSE, '2024-03-09 05:44:00+00', 'Art', 'User requested. Wrong minimum price.'),
    ('user1', 'Garmin GPS', 'This is a great GPS.', 50, 'Very Good', 99, 70, FALSE, '2024-02-28 12:22:00+00', 'Electronics', NULL),
    ('user1', 'Canon Powershot', 'Point and shoot!', 40, 'Good', 80, 60, FALSE, '2024-02-29 13:55:00+00', 'Electronics', NULL),
    ('user2', 'Nikon D3', 'New and in box!', 1500, 'New', 2000, 1589.35, FALSE, '2024-03-04 09:19:00+00', 'Electronics', NULL),
    ('user3', 'Danish Art Book', 'Delicious Danish Art', 10, 'Very Good', 15, 10, TRUE, '2024-03-02 11:41:00+00', 'Art', 'Cancelled by Admin'),
    ('admin1', 'SQL in 10 Minutes', 'Learn SQL really fast!', 5, 'Fair', 12, 10, FALSE, '2024-03-04 16:48:00+00', 'Books', NULL),
    ('admin2', 'SQL in 8 Minutes', 'Learn SQL even faster!', 5, 'Good', 10, 8, FALSE, '2024-03-07 10:01:00+00', 'Books', NULL),
    ('user6', 'Pull-up Bar', 'Works on any door frame.', 20, 'New', 40, 25, TRUE, '2024-03-08 22:09:00+00', 'Sporting Goods', NULL),
    ('jgreen', 'painting', 'round table', 300, 'New', 750, 500, TRUE, '2024-03-11 18:17:00+00', 'Home & Garden', NULL),
    ('admin1', 'good book', 'very good thing', 35, 'Good', 75, 36.21, FALSE, '2024-03-16 18:18:00+00', 'Other', NULL),
    ('jgreen', 'thingy', 'what is thingy?', 20, 'New', 50, 30, FALSE, '2024-03-14 07:05:00+00', 'Art', 'User can no longer be reached.');
    
-- Insert into bid table
INSERT INTO "bid" (username, item_id, bid_time, bid_amount) VALUES
('tblue', 1, '2024-02-02 22:48:00+00', 80),
('mred', 2, '2024-02-02 22:46:00+00', 10),
('user1', 2, '2024-02-03 13:07:00+00', 13),
('admin2', 2, '2024-02-03 13:07:00+00', 15),
('tblue', 2, '2024-02-03 13:09:00+00', 18),
('user2', 2, '2024-02-03 13:09:00+00', 20),
('tblue', 2, '2024-02-03 13:10:00+00', 22),
('jsmith', 2, '2024-02-03 13:10:00+00', 24),
('jgreen', 2, '2024-02-03 16:35:00+00', 30),
('tblue', 3, '2024-02-03 12:34:00+00', 100),
('jgreen', 3, '2024-02-03 12:35:00+00', 105),
('pbrown', 3, '2024-02-03 12:36:00+00', 300),
('jgreen', 4, '2024-02-03 16:35:00+00', 550),
('jgreen', 4, '2024-02-03 16:36:00+00', 600),
('pbrown', 4, '2024-02-04 12:19:00+00', 603.78),
('pbrown', 4, '2024-02-04 12:19:10+00', 606),
('user4', 5, '2024-02-03 16:33:00+00', 300),
('admin1', 5, '2024-02-03 20:09:19+00', 0),
('mred', 10, '2024-02-10 11:00:00+00', 50),
('mred', 10, '2024-02-10 11:01:00+00', 53),
('jgreen', 10, '2024-02-10 11:01:00+00', 55),
('mred', 10, '2024-02-10 11:03:00+00', 57),
('mred', 10, '2024-02-10 11:02:00+00', 58),
('mred', 10, '2024-02-10 11:27:00+00', 60),
('mred', 10, '2024-02-10 11:28:00+00', 61),
('mred', 10, '2024-02-10 11:31:00+00', 63),
('mred', 10, '2024-02-10 11:33:00+00', 67),
('pbrown', 10, '2024-02-10 11:33:00+00', 70),
('Pink', 12, '2024-02-14 13:48:00+00', 101),
('admin1', 12, '2024-02-14 13:50:00+00', 105),
('pbrown', 12, '2024-02-14 20:58:00+00', 120),
('pbrown', 12, '2024-02-14 21:00:00+00', 125),
('ablack', 16, '2024-02-18 11:39:00+00', 508),
('mred', 16, '2024-02-19 15:10:00+00', 515),
('tblue', 16, '2024-02-19 15:11:00+00', 516),
('mred', 16, '2024-02-19 15:11:00+00', 517),
('jsmith', 17, '2024-02-18 12:42:00+00', 20),
('trichards', 17, '2024-02-18 12:43:00+00', 25),
('apink', 17, '2024-02-18 12:43:00+00', 100),
('jsmith', 19, '2024-02-18 13:31:00+00', 300),
('pbrown', 19, '2024-02-18 13:32:00+00', 305),
('jgreen', 19, '2024-02-18 13:32:00+00', 310),
('jbrian', 19, '2024-02-18 13:33:00+00', 700),
('apink', 20, '2024-02-22 16:39:00+00', 255),
('admin1', 21, '2024-02-26 07:27:49+00', 0),
('admin1', 22, '2024-02-23 17:11:40+00', 0),
('user6', 25, '2024-02-23 15:34:00+00', 35),
('jbrian', 26, '2024-02-23 15:43:00+00', 52),
('user1', 26, '2024-02-23 15:44:00+00', 55),
('pbrown', 26, '2024-02-23 15:46:00+00', 70),
('user5', 27, '2024-02-23 15:51:00+00', 200),
('trichards', 28, '2024-02-23 15:59:00+00', 15),
('apink', 29, '2024-02-23 16:04:00+00', 18),
('user3', 30, '2024-02-23 16:06:00+00', 20),
('user3', 31, '2024-02-23 16:16:00+00', 15),
('mred', 32, '2024-02-23 16:22:00+00', 7),
('o''brian', 33, '2024-02-23 16:27:00+00', 6),
('admin2', 34, '2024-02-23 16:32:00+00', 5),
('pbrown', 35, '2024-03-03 19:35:00+00', 22),
('mred', 35, '2024-03-03 19:38:00+00', 25),
('pbrown', 35, '2024-03-03 19:39:00+00', 28),
('mred', 35, '2024-03-03 19:39:00+00', 30),
('admin2', 35, '2024-03-03 19:40:00+00', 33),
('pbrown', 35, '2024-03-03 19:40:00+00', 35),
('pbrown', 35, '2024-03-03 19:41:00+00', 40),
('mred', 36, '2024-03-03 19:38:00+00', 120),
('pbrown', 36, '2024-03-03 21:00:00+00', 122),
('pbrown', 36, '2024-03-03 21:06:00+00', 124),
('mred', 36, '2024-03-03 21:42:00+00', 126),
('pbrown', 39, '2024-03-06 13:14:00+00', 250),
('mred', 39, '2024-03-06 13:15:00+00', 253),
('jgreen', 39, '2024-03-07 13:49:00+00', 600),
('tblue', 40, '2024-03-07 13:34:00+00', 10),
('jgreen', 40, '2024-03-07 13:34:00+00', 11),
('tblue', 40, '2024-03-07 13:35:00+00', 30),
('pbrown', 41, '2024-03-08 11:34:00+00', 16),
('tblue', 42, '2024-03-07 19:09:00+00', 20),
('pbrown', 42, '2024-03-07 19:11:00+00', 21),
('tblue', 42, '2024-03-07 19:11:00+00', 25),
('tblue', 42, '2024-03-07 19:11:10+00', 50),
('admin1', 43, '2024-03-09 05:44:37+00', 0),
('user4', 44, '2024-02-27 14:53:00+00', 50),
('user5', 44, '2024-02-27 16:45:00+00', 55),
('user4', 44, '2024-02-27 19:28:00+00', 75),
('user5', 44, '2024-02-28 10:00:00+00', 85),
('user6', 45, '2024-02-29 13:55:00+00', 80),
('user1', 46, '2024-03-03 08:37:00+00', 1500),
('user3', 46, '2024-03-03 09:15:00+00', 1501),
('user1', 46, '2024-03-03 12:27:00+00', 1795),
('admin1', 47, '2024-03-02 11:41:18+00', 0),
('user4', 50, '2024-03-07 20:20:00+00', 20),
('user2', 50, '2024-03-08 21:15:00+00', 25),
('user5', 51, '2024-03-11 10:55:00+00', 745),
('admin1', 51, '2024-03-11 18:17:00+00', 750),
('jgreen', 52, '2024-03-11 18:24:00+00', 35),
('jgreen', 52, '2024-03-11 18:24:10+00', 37),
('admin1', 53, '2024-03-14 07:05:17+00', 0);

-- Insert into rating table
INSERT INTO "rating" (item_id, comments, number_of_stars, date_and_time) VALUES
(2, 'very good book', 4, '2024-02-03 16:36:00+00'),
(3, 'maybe quite useful', 4, '2024-02-03 13:52:00+00'),
(4, 'this is review of another plant by pbrown', 2, '2024-02-05 20:54:00+00'),
(10, 'impossible to rate', 0, '2024-02-11 05:16:00+00'),
(12, 'and i will chamge this one', 0, '2024-02-14 16:15:00+00'),
(16, 'dfsd', 5, '2024-02-19 15:10:00+00'),
(17, 'impossible to rate', 1, '2024-02-20 12:31:00+00'),
(19, 'never saw anything like that', 1, '2024-02-19 04:49:00+00'),
(20, 'no so great albom', 2, '2024-02-22 17:05:00+00'),
(25, 'one more useless comment', 2, '2024-02-24 15:20:00+00'),
(27, 'how would I rate it', 0, '2024-02-26 02:52:00+00'),
(30, 'never saw anything like that', 3, '2024-02-24 12:51:00+00'),
(32, 'let me think what I can write', 2, '2024-02-23 20:10:00+00'),
(34, 'let me think what I can write', 4, '2024-02-26 07:55:00+00'),
(35, 'something to look at', 4, '2024-03-06 01:50:00+00'),
(39, 'very bad sculpture', 0, '2024-03-06 13:14:00+00'),
(40, 'never saw anything like that', 1, '2024-03-09 16:11:00+00'),
(41, 'not so good something', 0, '2024-03-07 13:37:00+00'),
(42, 'very nice item', 1, '2024-03-10 03:14:00+00'),
(44, 'Great GPS!', 5, '2024-02-27 17:00:00+00'),
(45, 'never saw anything like that', 1, '2024-03-01 19:12:00+00'),
(46, 'never saw anything like that', 4, '2024-03-04 15:01:00+00'),
(50, 'so-so', 5, '2024-03-10 06:58:00+00'),
(51, 'etetete', 3, '2024-03-11 18:16:00+00'),
(52, 'really bvery good', 4, '2024-03-11 18:26:00+00');
