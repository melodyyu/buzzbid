from database.connection import execute_query

class ItemHandlerService:
    @staticmethod
    def fetch_item_info(item_id):
        query = """
                SELECT
                    i.item_id AS "Item ID",
                    i.name AS "Item Name", 
                    i.description AS "Description",
                    i.category_name AS "Category",
                    i.condition AS "Condition",
                    i.is_returnable AS "Returns Accepted?",
                    i.get_it_now_price AS "Get It Now Price",
                    i.end_time AS "Auction Ends", 
                    i.cancellation_reason AS "Cancellation Reason",
                    COALESCE(MAX(b.bid_amount)+1, i.starting_bid) AS "Minimum Bid",
                    i.username AS "Seller",
                    i.min_sale_price AS "Minimum Sale Price"
                FROM "item" i
                LEFT JOIN "bid" b ON i.item_id = b.item_id 
                WHERE i.item_id = %s
                GROUP BY i.item_id;
                """
        result = execute_query(query, (item_id,))
        return result
    
    @staticmethod
    def fetch_bidding_info(item_id):
        query = """
                SELECT
                    bid_amount AS "Bid Amount", 
                    bid_time AS "Time of Bid", 
                    username AS “Username”
                FROM bid
                WHERE item_id = %s
                ORDER BY bid_time DESC, bid_amount DESC LIMIT 4;
                """
        result = execute_query(query, (item_id,))
        return result
    

    @staticmethod
    def check_bid_price(item_id):
        query = """
                SELECT
                    COALESCE(MAX(b.bid_amount), i.starting_bid) AS highest_bid, 
                    i.get_it_now_price
                FROM "item" i
                LEFT JOIN "bid" b ON i.item_id = b.item_id 
                WHERE i.item_id = %s
                GROUP BY i.item_id, i.get_it_now_price;
                """
        result = execute_query(query, (item_id,))

        if result:
            # Assuming the query returns a row with two columns: highest_bid and get_it_now_price
            highest_bid = result[0][0] if result[0][0] is not None else 0
            get_it_now_price = result[0][1]
            return highest_bid, get_it_now_price
        else:
            # Return default values if the query returns no result
            return 0, None
        # return result
    

    @staticmethod
    def bid_on_item(username,item_id,bid_amount):
        query = """
                INSERT INTO Bid (username, item_id, bid_time, bid_amount) VALUES (%s, %s, NOW(), %s);
                """
        result = execute_query(query, (username, item_id, bid_amount))
        return result
    

    @staticmethod
    def fetch_average_rating(item_name):
        query = """
        SELECT DISTINCT
            ROUND(AVG(r.number_of_stars) OVER (PARTITION BY i.name), 1) AS avg_rating
        FROM "item" i
        JOIN "rating" r ON i.item_id = r.item_id
        WHERE i.name = %s;
        """
        return execute_query(query, (item_name,))


    @staticmethod
    def fetch_user_ratings(item_name):
        query = """
        SELECT 
            b.username AS "Rated by",
            r.number_of_stars, 
            r.comments, 
            r.date_and_time AS "Date",
            i.item_id
        FROM 
            rating r
        JOIN 
            item i ON i.item_id = r.item_id
        JOIN 
            bid b ON b.item_id = i.item_id
        WHERE 
            i.name = %s
            AND i.end_time < NOW()
            AND b.bid_amount = (
                SELECT MAX(bid_amount) 
                FROM bid 
                WHERE item_id = i.item_id AND bid_time <= i.end_time
            )
        ORDER BY 
            r.date_and_time DESC;
        """
        return execute_query(query, (item_name,))
    
    @staticmethod
    def submit_rating(item_id,number_of_stars,comments):
        try:
            query = """
            INSERT INTO "rating" (item_id, number_of_stars, comments, date_and_time)
            VALUES (%s, %s, %s, NOW());
            """
            execute_query(query, (item_id,number_of_stars,comments))

            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
    

    @staticmethod
    def get_it_now(username,item_id,bid_amount):
        try:
            
            current_timestamp_query = "SELECT NOW();"
            timestamp_result = execute_query(current_timestamp_query)
            if not timestamp_result:
                print("Failed to fetch current timestamp.")
                return False

            current_timestamp = timestamp_result[0][0]

            bid_query = """
                INSERT INTO Bid (username, item_id, bid_time, bid_amount) VALUES (%s, %s, %s, %s);
            """
            execute_query(bid_query, (username, item_id, current_timestamp, bid_amount))

            end_bid_query = """UPDATE item SET end_time = %s WHERE item_id = %s"""
            execute_query(end_bid_query, (current_timestamp, item_id))

            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False  # Return False if any exception was caught
        

    @staticmethod
    def fetch_categories():
        try:
            query = """
                SELECT category_name AS item_category
                FROM "category"
                ORDER BY category_name ASC;
                """
            
            result = execute_query(query) 
            return result
        
        except Exception as e:
            print(f"Unable to get categories {e}")
            return False


    @staticmethod
    def fetch_conditions():
        query = """ SELECT enumlabel 
                    FROM pg_enum 
                    JOIN pg_type ON pg_enum.enumtypid = pg_type.oid 
                    WHERE pg_type.typname = 'condition_enum';
                """
        result = execute_query(query)
        return result

    @staticmethod
    def fetch_auction_lengths():
        query = """ SELECT enumlabel 
                    FROM pg_enum 
                    JOIN pg_type ON pg_enum.enumtypid = pg_type.oid 
                    WHERE pg_type.typname = 'auction_length_enum';
                """
        result = execute_query(query)
        return result

    @staticmethod 
    def get_latest_item_id():
        query = """ SELECT item_id 
                    FROM "item"
                    ORDER BY item_id DESC
                    LIMIT 1;
                """
        result = execute_query(query)
        return result

    @staticmethod
    def update_item_description(item_id, new_description):
        # Assuming execute_query is defined to handle database operations
        query = """
        UPDATE "item" SET description = %s WHERE item_id = %s;
        """
        execute_query(query, (new_description, item_id))


    @staticmethod
    def cancel_item(item_id, cancellation_reason, username):
        """
        Cancel an auction item.

        :param item_id: ID of the item to cancel
        :param cancellation_reason: Reason for cancellation
        :param username: Username of the user performing the cancellation
        :return: Boolean indicating success of the operation
        """
        # Set a default cancellation reason if none provided
        cancellation_reason = cancellation_reason if cancellation_reason.strip() else "Cancelled by Admin"

        # Record a $0 'cancellation bid'
        execute_query("""
            INSERT INTO bid (username, item_id, bid_time, bid_amount)
            VALUES (%s, %s, NOW(), 0)
            """, (username, item_id))

        # Update the item's cancellation reason and end_time
        execute_query("""
            UPDATE item
            SET end_time = NOW(),
                cancellation_reason = %s
            WHERE item_id = %s
            """, (cancellation_reason, item_id))

        return True  # Adjust based on your error handling strategy

    @staticmethod
    def has_user_rated(item_id, current_user):
        query = """
        SELECT b.username
        FROM item i JOIN rating r ON i.item_id = r.item_id 
        JOIN bid b on i.item_id = b.item_id and b.bid_time <= i.end_time
        WHERE r.item_id = %s
        ORDER BY b.bid_time DESC, b.bid_amount DESC;
        """

        result = execute_query(query, (item_id,))
        if result and current_user == result[0][0]:
            return True
        else:
            return False
        
    
    @staticmethod
    def delete_user_rating(item_id):
        #print('test:',item_id)
        query = """
        DELETE FROM rating WHERE item_id = %s;
        """
        result = execute_query(query, (item_id,))
        return True
    
    @staticmethod
    def get_auction_results():
        try:
            query = """
                    SELECT
                    i.item_id AS "ID", 
                    i.name AS "Item Name", 
                    CASE
    					-- high bid wins item and auction timed out
    					WHEN (mb.max_bid >= i.min_sale_price) AND (mb.max_bid < i.get_it_now_price) AND i.cancellation_reason IS NULL 
        					THEN COALESCE(mb.max_bid::text, '-')
        				-- item was purchased with get_it_now_price and auction ended immediately 
        				WHEN (mb.max_bid = i.get_it_now_price) AND i.cancellation_reason IS NULL 
        					THEN COALESCE(mb.max_bid::text, '-')
        				-- highest bid was lower than minimum sale price, auction timed out 
        				WHEN (mb.max_bid < i.min_sale_price) AND i.cancellation_reason IS NULL 
        					THEN '-'
        				-- no bids were placed 
    					WHEN mb.max_bid IS NULL AND i.cancellation_reason IS NULL 
        					THEN '-'
        				-- auction was canceled
        				WHEN i.cancellation_reason IS NOT NULL 
        					THEN '-' 
        				else '-'
        			end as "Sale Price",
        			CASE
    					-- high bid won item and auction timed out 
  						WHEN mb.max_bid >= i.min_sale_price AND i.cancellation_reason IS NULL
        					THEN (
					            SELECT b.username
					            FROM "bid" b
					            WHERE b.item_id = i.item_id AND b.bid_amount = mb.max_bid 
					            ORDER BY b.bid_time DESC
					            LIMIT 1 )
					    -- item was purchased with get_it_now_price and auction ended immediately 
					    WHEN (mb.max_bid = i.get_it_now_price) AND i.cancellation_reason IS NULL
					        THEN (
					            SELECT b.username
					            FROM "bid" b
					            WHERE b.item_id = i.item_id AND b.bid_amount = mb.max_bid 
					            ORDER BY b.bid_time DESC
					            LIMIT 1 )
					    -- highest bid was lower than minimum sale price and auction timed out 
					    WHEN (mb.max_bid < i.min_sale_price) AND i.cancellation_reason IS NULL 
					        THEN '-' 
					    -- no bids were placed
					    WHEN mb.max_bid IS NULL AND i.cancellation_reason IS NULL 
					        THEN '-'
					    -- auction was canceled 
					    WHEN i.cancellation_reason IS NOT NULL 
					        THEN 'Canceled'
        			    ELSE '-'
						END AS "Winner",
					i.end_time AS "Auction Ended" 
                    FROM item i
                    LEFT JOIN (
                        SELECT item_id,
                        MAX(bid_amount) AS max_bid 
                        FROM "bid"
                        GROUP BY item_id) AS mb ON i.item_id = mb.item_id 
                    WHERE i.end_time <= NOW()
                    ORDER BY i.end_time DESC;
                """
                    
            result = execute_query(query) 
            #print("RESULT:", result, "\nresult TYPE:", type(result))
            return result
        
        except Exception as e:
            print(f"Unable to get auction results, ERROR: {e}")
            return False