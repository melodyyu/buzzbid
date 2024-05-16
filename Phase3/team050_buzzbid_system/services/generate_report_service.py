from database.connection import execute_query
from database.connection import execute_search_query
from collections import defaultdict

class GenerateReportService:
    @staticmethod
    def category_report():
        query = """SELECT 
                    i.category_name AS "Category", 
                    COUNT(i.item_id) AS "Total Items", 
                    MIN(i.get_it_now_price) FILTER (WHERE i.get_it_now_price > 0) AS "Min Price", 
                    MAX(i.get_it_now_price) AS "Max Price", 
                    ROUND(AVG(i.get_it_now_price) FILTER (WHERE i.get_it_now_price > 0), 2) AS "Average Price" 
                    FROM "item" i 
                    WHERE i.cancellation_reason IS NULL 
                    GROUP BY i.category_name 
                    ORDER BY i.category_name ASC; 
                """
        result = execute_query(query)
        if result:
            return_dict = defaultdict(list)
            for row in result:
                return_dict["Category"].append(row[0])
                return_dict["Total Items"].append(row[1])
                return_dict["Min Price"].append(row[2])
                return_dict["Max Price"].append(row[3])
                return_dict["Average Price"].append(row[4])
            return return_dict
        else:
            return None

    @staticmethod
    def get_user_details(username):
        query = """SELECT first_name, last_name FROM "user" WHERE username = %s;"""
        result = execute_query(query, (username,))
        if result:
            user_details = result[0]
            return {
                "first_name": user_details[0],
                "last_name": user_details[1]
            }
        else:
            return {"first_name": "", "last_name": ""}

    @staticmethod
    def user_report():
        query = """
                WITH UserListings AS ( 
                SELECT 
                    username, 
                    COUNT(*) AS total_listings, 
                    COUNT(DISTINCT item_id) AS unique_listings
                FROM 
                    "item" i
                GROUP BY 
                    username
                ), 
                UserSold AS (
                    SELECT 
                        i.username, 
                        COUNT(*) AS total_sold
                    FROM 
                        "item" i
                    JOIN (
                        SELECT 
                            item_id, 
                            MAX(bid_amount) AS winning_bid
                        FROM 
                            "bid" b
                        GROUP BY 
                            item_id
                    ) winning_bid_table ON winning_bid_table.item_id = i.item_id
                    JOIN 
                        "bid" b ON b.item_id = i.item_id AND b.bid_amount = winning_bid_table.winning_bid
                    WHERE 
                        b.bid_amount >= i.min_sale_price 
                        AND i.end_time <= NOW() 
                        AND i.cancellation_reason IS NULL
                    GROUP BY 
                        i.username
                ), 
                UserWins AS (
                    SELECT 
                        b.username,
                        COUNT(*) AS wins
                    FROM 
                        "bid" b
                    JOIN 
                        "item" i ON b.item_id = i.item_id 
                    WHERE 
                        b.bid_amount >= i.min_sale_price 
                        AND i.end_time <= NOW() 
                        AND b.bid_amount = (
                            SELECT 
                                MAX(bid_amount) 
                            FROM 
                                "bid"
                            WHERE 
                                item_id = b.item_id
                        ) 
                        AND i.cancellation_reason IS NULL 
                        AND i.end_time <= NOW()
                    GROUP BY 
                        b.username
                ), 
                UserRatings AS (
                    SELECT 
                        auction_winner,
                        COUNT(*) AS winner_total_ratings
                    FROM (
                        SELECT 
                            r.*,
                            i.username AS item_owner,
                            b.username AS auction_winner
                        FROM 
                            "rating" r
                        INNER JOIN 
                            "item" i ON r.item_id = i.item_id
                        JOIN 
                            (
                            SELECT 
                                b1.item_id,
                                b1.username,
                                b1.bid_amount AS highest_bid,
                                b1.bid_time
                            FROM 
                                "bid" b1
                            WHERE 
                                (b1.item_id, b1.bid_amount) IN (
                                    SELECT 
                                        item_id,
                                        MAX(bid_amount) AS highest_bid
                                    FROM "bid" b2
                                    GROUP BY item_id
                                    )
                            ) b ON b.item_id = i.item_id
                    ) AS auction_winners
                    GROUP BY 
                        auction_winner
                ),
                MostFrequentCondition AS ( 
                    SELECT 
                        cc.username, 
                        COALESCE(cc.condition::text, 'N/A') AS most_frequent_condition
                    FROM (
                        SELECT DISTINCT ON (username) 
                            username, 
                            condition 
                        FROM (
                            SELECT 
                                username, 
                                condition, 
                                COUNT(*) AS condition_count
                            FROM 
                                "item"
                            GROUP BY 
                                username, 
                                condition
                            ORDER BY 
                                username, 
                                condition_count DESC
                        ) AS condition_counts
                    ) AS cc
                ) 
                SELECT 
                    u.username AS "Username",
                    COALESCE(ul.total_listings, 0) AS "Listed",
                    COALESCE(us.total_sold, 0) AS "Sold",
                    COALESCE(uw.wins, 0) AS "Won",
                    COALESCE(uc.winner_total_ratings, 0) AS "Rated", 
                    COALESCE(mfc.most_frequent_condition::text, 'N/A') AS "Most Frequent Condition"
                FROM 
                    "user" u
                LEFT JOIN 
                    UserListings ul ON u.username = ul.username
                LEFT JOIN 
                    UserSold us ON u.username = us.username
                LEFT JOIN 
                    UserWins uw ON u.username = uw.username
                LEFT JOIN 
                    UserRatings uc ON u.username = uc.auction_winner
                LEFT JOIN 
                    MostFrequentCondition mfc ON u.username = mfc.username 
                ORDER BY 
                    coalesce(ul.total_listings, 0) DESC;

                """
        
        result = execute_search_query(query)
        print("RESULTS:", result, "result TYPE:", type(result))
        return result
            


    @staticmethod
    def top_rated_items_report():
        query = """
        SELECT
        i.name AS "Item Name", ROUND(AVG(r.number_of_stars)::NUMERIC, 1) AS "Average Rating", COUNT(r.number_of_stars) AS "Rating Count"
        FROM "rating" r
        JOIN "item" i ON r.item_id = i.item_id
        GROUP BY i.name
        HAVING COUNT(r.number_of_stars) > 0 ORDER BY "Average Rating" DESC, LOWER(name) LIMIT 10;
        """
        result = execute_query(query)
        return result

    @staticmethod
    def auction_statistics_report():
        # Dictionary to hold your statistics
        statistics = {
            'Auctions Active': 0,
            'Auctions Finished': 0,
            'Auctions Won': 0,
            'Auctions Cancelled': 0,
            'Items Rated': 0,
            'Items Not Rated': 0,
        }

        # Define your SQL queries
        queries = {
            'Auctions Active': """
                SELECT COUNT(*) FROM "item"
                WHERE cancellation_reason IS NULL AND end_time > NOW();
            """,
            'Auctions Finished': """
                SELECT COUNT(*) FROM "item"
                WHERE cancellation_reason IS NULL AND end_time <= NOW();
            """,
            'Auctions Won': """
                SELECT COUNT(DISTINCT item_id)
                FROM (
                    SELECT i.item_id
                    FROM "item" i
                    JOIN "bid" b ON i.item_id = b.item_id
                    WHERE i.cancellation_reason IS NULL AND i.end_time <= NOW()
                    GROUP BY i.item_id, i.min_sale_price
                    HAVING MAX(b.bid_amount) >= i.min_sale_price
                ) AS valid_items;
            """,
            'Auctions Cancelled': """
                SELECT COUNT(*) FROM "item"
                WHERE cancellation_reason IS NOT NULL;
            """,
            'Items Rated': """
                SELECT COUNT(*) FROM "rating";
            """,
            'Items Not Rated': """
                SELECT COUNT(*) FROM "item" i
                WHERE NOT EXISTS (
                    SELECT 1 FROM "rating" r
                    WHERE i.item_id = r.item_id
                );
            """
        }

        # Execute each query and update the statistics dictionary
        statistics = {}

        for key, query in queries.items():
            result = execute_query(query)
            statistics[key] = result[0][0] if result else 0

        return statistics

    @staticmethod
    def cancelled_auctions_report():
        query = """
        SELECT
            i.item_id AS "ID",
            i.username AS "Listed By",
            i.end_time AS "Cancelled Date",
            i.cancellation_reason AS "Reason"
        FROM "item" i
        WHERE i.cancellation_reason IS NOT NULL
        ORDER BY i.item_id DESC;
        """
        result = execute_query(query)
        return result if result else []


    