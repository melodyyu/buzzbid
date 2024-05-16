-----------------------------------------------------------------------
--   User Type, Item Condition, Auction Length enums (PostgreSQL)    --
-----------------------------------------------------------------------

CREATE TYPE user_type_enum AS ENUM ('Regular', 'Admin');
CREATE TYPE condition_enum AS ENUM ('New', 'Very Good', 'Good', 'Fair', 'Poor');
CREATE TYPE auction_length_enum AS ENUM ('1','3','5','7');

-----------------------------------------------------------------------
--                 Create table schema (PostgreSQL)                  --
-----------------------------------------------------------------------

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

CREATE TABLE "category" (
    category_name VARCHAR(50) NOT NULL,
    PRIMARY KEY (category_name)
);